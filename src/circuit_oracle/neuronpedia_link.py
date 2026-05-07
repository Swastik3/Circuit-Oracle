"""Neuronpedia URL helpers.

Per-feature dashboards live at:
    https://neuronpedia.org/{model_id}/{sae_id}/{feature_idx}

Where sae_id is templated like "{layer}-transcoder-hp" — the layer is filled
in per feature (config.py: ToolContext.neuronpedia_sae_id).
"""

from __future__ import annotations


def feature_url(layer: int, feature_idx: int, *, model_id: str, sae_template: str) -> str:
    """Return the Neuronpedia dashboard URL for a single transcoder feature.

    Raises ValueError on missing layer/feature_idx — fail loud rather than
    silently producing a bad URL like ".../None-transcoder-hp/None".
    """
    if layer is None or feature_idx is None:
        raise ValueError(
            f"feature_url requires non-None layer and feature_idx; got layer={layer}, feature_idx={feature_idx}"
        )
    sae_id = sae_template.format(layer=layer)
    return f"https://neuronpedia.org/{model_id}/{sae_id}/{feature_idx}"


def feature_link(layer: int, feature_idx: int, *, model_id: str, sae_template: str, label: str | None = None) -> str:
    """Return a markdown hyperlink to the Neuronpedia feature dashboard.

    label defaults to "L{layer}:F{feature_idx}".
    """
    url = feature_url(layer, feature_idx, model_id=model_id, sae_template=sae_template)
    txt = label or f"L{layer}:F{feature_idx}"
    return f"[{txt}]({url})"
