"""FastAPI shim that mimics Neuronpedia's `/api/feature/{model}/{sae}/{idx}`
endpoint, but serves descriptions from the local autointerp cache.

Why: `inspect_feature` was written against Neuronpedia's HTTP API. For
transcoder sets that aren't on Neuronpedia (e.g. mwhanna/qwen3-8b-transcoders)
the calls 500 and the oracle goes blind. Pointing `ToolContext.neuronpedia_base_url`
at this server lets `inspect_feature` keep its single code path while the
descriptions are generated locally via `describe_feature`.

Run via `scripts/run_autointerp_server.py` (which sets `--features-dir` and
`--cache-dir` for the qwen3-8b transcoders) or directly:

    uvicorn circuit_oracle.autointerp_server:create_app \
        --factory --host 127.0.0.1 --port 8765
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException

from .autointerp import (
    AutointerpConfig,
    AutointerpStore,
    FeatureCache,
    describe_feature,
)


def _layer_from_sae_id(sae_id: str) -> int:
    """Extract layer index from an SAE ID like '20-transcoder-hp'."""
    head = sae_id.split("-", 1)[0]
    try:
        return int(head)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot parse layer from sae_id={sae_id!r} (expected '<layer>-...')",
        ) from e


def _to_neuronpedia_shape(rec: dict, feature_data: dict) -> dict[str, Any]:
    """Translate local autointerp output into the JSON shape `_neuronpedia_inspect` expects.

    Required fields:
      - explanations: [{"description": str}]
      - activations: [{"tokens": [...], "values": [...]}]  (top quantile)
      - pos_str / neg_str: top/bottom promoted tokens
      - frac_nonzero: activation frequency
    """
    description = rec.get("label") or "No explanation available"

    activations: list[dict[str, Any]] = []
    for q in feature_data.get("examples_quantiles", []):
        for ex in q.get("examples", []):
            tokens = ex.get("tokens", [])
            values = ex.get("tokens_acts_list", [])
            if not tokens:
                continue
            activations.append({"tokens": tokens, "values": values})
            if len(activations) >= 3:
                break
        if len(activations) >= 3:
            break

    return {
        "explanations": [{"description": description}],
        "activations": activations,
        "pos_str": feature_data.get("top_logits", [])[:10],
        "neg_str": feature_data.get("bottom_logits", [])[:10],
        "frac_nonzero": feature_data.get("activation_frequency"),
    }


def create_app(
    features_dir: str | None = None,
    cache_dir: str | None = None,
    autointerp_model: str = "minimax/minimax-m2.7",
    api_key: str | None = None,
) -> FastAPI:
    features_dir = features_dir or os.environ.get("AUTOINTERP_FEATURES_DIR")
    cache_dir = cache_dir or os.environ.get("AUTOINTERP_CACHE_DIR")
    autointerp_model = os.environ.get("AUTOINTERP_MODEL", autointerp_model)
    if not features_dir or not cache_dir:
        raise RuntimeError(
            "autointerp_server needs features_dir and cache_dir "
            "(pass to create_app() or set AUTOINTERP_FEATURES_DIR / AUTOINTERP_CACHE_DIR)."
        )

    feature_cache = FeatureCache(features_dir)
    store = AutointerpStore(cache_dir)
    config = AutointerpConfig(
        features_dir=features_dir,
        cache_dir=cache_dir,
        model=autointerp_model,
        api_key=api_key,
    )

    app = FastAPI(title="Local autointerp Neuronpedia shim")

    @app.get("/healthz")
    def healthz() -> dict[str, Any]:
        return {
            "ok": True,
            "features_dir": features_dir,
            "cache_dir": cache_dir,
            "model": config.model,
        }

    @app.get("/api/feature/{model_id}/{sae_id}/{feature_idx}")
    def get_feature(model_id: str, sae_id: str, feature_idx: int) -> dict[str, Any]:
        layer = _layer_from_sae_id(sae_id)
        try:
            rec = describe_feature(
                layer,
                feature_idx,
                feature_cache=feature_cache,
                store=store,
                config=config,
            )
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        feature_data = feature_cache.get(layer, feature_idx)
        return _to_neuronpedia_shape(rec, feature_data)

    return app
