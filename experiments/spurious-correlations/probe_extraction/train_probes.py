#!/usr/bin/env python3
"""
Train biased and unbiased linear probes on model residual stream activations.

For each task, two probes are produced:
  {task_name}_layer{layer}_{dtype}.pt           -- biased probe (ambiguous split)
  {task_name}_layer{layer}_{dtype}_unbiased.pt  -- unbiased probe (balanced split)

Usage:
    python train_probes.py --config configs/bib_nurse_professor_gemma2_2b.yaml
    python train_probes.py --config configs/bib_nurse_professor_gemma2_2b.yaml --layer 18
    python train_probes.py --config configs/bib_nurse_professor_gemma2_2b.yaml --overwrite
"""

from __future__ import annotations
import argparse
import os
import sys
from collections import defaultdict
from functools import reduce
from pathlib import Path

import torch as t
import torch.nn as nn
from nnsight import LanguageModel
from tqdm import tqdm
import yaml

# Allow running as a script from any working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from probe_extraction.probe_model import Probe
from adapters import BiasInBiosAdapter, CivilCommentsAdapter, GenericHFAdapter, MultiNLIAdapter, DatasetAdapter


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def resolve_attr_path(obj, dotted_path: str):
    """Resolve a dotted attribute path, e.g. 'model.model.layers'."""
    return reduce(getattr, dotted_path.split("."), obj)


def pool_acts(acts: t.Tensor, attn_mask: t.Tensor) -> t.Tensor:
    """Mean-pool token activations weighted by the attention mask."""
    return (acts * attn_mask[:, :, None]).sum(1) / attn_mask.sum(1)[:, None]


# ---------------------------------------------------------------------------
# Activation collection
# ---------------------------------------------------------------------------

@t.no_grad()
def collect_activations(model, layer: int, layers_path: str, text_batches, tracer_kwargs: dict):
    """
    Yield (pooled_acts, true_labels, spurious_labels) for each batch.

    Activations are mean-pooled over token positions using the attention mask,
    matching the approach in experiments/bib_shift_sae.ipynb.

    Args:
        layers_path: dotted path to the layer list on the model,
                     e.g. "model.model.layers" (Gemma/Llama)
                       or "model.gpt_neox.layers" (Pythia)
    """
    layers = resolve_attr_path(model, layers_path)
    with tqdm(total=len(text_batches), desc="Collecting activations") as pbar:
        for text_batch, *labels in text_batches:
            with model.trace(text_batch, **tracer_kwargs):
                attn_mask = model.inputs[1]["attention_mask"]
                acts = layers[layer].output[0]
                pooled = pool_acts(acts, attn_mask).save()
            yield (pooled.value if hasattr(pooled, "value") else pooled), *labels
            pbar.update(1)


# ---------------------------------------------------------------------------
# Probe training and evaluation
# ---------------------------------------------------------------------------

def train_probe(
    activation_batches,
    d_probe: int,
    dtype: t.dtype = t.bfloat16,
    device: str = "cuda:0",
    label_idx: int = 0,
    lr: float = 1e-2,
    epochs: int = 1,
    seed: int = 42,
):
    t.manual_seed(seed)
    probe = Probe(d_probe, dtype=dtype).to(device)
    optimizer = t.optim.AdamW(probe.parameters(), lr=lr)
    criterion = nn.BCEWithLogitsLoss()
    losses = []

    for _ in range(epochs):
        for act, *labels in activation_batches:
            optimizer.zero_grad()
            logits = probe(act)
            loss = criterion(logits, labels[label_idx].to(logits))
            loss.backward()
            optimizer.step()
            losses.append(loss.item())

    return probe, losses


@t.no_grad()
def test_probe(probe: Probe, activation_batches):
    """
    Evaluate probe accuracy per label index.

    Returns:
        {0: true_label_accuracy, 1: spurious_label_accuracy}
    """
    corrects = defaultdict(list)
    for acts, *labels in activation_batches:
        logits = probe(acts)
        preds = (logits > 0.0).long()
        for idx, label in enumerate(labels):
            corrects[idx].append(preds == label)
    return {idx: t.cat(vals).float().mean().item() for idx, vals in corrects.items()}


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def dtype_from_str(s: str) -> t.dtype:
    options = {"bfloat16": t.bfloat16, "float16": t.float16, "float32": t.float32}
    if s not in options:
        raise ValueError(f"Unsupported dtype {s!r}. Choose from: {list(options)}")
    return options[s]


def save_probe(probe: Probe, path: str, activation_dim: int, dtype_str: str):
    """Save probe as state_dict + metadata. Portable across class locations."""
    t.save({"state_dict": probe.state_dict(), "activation_dim": activation_dim, "dtype": dtype_str}, path)


def load_probe(path: str, device: str) -> Probe:
    """Load a probe saved by save_probe()."""
    checkpoint = t.load(path, weights_only=True)
    probe = Probe(checkpoint["activation_dim"], dtype=dtype_from_str(checkpoint["dtype"]))
    probe.load_state_dict(checkpoint["state_dict"])
    return probe.to(device)


def build_adapter(cfg: dict) -> DatasetAdapter:
    adapter_cfg = cfg["adapter"]
    adapter_type = adapter_cfg["type"]
    kwargs = {k: v for k, v in adapter_cfg.items() if k != "type"}

    if adapter_type == "bias_in_bios":
        return BiasInBiosAdapter(**kwargs)
    elif adapter_type == "generic_hf":
        return GenericHFAdapter(**kwargs)
    elif adapter_type == "multinli":
        return MultiNLIAdapter(**kwargs)
    elif adapter_type == "civil_comments":
        return CivilCommentsAdapter(**kwargs)
    else:
        raise ValueError(
            f"Unknown adapter type {adapter_type!r}. "
            "Options: bias_in_bios, civil_comments, generic_hf, multinli"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Train biased and unbiased linear probes")
    parser.add_argument("--config",     required=True,        help="Path to YAML config file")
    parser.add_argument("--layer",      type=int,             help="Override layer from config")
    parser.add_argument("--device",     type=str,             help="Override device (e.g. cuda:0)")
    parser.add_argument("--output-dir", default="probes", type=str, dest="output_dir", help="Override output directory")
    parser.add_argument("--overwrite",  action="store_true",  help="Re-train even if output files exist")
    args = parser.parse_args()

    cfg = load_config(args.config)

    layer      = args.layer      if args.layer      is not None else cfg["layer"]
    device     = args.device     if args.device     is not None else cfg.get("device", "cuda:0")
    output_dir = args.output_dir if args.output_dir is not None else cfg.get("output_dir", "probes")

    os.makedirs(output_dir, exist_ok=True)

    dtype_str   = cfg.get("dtype", "bfloat16")
    dtype       = dtype_from_str(dtype_str)
    batch_size  = cfg.get("batch_size", 32)
    seed        = cfg.get("seed", 42)
    task_name   = cfg["task_name"]
    layers_path = cfg["layers_path"]
    model_name  = cfg["model_name"]
    model_kwargs = cfg.get("model_kwargs", {})
    lr          = cfg.get("lr", 1e-2)
    epochs      = cfg.get("epochs", 1)
    max_samples = cfg.get("max_samples", None)  # None = no limit

    tracer_kwargs = dict(scan=False, validate=False)

    # Output paths follow the same convention as experiments/:
    #   probe_layer_22_bfloat16.pt  /  probe_layer_22_bfloat16_unbiased.pt
    biased_path   = os.path.join(output_dir, f"{task_name}_layer{layer}_{dtype_str}.pt")
    unbiased_path = os.path.join(output_dir, f"{task_name}_layer{layer}_{dtype_str}_unbiased.pt")

    need_biased   = args.overwrite or not os.path.exists(biased_path)
    need_unbiased = args.overwrite or not os.path.exists(unbiased_path)

    # Build adapter (loads dataset)
    print(f"Loading dataset via adapter: {cfg['adapter']['type']}")
    adapter = build_adapter(cfg)
    activation_dim = adapter.activation_dim

    # Load model (only needed if we have to train or evaluate)
    print(f"Loading model {model_name!r} → {device} [{dtype_str}]")
    model = LanguageModel(
        model_name,
        device_map=device,
        dispatch=True,
        torch_dtype=dtype,
        **model_kwargs,
    )

    # -----------------------------------------------------------------------
    # Biased probe  (ambiguous = correlated split)
    # -----------------------------------------------------------------------
    if need_biased:
        print(f"\n--- Training biased probe (ambiguous split) ---")
        train_batches = adapter.get_batches(
            split="train", ambiguous=True, batch_size=batch_size, seed=seed, device=device
        )
        if max_samples is not None:
            train_batches = train_batches[:max_samples // batch_size]
        biased_probe, _ = train_probe(
            activation_batches=collect_activations(
                model, layer, layers_path, train_batches, tracer_kwargs
            ),
            d_probe=activation_dim,
            dtype=dtype,
            device=device,
            label_idx=0,
            lr=lr,
            epochs=epochs,
            seed=seed,
        )
        save_probe(biased_probe, biased_path, activation_dim, dtype_str)
        print(f"Saved → {biased_path}")
    else:
        print(f"\nBiased probe already exists, loading: {biased_path}")
        biased_probe = load_probe(biased_path, device)

    # -----------------------------------------------------------------------
    # Unbiased probe  (balanced = all four quadrants)
    # -----------------------------------------------------------------------
    if need_unbiased:
        print(f"\n--- Training unbiased probe (balanced split) ---")
        train_batches = adapter.get_batches(
            split="train", ambiguous=False, batch_size=batch_size, seed=seed, device=device
        )
        if max_samples is not None:
            train_batches = train_batches[:max_samples // batch_size]
        unbiased_probe, _ = train_probe(
            activation_batches=collect_activations(
                model, layer, layers_path, train_batches, tracer_kwargs
            ),
            d_probe=activation_dim,
            dtype=dtype,
            device=device,
            label_idx=0,
            lr=lr,
            epochs=epochs,
            seed=seed,
        )
        save_probe(unbiased_probe, unbiased_path, activation_dim, dtype_str)
        print(f"Saved → {unbiased_path}")
    else:
        print(f"\nUnbiased probe already exists, loading: {unbiased_path}")
        unbiased_probe = load_probe(unbiased_path, device)

    # -----------------------------------------------------------------------
    # Evaluation
    # -----------------------------------------------------------------------
    print("\n--- Evaluation ---")

    for probe_name, probe in [
        ("Biased (ambiguous train)", biased_probe),
        ("Unbiased (balanced train)", unbiased_probe),
    ]:
        print(f"\n{probe_name}:")

        amb_batches = adapter.get_batches(
            split="test", ambiguous=True, batch_size=batch_size, seed=seed, device=device
        )
        amb_accs = test_probe(
            probe,
            collect_activations(model, layer, layers_path, amb_batches, tracer_kwargs),
        )
        print(f"  ambiguous test acc:     {amb_accs[0]:.4f}")

        bal_batches = adapter.get_batches(
            split="test", ambiguous=False, batch_size=batch_size, seed=seed, device=device
        )
        bal_accs = test_probe(
            probe,
            collect_activations(model, layer, layers_path, bal_batches, tracer_kwargs),
        )
        print(f"  true label acc:         {bal_accs[0]:.4f}")
        print(f"  spurious label acc:     {bal_accs[1]:.4f}")

    print("\nDone.")
    print(f"  Biased probe:   {biased_path}")
    print(f"  Unbiased probe: {unbiased_path}")


if __name__ == "__main__":
    main()
