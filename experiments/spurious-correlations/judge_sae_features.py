#!/usr/bin/env python3
"""
Judge whether a set of SAE/transcoder features contains spurious ones.

Takes the top-N features ranked by EITHER biased or unbiased probe cosine similarity
(from rank_sae_features_by_probe.py), fetches their Neuronpedia descriptions, then
asks an LLM: "Does this feature set contain spurious features?"

The judge sees only the input prompt, the task description, and the features —
it does NOT know whether the features came from a biased or unbiased ranking.

Hypothesis: features ranked by the biased probe should contain spurious ones
(high cos_sim_biased → encodes spurious signal); features ranked by the unbiased
probe should not.

Usage:
    python experiments/spurious-correlations/judge_sae_features.py \\
        --input probe_plt_features/bib_journalist_dietitian-pos_pos_1-transcoder.json \\
        --ranking biased

    python experiments/spurious-correlations/judge_sae_features.py \\
        --input probe_plt_features/bib_journalist_dietitian-pos_pos_1-transcoder.json \\
        --ranking unbiased

    # Run both rankings in one go (saves two result files)
    python experiments/spurious-correlations/judge_sae_features.py \\
        --input probe_plt_features/bib_journalist_dietitian-pos_pos_1-transcoder.json \\
        --ranking both

--> python judge_sae_features.py --input probe_plt_features/bib_*-sae.json --ranking both --top-n 20
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from anthropic import Anthropic

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_HERE     = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent

NP_MODEL_ID          = "gemma-2-2b"
NP_TRANSCODER_SAE_ID = "22-gemmascope-transcoder-16k"
NP_SAE_SAE_ID        = "22-gemmascope-res-16k"

DEFAULT_TOP_N  = 20
DEFAULT_MODEL  = "minimax/minimax-m2.7"
NP_TIMEOUT     = 15
NP_RETRY_DELAY = 1.0

# Per-dataset task descriptions and spuriosity concerns (mirrors run_oracle_on_probes.py)
DATASET_CONCERNS = {
    "bib_journalist_dietitian": (
        "binary profession classification (dietitian vs journalist)",
        "The features encode spurious gender markers rather than genuine profession indicators to predict the profession.",
    ),
    "bib_nurse_professor": (
        "binary profession classification (nurse vs professor)",
        "The features encode spurious gender markers rather than genuine profession indicators to predict the profession.",
    ),
    "bib_surgeon_teacher": (
        "binary profession classification (surgeon vs teacher)",
        "The features encode spurious gender markers rather than genuine profession indicators to predict the profession.",
    ),
    "civil_comments": (
        "toxicity classification",
        "The features encode spurious identity-group signals rather than actual toxic content to predict toxicity.",
    ),
    "multinli": (
        "natural language inference (contradiction vs entailment)",
        "The features encode spurious negation-word signals rather than actual semantic contradiction to predict contradiction.",
    ),
}


# ---------------------------------------------------------------------------
# Neuronpedia
# ---------------------------------------------------------------------------

def fetch_neuronpedia(feature_idx: int, sae_id: str) -> dict:
    url = f"https://www.neuronpedia.org/api/feature/{NP_MODEL_ID}/{sae_id}/{feature_idx}"
    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=NP_TIMEOUT)
            if resp.status_code == 429:
                time.sleep(NP_RETRY_DELAY * (attempt + 1))
                continue
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            if attempt == 2:
                return {"error": str(e)}
            time.sleep(NP_RETRY_DELAY)
    else:
        return {"error": "Max retries exceeded"}

    data = resp.json()

    label = "No explanation available"
    if data.get("explanations"):
        label = data["explanations"][0].get("description", label)

    top_examples = []
    for act in (data.get("activations") or [])[:3]:
        tokens = act.get("tokens", [])
        values = act.get("values", [])
        text = "".join(tokens)[:200]
        max_val = max(values) if values else 0
        max_idx = values.index(max_val) if values else 0
        max_token = tokens[max_idx] if max_idx < len(tokens) else ""
        top_examples.append({
            "text_snippet": text,
            "max_activation": round(max_val, 3),
            "max_token": max_token,
        })

    return {
        "feature_idx":             feature_idx,
        "label":                   label,
        "top_activating_examples": top_examples,
        "promoted_tokens":         data.get("pos_str", [])[:10],
        "suppressed_tokens":       data.get("neg_str", [])[:10],
        "frac_nonzero":            data.get("frac_nonzero"),
    }


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def select_features(features: list[dict], ranking: str, top_n: int) -> list[dict]:
    """Return top-N features sorted by the chosen ranking key."""
    key = "rank_biased" if ranking == "biased" else "rank_unbiased"
    return sorted(features, key=lambda f: f[key])[:top_n]


SYSTEM_PROMPT = f"""\
You are an interpretability researcher analyzing sparse autoencoder (SAE) features \
from a language model (Gemma-2-2B).

You will be given:
- An input text that was passed through the model
- The task the model is being probed for
- A set of SAE features that were active on this input, along with their \
  Neuronpedia labels and activating examples

Your job is to  determine whether the concern is true.

Respond with:
1. A verdict: YES (spurious features present) or NO (no spurious features)
2. A list of any spurious features identified, with reasoning
3. A brief overall summary
"""


def build_user_prompt(
    prompt: str,
    dataset: str,
    task_desc: str,
    concern: str,
    features_with_np: list[dict],
) -> str:
    lines = [
        f"Input text: {prompt[:400]}",
        f"Task: {task_desc}",
        f"Concern: {concern}",
        "",
        f"Active SAE features ({len(features_with_np)} shown):",
        "",
    ]

    for f in features_with_np:
        np = f.get("neuronpedia", {})
        lines += [
            f"Feature {f['feature_idx']}",
            f"  label:             {np.get('label', 'N/A')}",
            f"  promoted_tokens:   {np.get('promoted_tokens', [])}",
            f"  suppressed_tokens: {np.get('suppressed_tokens', [])}",
        ]
        for ex in np.get("top_activating_examples", []):
            lines.append(
                f"  example [{ex['max_token']!r} @{ex['max_activation']}]: "
                f"{ex['text_snippet'][:120]!r}"
            )
        lines.append("")

    lines.append(
        "Do these features contain spurious ones? "
        "Verdict (YES/NO), list of spurious features with reasoning, and summary."
    )
    return "\n".join(lines)


def run_one(
    input_path: Path,
    ranking: str,
    top_n: int,
    client: Anthropic,
    model: str,
) -> Path:
    # Save
    OUT_DIR = _HERE / "probe_sae_analysis"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{input_path.stem}-{ranking}.json"
    if os.path.exists(out_path):
        return out_path
    
    with open(input_path) as f:
        ranking_data = json.load(f)

    dataset   = ranking_data.get("dataset", "unknown")
    feat_type = ranking_data.get("type", "transcoder")
    prompt    = ranking_data.get("prompt", "")
    features  = ranking_data.get("features", [])

    task_desc, concern = DATASET_CONCERNS.get(dataset, ("unknown task", "unknown concern"))
    sae_id = NP_TRANSCODER_SAE_ID if feat_type == "transcoder" else NP_SAE_SAE_ID

    selected = select_features(features, ranking, top_n)
    print(f"  Top-{top_n} by {ranking} ranking → {len(selected)} features")

    # Fetch Neuronpedia
    features_with_np = []
    for f in selected:
        fidx = f["feature_idx"]
        print(f"    NP {fidx}...", end=" ", flush=True)
        np_info = fetch_neuronpedia(fidx, sae_id)
        if "error" in np_info:
            print(f"ERROR: {np_info['error']}")
        else:
            print(f"{np_info['label'][:55]}")
        features_with_np.append({**f, "neuronpedia": np_info})

    # Print summary table
    print()
    for f in features_with_np:
        np = f.get("neuronpedia", {})
        print(
            f"    [{f['feature_idx']:5d}] "
            f"b={f['cos_sim_biased']:+.3f}(#{f['rank_biased']:3d}) "
            f"u={f['cos_sim_unbiased']:+.3f}(#{f['rank_unbiased']:3d})  "
            f"{np.get('label', '')[:55]}"
        )

    # LLM call
    user_msg = build_user_prompt(prompt, dataset, task_desc, concern, features_with_np)
    print(f"\n  Querying {model}...", flush=True)
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        thinking={"type": "enabled", "budget_tokens": 1024},
        messages=[{"role": "user", "content": user_msg}],
    )
    try:
        analysis = next(b.text for b in response.content if b.type == "text").strip()
    except Exception as ex:
        print(response.content)
        raise(ex)

    print("\n  --- LLM verdict ---")
    print(analysis)


    with open(out_path, "w") as f:
        json.dump({
            "input_file":         str(input_path),
            "dataset":            dataset,
            "type":               feat_type,
            "prompt":             prompt,
            "ranking":            ranking,
            "top_n":              top_n,
            "model":              model,
            "features_inspected": features_with_np,
            "analysis":           analysis,
        }, f, indent=2)
    print(f"  Saved → {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Judge spuriosity of SAE features ranked by probe cosine similarity"
    )
    parser.add_argument("--input", nargs="+", required=True,
                        help="Ranking JSON file(s) from rank_sae_features_by_probe.py")
    parser.add_argument("--ranking", default="both", choices=["biased", "unbiased", "both"],
                        help="Which probe ranking to use when selecting features (default: both)")
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N,
                        help=f"Number of top features to inspect (default: {DEFAULT_TOP_N})")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--provider", default=os.environ.get("LLM_PROVIDER", "openrouter"),
                        choices=["anthropic", "openrouter"])
    args = parser.parse_args()

    # Load .env
    env_path = _REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    # Build client
    if args.provider == "openrouter":
        client = Anthropic(
            base_url="https://openrouter.ai/api",
            auth_token=os.environ.get("OPENROUTER_API_KEY", ""),
            api_key="",
        )
        model = args.model 
    else:
        client = Anthropic()
        model = args.model

    # Resolve input files
    input_paths = []
    for pattern in args.input:
        p = Path(pattern)
        if p.exists():
            input_paths.append(p)
        else:
            matches = sorted(_HERE.glob(pattern)) or sorted(Path(".").glob(pattern))
            if not matches:
                print(f"WARNING: no files matched: {pattern}")
            input_paths.extend(matches)

    if not input_paths:
        print("No input files found.")
        sys.exit(1)

    rankings = ["biased", "unbiased"] if args.ranking == "both" else [args.ranking]

    for path in input_paths:
        print(f"\n{'='*60}\n{path.name}\n{'='*60}")
        for ranking in rankings:
            print(f"\n-- ranking: {ranking} --")
            run_one(path, ranking, args.top_n, client, model)

    print("\nAll done.")


if __name__ == "__main__":
    main()
