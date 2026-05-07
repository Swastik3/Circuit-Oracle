"""Local autointerp: generate feature descriptions from cached top-activating examples.

For transcoders not hosted on Neuronpedia (e.g. mwhanna/qwen3-8b-transcoders),
this module reads the local `features/` cache and uses an LLM to produce a
one-line description per feature, mimicking Neuronpedia's autointerp labels.
Generated descriptions are persisted to a JSONL file so future calls are
free and auditable.

On-disk format (matches circuit-tracer's frontend, see
`circuit_tracer/frontend/feature_models.py` and `assets/util.js:89-93`):
- features/index.json.gz: {layer_idx: {filename, offsets[]}}
- features/layer_N.bin: concatenated chunks, each
  [4-byte LE uint32 length][gzip(json)] where the JSON conforms to
  feature_models.Model.
"""

from __future__ import annotations

import gzip
import json
import os
import struct
import threading
import time
from dataclasses import dataclass
from typing import Any

from .llm_client import LLMClient


# ---------- Feature cache (binary loader) ----------

class FeatureCache:
    """Read per-feature records from a transcoder repo's `features/` directory."""

    def __init__(self, features_dir: str):
        self.features_dir = features_dir
        index_path = os.path.join(features_dir, "index.json.gz")
        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"Missing {index_path}. Run scripts/download_features.py first."
            )
        with gzip.open(index_path, "rb") as f:
            raw = json.load(f)
        # Top-level mixes metadata ("version", "format") with per-layer entries
        # keyed by stringified layer index — keep only the numeric keys.
        self._index: dict[int, dict] = {
            int(k): v for k, v in raw.items() if k.lstrip("-").isdigit()
        }
        self._read_lock = threading.Lock()

    def get(self, layer: int, feature_idx: int) -> dict[str, Any]:
        if layer not in self._index:
            raise KeyError(f"Layer {layer} not in feature index.")
        entry = self._index[layer]
        offsets = entry["offsets"]
        if feature_idx < 0 or feature_idx + 1 >= len(offsets):
            raise KeyError(
                f"Feature {feature_idx} out of range for layer {layer} "
                f"(have {len(offsets) - 1} features)."
            )
        bin_path = os.path.join(self.features_dir, entry["filename"])
        start, end = offsets[feature_idx], offsets[feature_idx + 1]
        with self._read_lock, open(bin_path, "rb") as fh:
            fh.seek(start)
            chunk = fh.read(end - start)
        data_len = struct.unpack("<I", chunk[:4])[0]
        payload = gzip.decompress(chunk[4:4 + data_len])
        return json.loads(payload)


# ---------- On-disk JSONL store ----------

class AutointerpStore:
    """Append-only JSONL of generated descriptions, indexed by (layer, feature_idx)."""

    def __init__(self, cache_dir: str, filename: str = "autointerp.jsonl"):
        os.makedirs(cache_dir, exist_ok=True)
        self.path = os.path.join(cache_dir, filename)
        self._index: dict[tuple[int, int], dict] = {}
        self._write_lock = threading.Lock()
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                self._index[(rec["layer"], rec["feature_idx"])] = rec

    def get(self, layer: int, feature_idx: int) -> dict | None:
        return self._index.get((layer, feature_idx))

    def put(self, record: dict) -> None:
        key = (record["layer"], record["feature_idx"])
        with self._write_lock:
            with open(self.path, "a") as f:
                f.write(json.dumps(record) + "\n")
            self._index[key] = record


# ---------- Prompt + LLM call ----------

_AUTOINTERP_SYSTEM = (
    "You are an interpretability researcher. You will be shown the top-activating "
    "contexts of a single transcoder feature, along with the tokens it most promotes "
    "and suppresses in the output distribution. Write a single concise sentence "
    "(<=25 words) describing what this feature represents or detects. Focus on the "
    "semantic/syntactic pattern that activates it. Do not start with 'This feature' "
    "- write the description directly. Output only the description, no preamble."
)


def _format_examples(feature_data: dict, max_per_quantile: int = 3) -> str:
    lines = []
    for q in feature_data.get("examples_quantiles", []):
        qname = q.get("quantile_name", "?")
        examples = q.get("examples", [])[:max_per_quantile]
        if not examples:
            continue
        lines.append(f"\n## Quantile: {qname}")
        for ex in examples:
            tokens = ex.get("tokens", [])
            acts = ex.get("tokens_acts_list", [])
            if not tokens:
                continue
            max_act = max(acts) if acts else 0
            parts = []
            for tok, a in zip(tokens, acts):
                tok_disp = tok.replace("\n", "\\n")
                if max_act > 0 and a == max_act:
                    parts.append(f"[[{tok_disp}|{a:.2f}]]")
                elif a > 0:
                    parts.append(f"{tok_disp}|{a:.2f}")
                else:
                    parts.append(tok_disp)
            lines.append("  " + " ".join(parts))
    return "\n".join(lines) if lines else "(no examples)"


def _build_prompt(feature_data: dict) -> str:
    top_logits = feature_data.get("top_logits", [])[:10]
    bottom_logits = feature_data.get("bottom_logits", [])[:10]
    examples_block = _format_examples(feature_data)
    return (
        f"Top promoted tokens: {top_logits}\n"
        f"Top suppressed tokens: {bottom_logits}\n"
        f"Activation frequency: {feature_data.get('activation_frequency')}\n"
        f"\nTop-activating contexts (token|activation, [[max-token|act]] highlighted):\n"
        f"{examples_block}\n"
    )


# ---------- Public entry point ----------

@dataclass
class AutointerpConfig:
    features_dir: str
    cache_dir: str
    model: str = "minimax/minimax-m2.7"
    api_key: str | None = None  # falls back to OPENROUTER_API_KEY
    # Generous cap so reasoning models (e.g. MiniMax M2.7) have room to finish
    # their internal thinking and still emit the final description. The actual
    # answer is short (<25 words). Tune down if you switch to a non-reasoning
    # model to save cost.
    max_tokens: int = 8000


_clients: dict[str, LLMClient] = {}

def _get_client(api_key: str | None) -> LLMClient:
    key = api_key or ""
    if key not in _clients:
        _clients[key] = LLMClient(provider="openrouter", api_key=api_key)
    return _clients[key]


def describe_feature(
    layer: int,
    feature_idx: int,
    *,
    feature_cache: FeatureCache,
    store: AutointerpStore,
    config: AutointerpConfig,
    force_regenerate: bool = False,
) -> dict:
    """Return a feature description in the same shape as `tools.inspect_feature`.

    Always loads feature_data from the local cache (cheap disk read) so the
    return shape is consistent. The LLM is only called on cache miss.
    """
    feature_data = feature_cache.get(layer, feature_idx)

    cached = None if force_regenerate else store.get(layer, feature_idx)
    if cached is not None:
        description = cached["description"]
    else:
        prompt = _build_prompt(feature_data)
        client = _get_client(config.api_key)
        resp = client.create_message(
            model=config.model,
            system=_AUTOINTERP_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=config.max_tokens,
        )
        description = "".join(
            block.text for block in resp.content if getattr(block, "type", None) == "text"
        ).strip()
        store.put({
            "layer": layer,
            "feature_idx": feature_idx,
            "description": description,
            "model": config.model,
            "prompt": prompt,
            "timestamp": time.time(),
            "top_logits": feature_data.get("top_logits", [])[:10],
            "bottom_logits": feature_data.get("bottom_logits", [])[:10],
            "activation_frequency": feature_data.get("activation_frequency"),
        })

    top_examples = []
    for q in feature_data.get("examples_quantiles", []):
        for ex in q.get("examples", []):
            tokens = ex.get("tokens", [])
            acts = ex.get("tokens_acts_list", [])
            if not tokens:
                continue
            max_val = max(acts) if acts else 0
            max_idx = acts.index(max_val) if acts else 0
            top_examples.append({
                "text_snippet": "".join(tokens)[:200],
                "max_activation": round(max_val, 3),
                "max_token": tokens[max_idx] if max_idx < len(tokens) else "",
            })
            if len(top_examples) >= 3:
                break
        if len(top_examples) >= 3:
            break

    return {
        "layer": layer,
        "feature_idx": feature_idx,
        "label": description or "No explanation available",
        "top_activating_examples": top_examples,
        "promoted_tokens": feature_data.get("top_logits", [])[:10],
        "suppressed_tokens": feature_data.get("bottom_logits", [])[:10],
        "frac_nonzero": feature_data.get("activation_frequency"),
        "source": "local_autointerp",
    }
