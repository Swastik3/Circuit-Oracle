"""Compute the Arditi-style diff-in-mean refusal direction on Qwen3-4B.

Faithful to Arditi et al. 2024 (arXiv:2406.11717), `andyrdt/refusal_direction`,
specifically `pipeline/submodules/select_direction.py`:

  1. Load Qwen3-4B as a vanilla TransformerLens HookedTransformer (no
     transcoders — diff-in-mean operates on the raw residual stream).
  2. Baseline-behavior filter: drop harmful prompts the model does not refuse,
     drop harmless prompts the model does refuse.
  3. Cache `blocks.{l}.hook_resid_pre` for every layer over the post-instruction
     chat-template suffix (~9 token positions for Qwen3 with enable_thinking=False).
  4. Compute per-(layer, pos) direction r = mean(harmful) - mean(harmless).
  5. Score every (layer, pos) candidate on Arditi's THREE metrics:
       a. ablation_refusal_score — refusal_score on harmful val under ablation
          at every layer (lower = better jailbreak)
       b. kl_harmless — KL(baseline||ablated) on harmless val (filter at 0.1)
       c. steering_refusal_score — refusal_score on harmless val under ADDITION
          of r_hat at the candidate's source layer only, alpha=1.0 (filter > 0)
  6. Two hard filters (KL ≤ threshold AND steering > threshold) then
     argmin(ablation_refusal_score). No weighted sum, no Pareto — exactly
     Arditi's selection logic.
  7. Save the chosen direction + per-candidate scores to weights/arditi/refusal/.

Run on the remote VM:

    python -m baselines.arditi.extract_direction
"""

from __future__ import annotations

import argparse
import json
import os

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, "baselines", "arditi", "data")
WEIGHTS_DIR = os.path.join(REPO_ROOT, "weights", "arditi", "refusal")

# Qwen3-4B refusal first-token candidates. Arditi's `refusal_score`
# (refusal_direction/pipeline/submodules/select_direction.py:17-30) is
# log(P(refusal) / P(not refusal)) — refusal vs. everything-else in the
# softmax distribution, NOT refusal vs. a hand-curated comply set. So we
# only need the refusal token set.
REFUSAL_LEAD_STRINGS = ["I cannot", "I can't", "I won't", "I'm sorry", "Sorry", "As an", "As a"]


def format_user_only(tokenizer, user_message: str) -> str:
    """Same chat-template formatting as circuit_oracle.graph_compute.format_chat
    but inlined here so this script has no circuit_oracle dependency."""
    messages = [
        {"role": "system", "content": ""},
        {"role": "user", "content": user_message},
    ]
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def encode_lead_tokens(tokenizer, strings: list[str]) -> list[int]:
    """First-token IDs for each lead string (with leading-space variant)."""
    ids = set()
    for s in strings:
        for variant in (s, " " + s):
            t = tokenizer(variant, add_special_tokens=False)["input_ids"]
            if t:
                ids.add(t[0])
    return sorted(ids)


def behavior_filter(
    model,
    prompts: list[str],
    refusal_ids: list[int],
    expect_refusal: bool,
) -> tuple[list[str], list[str]]:
    """Drop prompts whose baseline behavior contradicts their label.

    Uses a continuous log-odds threshold (`refusal_score > 0`), matching Arditi's
    `run_pipeline.py:46-53`. A prior version of this function used an argmax-in-
    refusal_ids check, which can disagree with Arditi on borderline prompts and
    shifts which prompts enter the diff-in-mean.

    expect_refusal=True for harmful prompts; expect_refusal=False for harmless.
    Returns (kept, dropped).
    """
    kept, dropped = [], []
    for p in prompts:
        is_refusal = refusal_score(model, p, refusal_ids) > 0.0
        if expect_refusal == is_refusal:
            kept.append(p)
        else:
            dropped.append(p)
    return kept, dropped


def cache_resid_pre(
    model,
    prompts: list[str],
    n_pos: int,
) -> torch.Tensor:
    """Forward-pass each prompt and stack the last n_pos resid_pre activations.

    Returns: [n_prompts, n_layers, n_pos, d_model] on CPU, fp32.
    """
    n_layers = model.cfg.n_layers
    d_model = model.cfg.d_model
    out = torch.zeros(len(prompts), n_layers, n_pos, d_model, dtype=torch.float32)
    hook_names = [f"blocks.{l}.hook_resid_pre" for l in range(n_layers)]

    for i, prompt in enumerate(prompts):
        formatted = format_user_only(model.tokenizer, prompt)
        toks = model.tokenizer(formatted, return_tensors="pt")["input_ids"].to(model.cfg.device)
        with torch.no_grad():
            _, cache = model.run_with_cache(toks, names_filter=hook_names)
        for l, name in enumerate(hook_names):
            acts = cache[name][0, -n_pos:, :].to(torch.float32).cpu()
            out[i, l] = acts
        del cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    return out


def project_out(acts: torch.Tensor, r_hat: torch.Tensor) -> torch.Tensor:
    coeff = (acts * r_hat).sum(dim=-1, keepdim=True)
    return acts - coeff * r_hat


def kl_div(p_logits: torch.Tensor, q_logits: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    """KL(P || Q) at a single token position.

    Matches Arditi's `kl_div_fn` (`select_direction.py`): softmax then log+eps,
    in float64. The eps guards against log(0) when one distribution puts
    near-zero mass on a token the other distribution puts non-trivial mass on.
    """
    p_logits = p_logits.to(torch.float64)
    q_logits = q_logits.to(torch.float64)
    probs_p = torch.softmax(p_logits, dim=-1)
    probs_q = torch.softmax(q_logits, dim=-1)
    return (probs_p * (torch.log(probs_p + eps) - torch.log(probs_q + eps))).sum(dim=-1)


def make_ablation_hook(r_hat: torch.Tensor):
    # TransformerLens calls forward hooks as `hook(activation, hook=HookPoint)`
    # — the second arg is a kwarg named `hook`. Use **kwargs to accept it
    # without colliding with the outer factory function's name.
    def hook(acts, **kwargs):
        return project_out(acts, r_hat.to(acts.device, dtype=acts.dtype))
    return hook


def all_ablation_hooks(model, r_hat: torch.Tensor) -> list[tuple[str, callable]]:
    """Hooks that ablate r_hat at every layer's resid_pre, attn_out, mlp_out.

    Ablation must span every write to the residual stream, so the projection
    is applied 3× per layer (matching Arditi's `get_orthogonalized_matrix`-
    equivalent forward-time setup). See `select_direction.py:~145`.
    """
    hooks = []
    fn = make_ablation_hook(r_hat)
    for l in range(model.cfg.n_layers):
        for name in (f"blocks.{l}.hook_resid_pre",
                     f"blocks.{l}.hook_attn_out",
                     f"blocks.{l}.hook_mlp_out"):
            hooks.append((name, fn))
    return hooks


def make_steering_hook(r_hat: torch.Tensor, coeff: float = 1.0):
    """ADD coeff * r_hat to activations at one hook point.

    Used for Arditi's induce-refusal / steering metric: when we add the
    candidate refusal direction to a HARMLESS prompt, does the model start
    to refuse? Asymmetric with ablation: steering fires at ONE layer only
    (the candidate's source layer), alpha hardcoded to 1.0 — matching
    Arditi's `select_direction.py:~205-220`.
    """
    def hook(acts, **kwargs):
        return acts + coeff * r_hat.to(acts.device, dtype=acts.dtype)
    return hook


def refusal_score(model, prompt: str, refusal_ids: list[int], epsilon: float = 1e-8) -> float:
    """log(P(refusal_first_token)) - log(1 - P(refusal_first_token)).

    Mirror of Arditi's `refusal_score` (`select_direction.py:17-30`): log-odds of
    "refusal vs. everything else" computed on softmax probabilities at the
    next-token position. Higher = model leans more toward refusing; lower =
    model leans toward producing a non-refusal continuation.

    NOT log-odds against a hand-curated comply set — we tried that earlier and
    it diverged from Arditi's metric (a curated comply set under-counts the
    fluent-comply mass which can spread across many opening tokens).
    """
    formatted = format_user_only(model.tokenizer, prompt)
    toks = model.tokenizer(formatted, return_tensors="pt")["input_ids"].to(model.cfg.device)
    with torch.no_grad():
        logits = model(toks)
    # float64 to match Arditi's `select_direction.py:22` precision.
    last = logits[0, -1, :].to(torch.float64)
    probs = torch.softmax(last, dim=-1)
    refusal_p = probs[refusal_ids].sum()
    nonrefusal_p = 1.0 - refusal_p
    return float((torch.log(refusal_p + epsilon) - torch.log(nonrefusal_p + epsilon)).item())


def score_candidate(
    model,
    layer: int,
    pos: int,
    r: torch.Tensor,
    val_pos_prompts: list[str],
    val_neg_prompts: list[str],
    refusal_ids: list[int],
    cached_baseline_refusal: list[float],
    cached_baseline_neg_logits: list[torch.Tensor],
) -> dict:
    """Score one (layer, pos) candidate on Arditi's three metrics.

    Three metrics, all computed on the held-out val splits:
      1. ablation_refusal_score — mean refusal_score on harmful val UNDER ablation
         (lower = better jailbreak).
      2. kl_harmless — KL(baseline || ablated) on harmless val (higher = more
         collateral damage on innocuous prompts).
      3. steering_refusal_score — mean refusal_score on harmless val UNDER ADDITION
         of r_hat at the candidate's source layer only (higher = the direction
         actually induces refusal when we steer harmless inputs into it).

    The caller passes precomputed baselines so we don't recompute them per
    candidate (28 layers × 9 positions = 252 candidates × ~25 val prompts).
    """
    r_hat = r / (r.norm() + 1e-8)
    abl_hooks = all_ablation_hooks(model, r_hat)

    # Metric 1: refusal score under ablation, on harmful val.
    refusal_ablated = []
    with model.hooks(fwd_hooks=abl_hooks):
        for p in val_pos_prompts:
            refusal_ablated.append(refusal_score(model, p, refusal_ids))

    # Metric 2: KL on harmless val (baseline vs ablated).
    kl_vals = []
    with model.hooks(fwd_hooks=abl_hooks):
        for p, base_logits in zip(val_neg_prompts, cached_baseline_neg_logits):
            formatted = format_user_only(model.tokenizer, p)
            toks = model.tokenizer(formatted, return_tensors="pt")["input_ids"].to(model.cfg.device)
            with torch.no_grad():
                abl_logits = model(toks)[0, -1, :]
            kl_vals.append(float(kl_div(base_logits, abl_logits).item()))

    # Metric 3: induce-refusal steering on harmless val. Add the RAW
    # mean-diff vector r (NOT r_hat) at the candidate's source layer's
    # resid_pre only, coeff=1.0. The paper (eq. 3) and code (hook_utils.py
    # `get_activation_addition_input_pre_hook` does no internal normalization)
    # both use raw r. The natural ‖r‖ encodes the calibrated harmful-harmless
    # mean distance — using r_hat would dilute the steering perturbation
    # by ‖r‖ and silently shift which candidates pass the steering filter.
    # Asymmetric with ablation (which uses r_hat at every layer); the
    # asymmetry is intentional, since projection needs a unit vector but
    # displacement does not.
    steer_hook_point = f"blocks.{layer}.hook_resid_pre"
    steer_hook = make_steering_hook(r, coeff=1.0)
    refusal_steered = []
    with model.hooks(fwd_hooks=[(steer_hook_point, steer_hook)]):
        for p in val_neg_prompts:
            refusal_steered.append(refusal_score(model, p, refusal_ids))

    refusal_baseline_mean = sum(cached_baseline_refusal) / len(cached_baseline_refusal)
    refusal_ablated_mean = sum(refusal_ablated) / len(refusal_ablated)
    refusal_steered_mean = sum(refusal_steered) / len(refusal_steered)
    return {
        "layer": layer,
        "pos": pos,
        "refusal_baseline": refusal_baseline_mean,
        "ablation_refusal_score": refusal_ablated_mean,
        "refusal_drop": refusal_baseline_mean - refusal_ablated_mean,
        "kl_harmless": sum(kl_vals) / len(kl_vals),
        "steering_refusal_score": refusal_steered_mean,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-pos", dest="n_pos", type=int, default=9,
                    help="number of post-instruction tokens to sweep (default: 9 for Qwen3-4B "
                         "with enable_thinking=False)")
    ap.add_argument("--top-layer-drop-pct", dest="top_layer_drop_pct", type=float, default=0.20)
    ap.add_argument("--kl-threshold", dest="kl_threshold", type=float, default=0.1,
                    help="filter out candidates with KL(baseline||ablated) > threshold on "
                         "harmless val (Arditi default 0.1)")
    ap.add_argument("--induce-refusal-threshold", dest="induce_refusal_threshold",
                    type=float, default=0.0,
                    help="filter out candidates whose steering_refusal_score on harmless val "
                         "is below threshold — i.e. the direction must INDUCE some refusal "
                         "when added to harmless prompts (Arditi default 0.0)")
    ap.add_argument("--model-name", dest="model_name", default="Qwen/Qwen3-4B")
    args = ap.parse_args()

    from transformer_lens import HookedTransformer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs(WEIGHTS_DIR, exist_ok=True)

    # Arditi-faithful schema: separate train/val pools per side, all 4 filtered
    # independently. n_train and n_val are pre-filter caps from fetch_data.py.
    with open(os.path.join(DATA_DIR, "refusal_train.json")) as f:
        d = json.load(f)
    harmful_train_pool  = d["harmful_train"]
    harmful_val_pool    = d["harmful_val"]
    harmless_train_pool = d["harmless_train"]
    harmless_val_pool   = d["harmless_val"]

    print(f"Loading {args.model_name} into vanilla HookedTransformer...")
    model = HookedTransformer.from_pretrained(
        args.model_name,
        fold_ln=False,
        center_writing_weights=False,
        center_unembed=False,
        dtype=torch.bfloat16,
        device=device,
    )
    n_layers = model.cfg.n_layers
    n_pos = args.n_pos
    print(f"n_layers={n_layers}, d_model={model.cfg.d_model}, n_pos sweep={n_pos}")

    refusal_ids = encode_lead_tokens(model.tokenizer, REFUSAL_LEAD_STRINGS)
    print(f"refusal_ids={refusal_ids}")

    # Filter all four pools independently (matches Arditi's `filter_data`
    # called per-split in `run_pipeline.py:36-51`).
    print("\nBaseline-behavior filter on harmful train pool...")
    harmful_train_kept, harmful_train_drop = behavior_filter(
        model, harmful_train_pool, refusal_ids, expect_refusal=True)
    print(f"  kept {len(harmful_train_kept)} / dropped {len(harmful_train_drop)}")
    print("Baseline-behavior filter on harmless train pool...")
    harmless_train_kept, harmless_train_drop = behavior_filter(
        model, harmless_train_pool, refusal_ids, expect_refusal=False)
    print(f"  kept {len(harmless_train_kept)} / dropped {len(harmless_train_drop)}")
    print("Baseline-behavior filter on harmful val pool...")
    val_pos, harmful_val_drop = behavior_filter(
        model, harmful_val_pool, refusal_ids, expect_refusal=True)
    print(f"  kept {len(val_pos)} / dropped {len(harmful_val_drop)}")
    print("Baseline-behavior filter on harmless val pool...")
    val_neg, harmless_val_drop = behavior_filter(
        model, harmless_val_pool, refusal_ids, expect_refusal=False)
    print(f"  kept {len(val_neg)} / dropped {len(harmless_val_drop)}")

    # Balance train sides by truncating to the smaller kept pool. Val is left
    # at its post-filter natural size (Arditi does not balance val).
    n_train = min(len(harmful_train_kept), len(harmless_train_kept))
    if n_train < 16:
        raise RuntimeError(
            f"only {n_train} balanced train prompts after filtering; need ≥16. "
            f"Check refusal_ids on the Qwen3 tokenizer."
        )
    if not val_pos or not val_neg:
        raise RuntimeError("empty val pool after filtering; aborting")
    train_pos = harmful_train_kept[:n_train]
    train_neg = harmless_train_kept[:n_train]
    print(f"\nTrain: {len(train_pos)} harmful + {len(train_neg)} harmless")
    print(f"Val:   {len(val_pos)} harmful + {len(val_neg)} harmless")

    print("\nCaching resid_pre on train harmful...")
    pos_acts = cache_resid_pre(model, train_pos, n_pos)
    print("Caching resid_pre on train harmless...")
    neg_acts = cache_resid_pre(model, train_neg, n_pos)
    diffs = pos_acts.mean(0) - neg_acts.mean(0)  # [n_layers, n_pos, d_model]
    print(f"diffs shape: {tuple(diffs.shape)}")

    # Cache baselines once — they don't depend on the candidate direction.
    print("\nCaching baseline refusal score on harmful val (no hooks)...")
    cached_baseline_refusal = [refusal_score(model, p, refusal_ids) for p in val_pos]
    print("Caching baseline harmless val logits (for KL)...")
    cached_baseline_neg_logits = []
    for p in val_neg:
        formatted = format_user_only(model.tokenizer, p)
        toks = model.tokenizer(formatted, return_tensors="pt")["input_ids"].to(model.cfg.device)
        with torch.no_grad():
            cached_baseline_neg_logits.append(model(toks)[0, -1, :].clone())

    last_layer_kept = int(n_layers * (1 - args.top_layer_drop_pct))
    print(f"\nSweeping layers [0, {last_layer_kept}) × positions [-{n_pos}, 0):")
    candidates = []
    for layer in range(last_layer_kept):
        for p_idx in range(n_pos):
            pos_offset = p_idx - n_pos  # p_idx=0 → -n_pos (oldest), p_idx=n_pos-1 → -1 (newest)
            r = diffs[layer, p_idx, :]
            score = score_candidate(
                model, layer, pos_offset, r, val_pos, val_neg, refusal_ids,
                cached_baseline_refusal, cached_baseline_neg_logits,
            )
            candidates.append(score)
            kl_ok = score["kl_harmless"] <= args.kl_threshold
            steer_ok = score["steering_refusal_score"] >= args.induce_refusal_threshold
            keep = kl_ok and steer_ok
            print(f"  L{layer:02d} p{pos_offset:+d}: "
                  f"abl_refusal={score['ablation_refusal_score']:+.3f} "
                  f"(drop={score['refusal_drop']:+.3f})  "
                  f"kl={score['kl_harmless']:.4f}  "
                  f"steer={score['steering_refusal_score']:+.3f}  "
                  f"{'KEEP' if keep else 'drop'}")

    # Two hard filters then argmin(ablation_refusal_score) — exactly Arditi's
    # `select_direction` logic (no weighted sum, no Pareto).
    survivors = [
        c for c in candidates
        if c["kl_harmless"] <= args.kl_threshold
        and c["steering_refusal_score"] >= args.induce_refusal_threshold
    ]
    if not survivors:
        raise RuntimeError(
            f"no candidate survived filters (KL≤{args.kl_threshold}, "
            f"steering>{args.induce_refusal_threshold}). "
            f"Loosen --kl-threshold or --induce-refusal-threshold."
        )

    # argmin(ablation_refusal_score) ≡ argmax(refusal_drop) since baseline is constant.
    best = min(survivors, key=lambda c: c["ablation_refusal_score"])
    print(f"\nBest: L{best['layer']} pos={best['pos']:+d} "
          f"(abl_refusal={best['ablation_refusal_score']:+.3f}, "
          f"drop={best['refusal_drop']:+.3f}, "
          f"kl={best['kl_harmless']:.4f}, "
          f"steer={best['steering_refusal_score']:+.3f})")

    p_idx = best["pos"] + n_pos
    chosen = diffs[best["layer"], p_idx, :].clone()
    out_path = os.path.join(WEIGHTS_DIR, f"r_layer{best['layer']}_pos{best['pos']}.pt")
    torch.save(chosen, out_path)
    summary_path = os.path.join(WEIGHTS_DIR, "summary.json")
    with open(summary_path, "w") as f:
        json.dump({
            "model_name": args.model_name,
            "chosen_layer": best["layer"],
            "chosen_pos": best["pos"],
            "n_train": len(train_pos),
            "n_val": len(val_pos),
            "n_pos_sweep": n_pos,
            "kl_threshold": args.kl_threshold,
            "induce_refusal_threshold": args.induce_refusal_threshold,
            "top_layer_drop_pct": args.top_layer_drop_pct,
            "refusal_lead_strings": REFUSAL_LEAD_STRINGS,
            "candidates": candidates,
            "best": best,
            "direction_path": out_path,
            "behavior_filter": {
                "harmful_train_kept":   len(harmful_train_kept),
                "harmful_train_dropped":  len(harmful_train_drop),
                "harmless_train_kept":  len(harmless_train_kept),
                "harmless_train_dropped": len(harmless_train_drop),
                "harmful_val_kept":     len(val_pos),
                "harmful_val_dropped":    len(harmful_val_drop),
                "harmless_val_kept":    len(val_neg),
                "harmless_val_dropped":   len(harmless_val_drop),
            },
        }, f, indent=2)
    print(f"Saved direction to {out_path}")
    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()
