#!/usr/bin/env python3
"""
Rank SAE/transcoder features by cosine similarity with biased and unbiased probe weights.

For a given prompt, pass it through Gemma-2-2B, collect layer-22 residual stream
activations, encode with a SAELens SAE or transcoder, then compute cosine similarity
of each active feature's decoder direction with the biased and unbiased probe weight
vectors.  Save ranked results to probe_sae_features/ or probe_plt_features/.

Usage:
    python experiments/spurious-correlations/rank_sae_features_by_probe.py \
        --dataset bib_journalist_dietitian \
        --type sae          # or --type transcoder
        --prompt "She is a nurse."

    # Run all datasets with default sample prompt
    python experiments/spurious-correlations/rank_sae_features_by_probe.py --all
"""

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL_NAME  = "google/gemma-2-2b"
PROBE_LAYER = {
    "bib_nurse_professor": 22,
    "bib_journalist_dietitian": 22,
    "bib_surgeon_teacher": 22,
    "civil_comments": 12,
    "multinli": 17,
}
DATASET_JSON = Path(__file__).resolve().parent / "prompts.json"
PROBE_DIR   = Path(__file__).resolve().parent / "probe_extraction" / "probes"
OUT_SAE_DIR = Path(__file__).resolve().parent / "probe_sae_features"
OUT_PLT_DIR = Path(__file__).resolve().parent / "probe_plt_features"
DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE       = torch.float32   # SAELens works in float32
print("Device set to:", DEVICE)
# SAELens release / SAE-id for Gemma-2-2B layer 22
# SAE_RELEASE        = "gemma-scope-2b-pt-res"
# SAE_ID             = "layer_22/width_16k/average_l0_72"
SAE_RELEASE        = "gemma-scope-2b-pt-res-canonical"
SAE_ID             = "layer_22/width_16k/canonical"

TRANSCODER_RELEASE = "gemma-scope-2b-pt-transcoders"
TRANSCODER_ID      = "layer_22/width_16k/average_l0_15"

DATASETS = [
    "bib_journalist_dietitian",
    "bib_nurse_professor",
    "bib_surgeon_teacher",
    "civil_comments",
    "multinli",
]

def parse_dataset_prompts(dataset: str) -> dict[str, list[str]]:
    """
    Parse probe_spuriosity/analysis.md and return
    {'neg_neg': [...prompts...], 'pos_pos': [...prompts...]}
    for the given dataset.

    neg_neg = subgroup with (true=0, spurious=0)
    pos_pos = subgroup with (true=1, spurious=1)
    Up to 5 prompts per subgroup (takes the "Top N" listed ones).
    """
    prompt_dataset = json.load(open(DATASET_JSON, "r"))
    result = prompt_dataset[dataset]
    return result

# ---------------------------------------------------------------------------
# Probe loading
# ---------------------------------------------------------------------------

class Probe(nn.Module):
    def __init__(self, activation_dim: int, dtype=torch.bfloat16):
        super().__init__()
        self.net = nn.Linear(activation_dim, 1, bias=True, dtype=dtype)

    @property
    def weight_vec(self) -> torch.Tensor:
        return self.net.weight.squeeze(0).detach()


def load_probe(path: Path, device: str) -> Probe:
    checkpoint = torch.load(path, weights_only=True, map_location=device)
    probe = Probe(checkpoint["activation_dim"])
    probe.load_state_dict(checkpoint["state_dict"])
    return probe.eval()


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def get_layer22_activations(prompt: str, model_tl, probe_leyer) -> torch.Tensor:
    """Return mean-pooled layer-22 residual stream activations, shape (d_model,)."""
    hook_name = f"blocks.{probe_leyer}.hook_resid_post"
    tokens = model_tl.to_tokens(prompt, prepend_bos=True)
    with torch.no_grad():
        _, cache = model_tl.run_with_cache(tokens, names_filter=hook_name)
    h = cache[hook_name]          # (1, n_pos, d_model)
    pooled = h[0].mean(dim=0)     # (d_model,)
    return pooled.to(DTYPE)


def rank_features(
    prompt: str,
    dataset: str,
    sae_type: str,   # "sae" or "transcoder"
    model_tl,
    sae_or_transcoder,
    probe_biased: Probe,
    probe_unbiased: Probe,
) -> dict:
    """Run one prompt, return a dict with ranked feature info."""

    # 1. Layer-22 residual stream activations
    acts = get_layer22_activations(prompt, model_tl, PROBE_LAYER[dataset])   # (d_model,)
    acts_device = acts.to(DEVICE)

    # 2. Encode through SAE/transcoder → sparse feature activations
    with torch.no_grad():
        feature_acts = sae_or_transcoder.encode(acts_device.unsqueeze(0))  # (1, n_features)
    feature_acts = feature_acts.squeeze(0)  # (n_features,)

    # 3. Find active features (activation > 0)
    active_mask = feature_acts > 0
    active_indices = active_mask.nonzero(as_tuple=True)[0].tolist()

    if len(active_indices) == 0:
        return {"prompt": prompt, "dataset": dataset, "type": sae_type, "features": []}
    else:
        print(f"active_indices: {len(active_indices)}")
    # 4. Get decoder directions for active features
    # W_dec shape in SAELens: (n_features, d_model)
    W_dec = sae_or_transcoder.W_dec  # (n_features, d_model)
    dec_dirs = W_dec[active_indices]  # (n_active, d_model)
    dec_dirs_f32 = dec_dirs.to(DTYPE)

    # 5. Probe weight vectors (d_model,), normalise for cosine similarity
    w_biased   = probe_biased.weight_vec.to(DTYPE).to(DEVICE)
    w_unbiased = probe_unbiased.weight_vec.to(DTYPE).to(DEVICE)

    cos_biased   = F.cosine_similarity(dec_dirs_f32, w_biased.unsqueeze(0),   dim=-1)
    cos_unbiased = F.cosine_similarity(dec_dirs_f32, w_unbiased.unsqueeze(0), dim=-1)

    cos_biased_list   = cos_biased.cpu().tolist()
    cos_unbiased_list = cos_unbiased.cpu().tolist()
    activations_list  = feature_acts[active_indices].cpu().tolist()

    # 6. Build ranked lists (descending by cosine sim)
    rank_by_biased   = sorted(range(len(active_indices)), key=lambda i: -cos_biased_list[i])
    rank_by_unbiased = sorted(range(len(active_indices)), key=lambda i: -cos_unbiased_list[i])

    rank_biased_map   = {i: r for r, i in enumerate(rank_by_biased)}
    rank_unbiased_map = {i: r for r, i in enumerate(rank_by_unbiased)}

    features = []
    for i, feat_idx in enumerate(active_indices):
        features.append({
            "feature_idx":      feat_idx,
            "activation":       activations_list[i],
            "cos_sim_biased":   cos_biased_list[i],
            "cos_sim_unbiased": cos_unbiased_list[i],
            "rank_biased":      rank_biased_map[i],
            "rank_unbiased":    rank_unbiased_map[i],
        })

    # Sort by rank_biased for readability
    features.sort(key=lambda f: f["rank_biased"])

    return {
        "prompt":   prompt,
        "dataset":  dataset,
        "type":     sae_type,
        "n_active": len(active_indices),
        "features": features,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Rank SAE/transcoder features by probe cosine similarity")
    parser.add_argument("--dataset", default=None, choices=DATASETS, help="Dataset slug")
    parser.add_argument("--type",    default="transcoder", choices=["sae", "transcoder"],
                        help="Use residual SAE or transcoder (default: transcoder)")
    parser.add_argument("--all",     action="store_true", help="Run all datasets")
    args = parser.parse_args()

    if not args.all and args.dataset is None:
        parser.error("Provide --dataset or --all")

    datasets = DATASETS if args.all else [args.dataset]

    # --- Load model (shared across datasets) ---
    print(f"Loading {MODEL_NAME} via transformer_lens...", flush=True)
    import transformer_lens
    model_tl = transformer_lens.HookedTransformer.from_pretrained(
        MODEL_NAME,
        dtype=DTYPE,
        device=DEVICE,
    )
    model_tl.eval()
    print("Model loaded.", flush=True)

    # --- Load SAE / transcoder (shared across datasets) ---
    from sae_lens import SAE
    if args.type == "sae":
        print(f"Loading SAE: {SAE_RELEASE} / {SAE_ID}", flush=True)
        sae = SAE.from_pretrained(SAE_RELEASE, SAE_ID, device=DEVICE)
    else:
        from sae_lens import Transcoder
        print(f"Loading transcoder: {TRANSCODER_RELEASE} / {TRANSCODER_ID}", flush=True)
        sae = Transcoder.from_pretrained(TRANSCODER_RELEASE, TRANSCODER_ID, device=DEVICE)
    sae.eval()
    print(f"SAE/transcoder loaded. W_dec shape: {sae.W_dec.shape}", flush=True)

    out_dir = OUT_SAE_DIR if args.type == "sae" else OUT_PLT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    for dataset in datasets:
        print(f"\n--- Dataset: {dataset} ---", flush=True)
        
        # Load probes
        biased_path   = PROBE_DIR / f"{dataset}_layer{PROBE_LAYER[dataset]}_bfloat16.pt"
        unbiased_path = PROBE_DIR / f"{dataset}_layer{PROBE_LAYER[dataset]}_bfloat16_unbiased.pt"
        assert biased_path.exists(),   f"Not found: {biased_path}"
        assert unbiased_path.exists(), f"Not found: {unbiased_path}"

        probe_biased   = load_probe(biased_path,   DEVICE)
        probe_unbiased = load_probe(unbiased_path, DEVICE)
        print(f"Probes loaded.", flush=True)

        prompt_ds = parse_dataset_prompts(dataset)
        
        for prompt_type, prompts in prompt_ds.items():
            # For civil_comments and multinli
            # if 'neg_neg' in prompt_type:
            #     continue
            for idx, prompt in enumerate(prompts):
                print(f"{prompt_type}_{idx+1} Prompt: {prompt[:80]}...", flush=True)

                result = rank_features(
                    prompt=prompt,
                    dataset=dataset,
                    sae_type=args.type,
                    model_tl=model_tl,
                    sae_or_transcoder=sae,
                    probe_biased=probe_biased,
                    probe_unbiased=probe_unbiased,
                )

                out_path = out_dir / f"{dataset}-{prompt_type}_{idx+1}-{args.type}.json"
                with open(out_path, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"Saved {result['n_active']} active features → {out_path}", flush=True)

    print("\nDone.", flush=True)


if __name__ == "__main__":
    main()
