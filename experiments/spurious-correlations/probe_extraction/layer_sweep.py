#!/usr/bin/env python3
"""
Two-phase layer selection for biased probes.

Phase 1 (ambiguous): Train a biased probe at every layer and evaluate on the
    ambiguous test set.  Saves results to a JSON file.

Phase 2 (select): Read the phase-1 JSON, filter layers above a threshold on
    both accuracies, then re-sweep only those layers on the *balanced* test set.
    The layer with the worst combined (true + spurious) balanced accuracy is
    selected — it generalises worst to balanced data, meaning it relies most on
    the spurious correlation.

Usage:
    # Phase 1 — sweep ambiguous set (saves JSON automatically)
    python layer_sweep.py ambiguous --config configs/multinli_gemma2_2b.yaml
    python layer_sweep.py ambiguous --config configs/multinli_gemma2_2b.yaml --start 10 --end 26

    # Phase 2 — select layer from phase-1 results (no GPU needed for filtering,
    #           but loads model to evaluate on balanced set)
    python layer_sweep.py select --config configs/multinli_gemma2_2b.yaml --phase1-json configs/layer_sweep_multinli_gemma2_2b.json --threshold 0.90
    python layer_sweep.py select --config configs/civil_comments_gemma2_2b.yaml --phase1-json configs/layer_sweep_civil_comments_gemma2_2b.json --threshold 0.86
"""

from __future__ import annotations
import os
import argparse
import json
import sys
from pathlib import Path

import torch as t
from nnsight import LanguageModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from probe_extraction.train_probes import (
    collect_activations,
    train_probe,
    test_probe,
    load_config,
    dtype_from_str,
    build_adapter,
    resolve_attr_path,
)
from probe_extraction.probe_model import Probe


def phase_ambiguous(args):
    """Phase 1: sweep layers on the ambiguous test set."""
    cfg = load_config(args.config)

    device      = args.device or cfg.get("device", "cuda:0")
    dtype_str   = cfg.get("dtype", "bfloat16")
    dtype       = dtype_from_str(dtype_str)
    batch_size  = cfg.get("batch_size", 32)
    seed        = cfg.get("seed", 42)
    layers_path = cfg["layers_path"]
    model_name  = cfg["model_name"]
    model_kwargs = cfg.get("model_kwargs", {})
    lr          = cfg.get("lr", 1e-2)
    epochs      = cfg.get("epochs", 1)
    max_samples = cfg.get("max_samples", None)

    tracer_kwargs = dict(scan=False, validate=False)

    # Load dataset
    print(f"Loading dataset via adapter: {cfg['adapter']['type']}")
    adapter = build_adapter(cfg)
    activation_dim = adapter.activation_dim

    # Load model
    print(f"Loading model {model_name!r} → {device} [{dtype_str}]")
    model = LanguageModel(
        model_name,
        device_map=device,
        dispatch=True,
        torch_dtype=dtype,
        **model_kwargs,
    )

    # Determine layer count
    layers = resolve_attr_path(model, layers_path)
    n_layers = len(layers)
    start = args.start
    end = args.end if args.end is not None else n_layers
    end = min(end, n_layers)
    print(f"Model has {n_layers} layers. Sweeping layers [{start}, {end}).\n")

    def get_train_batches():
        batches = adapter.get_batches(
            split="train", ambiguous=True, batch_size=batch_size, seed=seed, device=device
        )
        if max_samples is not None:
            batches = batches[:max_samples // batch_size]
        return batches

    def get_test_batches():
        return adapter.get_batches(
            split="test", ambiguous=True, batch_size=batch_size, seed=seed, device=device
        )

    results = []

    for layer in range(start, end):
        print(f"=== Layer {layer} ===")

        if os.path.exists(f"tmp_probes/{cfg['task_name']}_layer{layer}_{dtype_str}.pt"):
            checkpoint = t.load(f"tmp_probes/{cfg['task_name']}_layer{layer}_{dtype_str}.pt", weights_only=True)
            probe = Probe(checkpoint["activation_dim"], dtype=dtype_from_str(checkpoint["dtype"]))
            probe.load_state_dict(checkpoint["state_dict"])
            probe = probe.to(device)
        else:
            train_batches = get_train_batches()
            probe, losses = train_probe(
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
            t.save({"state_dict": probe.state_dict(), "activation_dim": activation_dim, "dtype": dtype_str}, 
                f"tmp_probes/{cfg['task_name']}_layer{layer}_{dtype_str}.pt")
        
        test_batches = get_test_batches()
        accs = test_probe(
            probe,
            collect_activations(model, layer, layers_path, test_batches, tracer_kwargs),
        )
        true_acc = accs[0]
        spurious_acc = accs.get(1, float("nan"))
        results.append((layer, true_acc, spurious_acc))
        
        print(f"  ambiguous test — true_label acc: {true_acc:.4f}, spurious_label acc: {spurious_acc:.4f}\n")

    # Summary table
    print("\n" + "=" * 60)
    print(f"{'Layer':>5}  {'Amb. Test Acc (true)':>20}  {'Amb. Test Acc (spur.)':>21}")
    print("-" * 60)
    for layer, true_acc, spurious_acc in results:
        print(f"{layer:>5}  {true_acc:>20.4f}  {spurious_acc:>21.4f}")
    print("=" * 60)

    best_layer, best_acc, _ = max(results, key=lambda x: x[1])
    print(f"\nBest layer by ambiguous test accuracy: {best_layer} (acc = {best_acc:.4f})")

    # Save results to JSON
    config_name = Path(args.config).stem
    out_path = Path(args.config).parent / f"layer_sweep_{config_name}.json"
    json_results = {
        "config": args.config,
        "best_layer": best_layer,
        "best_accuracy": best_acc,
        "layers": {
            layer: {"true_label_acc": true_acc, "spurious_label_acc": spurious_acc}
            for layer, true_acc, spurious_acc in results
        },
    }
    out_path.write_text(json.dumps(json_results, indent=2))
    print(f"Results saved to {out_path}")


def phase_select(args):
    """Phase 2: filter by threshold, re-sweep candidates on balanced set, pick worst."""
    # Load phase-1 results
    with open(args.phase1_json) as f:
        phase1 = json.load(f)

    threshold = args.threshold
    candidates = []
    for layer_str, accs in phase1["layers"].items():
        if accs["true_label_acc"] >= threshold and accs["spurious_label_acc"] >= threshold:
            candidates.append(int(layer_str))
    candidates.sort()

    print(f"Phase-1 threshold: {threshold}")
    print(f"Candidate layers (both accs >= {threshold}): {candidates}")

    if not candidates:
        print("No layers passed the threshold. Try lowering --threshold.")
        return

    if len(candidates) == 1:
        print(f"\nOnly one candidate — selected layer {candidates[0]}")
        _save_selection(args, phase1, candidates[0], balanced_results={})
        return

    # Need to sweep candidates on balanced set
    cfg = load_config(args.config)

    device      = args.device or cfg.get("device", "cuda:0")
    dtype_str   = cfg.get("dtype", "bfloat16")
    dtype       = dtype_from_str(dtype_str)
    batch_size  = cfg.get("batch_size", 32)
    seed        = cfg.get("seed", 42)
    layers_path = cfg["layers_path"]
    model_name  = cfg["model_name"]
    model_kwargs = cfg.get("model_kwargs", {})
    lr          = cfg.get("lr", 1e-2)
    epochs      = cfg.get("epochs", 1)
    max_samples = cfg.get("max_samples", None)

    tracer_kwargs = dict(scan=False, validate=False)

    print(f"\nLoading dataset via adapter: {cfg['adapter']['type']}")
    adapter = build_adapter(cfg)
    activation_dim = adapter.activation_dim

    print(f"Loading model {model_name!r} → {device} [{dtype_str}]")
    model = LanguageModel(
        model_name,
        device_map=device,
        dispatch=True,
        torch_dtype=dtype,
        **model_kwargs,
    )

    def get_train_batches():
        batches = adapter.get_batches(
            split="train", ambiguous=True, batch_size=batch_size, seed=seed, device=device
        )
        if max_samples is not None:
            batches = batches[:max_samples // batch_size]
        return batches

    def get_balanced_test_batches():
        return adapter.get_batches(
            split="test", ambiguous=False, batch_size=batch_size, seed=seed, device=device
        )

    balanced_results = {}

    for layer in candidates:
        print(f"\n=== Layer {layer} (balanced eval) ===")

        # Re-train biased probe at this layer
        # train_batches = get_train_batches()
        # probe, _ = train_probe(
        #     activation_batches=collect_activations(
        #         model, layer, layers_path, train_batches, tracer_kwargs
        #     ),
        #     d_probe=activation_dim,
        #     dtype=dtype,
        #     device=device,
        #     label_idx=0,
        #     lr=lr,
        #     epochs=epochs,
        #     seed=seed,
        # )
        checkpoint = t.load(f"tmp_probes/{cfg['task_name']}_layer{layer}_{dtype_str}.pt", weights_only=True)
        probe = Probe(checkpoint["activation_dim"], dtype=dtype_from_str(checkpoint["dtype"]))
        probe.load_state_dict(checkpoint["state_dict"])
        probe = probe.to(device)

        # Evaluate on balanced test set
        bal_batches = get_balanced_test_batches()
        accs = test_probe(
            probe,
            collect_activations(model, layer, layers_path, bal_batches, tracer_kwargs),
        )
        true_acc = accs[0]
        spurious_acc = accs.get(1, float("nan"))
        balanced_results[layer] = {"true_label_acc": true_acc, "spurious_label_acc": spurious_acc}
        print(f"  balanced test — true_label acc: {true_acc:.4f}, spurious_label acc: {spurious_acc:.4f}")

    # Summary table
    print("\n" + "=" * 60)
    print(f"{'Layer':>5}  {'Bal. Test Acc (true)':>20}  {'Bal. Test Acc (spur.)':>21}  {'Sum':>8}")
    print("-" * 60)
    for layer in candidates:
        r = balanced_results[layer]
        s = r["true_label_acc"] + r["spurious_label_acc"]
        print(f"{layer:>5}  {r['true_label_acc']:>20.4f}  {r['spurious_label_acc']:>21.4f}  {s:>8.4f}")
    print("=" * 60)

    # Pick the layer with the worst combined balanced accuracy
    selected = min(candidates, key=lambda l: balanced_results[l]["true_label_acc"] + balanced_results[l]["spurious_label_acc"])
    sel = balanced_results[selected]
    print(f"\nSelected layer {selected} (worst balanced: true={sel['true_label_acc']:.4f}, spur={sel['spurious_label_acc']:.4f})")

    _save_selection(args, phase1, selected, balanced_results)


def _save_selection(args, phase1, selected_layer, balanced_results):
    """Save phase-2 selection results to JSON next to the phase-1 file."""
    out_path = Path(args.phase1_json).with_name(
        Path(args.phase1_json).stem.replace("layer_sweep", "layer_selection") + ".json"
    )
    result = {
        "config": phase1["config"],
        "threshold": args.threshold,
        "selected_layer": selected_layer,
        "phase1_json": args.phase1_json,
        "balanced_results": {
            str(k): v for k, v in balanced_results.items()
        },
    }
    out_path.write_text(json.dumps(result, indent=2))
    print(f"Selection saved to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Two-phase layer selection for biased probes")
    subparsers = parser.add_subparsers(dest="phase", required=True)

    # Phase 1: ambiguous sweep
    p1 = subparsers.add_parser("ambiguous", help="Phase 1: sweep layers on ambiguous test set")
    p1.add_argument("--config", required=True, help="Path to YAML config file")
    p1.add_argument("--start", type=int, default=0, help="First layer index (inclusive)")
    p1.add_argument("--end", type=int, default=None, help="Last layer index (exclusive)")
    p1.add_argument("--device", type=str, default=None, help="Override device")

    # Phase 2: select from phase-1 results
    p2 = subparsers.add_parser("select", help="Phase 2: select layer using balanced test set")
    p2.add_argument("--config", required=True, help="Path to YAML config file")
    p2.add_argument("--phase1-json", required=True, help="Path to phase-1 JSON output")
    p2.add_argument("--threshold", type=float, default=0.90, help="Min accuracy on both labels (default: 0.90)")
    p2.add_argument("--device", type=str, default=None, help="Override device")

    args = parser.parse_args()

    if args.phase == "ambiguous":
        phase_ambiguous(args)
    elif args.phase == "select":
        phase_select(args)


if __name__ == "__main__":
    main()
