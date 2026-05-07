"""Generate baseline + directional-ablation completions for the locked
eval prompts using the Arditi-style refusal direction extracted by
extract_direction.py.

Run on the remote VM:

    # All 10 locked eval prompts:
    python -m baselines.arditi.apply_direction

    # Subset (space-separated, matching scripts/run_all.py convention):
    python -m baselines.arditi.apply_direction --slugs tiananmen-massacre airport-bomb-smuggling
"""

from __future__ import annotations

import argparse
import json
import os
from glob import glob

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEIGHTS_DIR = os.path.join(REPO_ROOT, "weights", "arditi", "refusal")
RUNS_DIR = os.path.join(REPO_ROOT, "baselines", "arditi", "runs", "refusal")
LOCKED_PROMPTS_PATH = os.path.join(REPO_ROOT, "data", "prompts.json")


def format_user_only(tokenizer, system_prompt: str, user_message: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def project_out(acts: torch.Tensor, r_hat: torch.Tensor) -> torch.Tensor:
    coeff = (acts * r_hat).sum(dim=-1, keepdim=True)
    return acts - coeff * r_hat


def make_ablation_hook(r_hat: torch.Tensor):
    # TransformerLens calls forward hooks as `hook(activation, hook=HookPoint)`
    # — the second arg is a kwarg named `hook`. Use **kwargs to accept it.
    def hook(acts, **kwargs):
        return project_out(acts, r_hat.to(acts.device, dtype=acts.dtype))
    return hook


def all_ablation_hooks(model, r_hat: torch.Tensor) -> list:
    hooks = []
    fn = make_ablation_hook(r_hat)
    for l in range(model.cfg.n_layers):
        for name in (f"blocks.{l}.hook_resid_pre",
                     f"blocks.{l}.hook_attn_out",
                     f"blocks.{l}.hook_mlp_out"):
            hooks.append((name, fn))
    return hooks


def generate_completion(model, prompt: str, max_new_tokens: int, hooks: list | None) -> str:
    """Greedy generation. If hooks=None, runs baseline; otherwise applies the hooks
    for the entire generate() call (TL's `model.hooks` context manager covers all
    autoregressive decode steps inside generate())."""
    input_ids = model.tokenizer(prompt, return_tensors="pt")["input_ids"].to(model.cfg.device)
    prompt_len = input_ids.shape[1]
    # use_past_kv_cache=False matches circuit_oracle.graph_compute.generate_response —
    # avoids the Qwen3-4B GQA + RoPE + bf16 dtype mismatch and dodges any
    # double-application of hooks during cached decode.
    kwargs = dict(
        max_new_tokens=max_new_tokens,
        stop_at_eos=True,
        do_sample=False,  # deliberately greedy for baseline-vs-ablated comparability
        use_past_kv_cache=False,
    )
    if hooks:
        with model.hooks(fwd_hooks=hooks):
            out = model.generate(input_ids, **kwargs)
    else:
        out = model.generate(input_ids, **kwargs)
    new_ids = out[0, prompt_len:]
    return model.tokenizer.decode(new_ids, skip_special_tokens=True)


def find_direction_path() -> str:
    """Locate the most recently *modified* r_layer*_pos*.pt under WEIGHTS_DIR.

    Sort by mtime, not lex order — `r_layer10_pos-1.pt` lex-sorts before
    `r_layer9_pos-1.pt` and would silently win.
    """
    candidates = glob(os.path.join(WEIGHTS_DIR, "r_layer*_pos*.pt"))
    if not candidates:
        raise FileNotFoundError(
            f"no direction tensor under {WEIGHTS_DIR}; run extract_direction.py first"
        )
    return max(candidates, key=os.path.getmtime)


def parse_layer_pos_from_path(path: str) -> tuple[int, int]:
    """Extract (layer, pos) from a path like '.../r_layer22_pos-1.pt'."""
    name = os.path.basename(path)
    # name like r_layer22_pos-1.pt
    stem = name[:-3] if name.endswith(".pt") else name  # r_layer22_pos-1
    parts = stem.split("_")
    layer = int(parts[1].removeprefix("layer"))
    pos = int(parts[2].removeprefix("pos"))
    return layer, pos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs", nargs="*", default=None,
                    help="space-separated slugs; omit to run all 10 locked eval prompts")
    ap.add_argument("--max-new-tokens", type=int, default=800,
                    help="match the main interventional pipeline's 800-token cap "
                         "(circuit_oracle/tools.py:508/573/685) for fair head-to-head")
    ap.add_argument("--model-name", default="Qwen/Qwen3-4B")
    ap.add_argument("--direction", default=None,
                    help="path to direction .pt; default = mtime-newest under weights/arditi/refusal/")
    args = ap.parse_args()

    from transformer_lens import HookedTransformer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs(RUNS_DIR, exist_ok=True)

    with open(LOCKED_PROMPTS_PATH) as f:
        entries = json.load(f)["entries"]
    if args.slugs:
        wanted = set(args.slugs)
        kept = [e for e in entries if e["slug"] in wanted]
        missing = wanted - {e["slug"] for e in kept}
        if missing:
            available = sorted(e["slug"] for e in entries)
            raise SystemExit(
                f"ERROR: unknown slugs {sorted(missing)}. "
                f"Available: {available}"
            )
        entries = kept
    print(f"Will process {len(entries)} slug(s)")

    direction_path = args.direction or find_direction_path()
    layer, pos = parse_layer_pos_from_path(direction_path)
    r = torch.load(direction_path, map_location="cpu", weights_only=True).to(torch.float32)
    r_hat = (r / (r.norm() + 1e-8)).to(device)
    print(f"Loaded direction (layer={layer}, pos={pos}, norm={r.norm():.3f}) from {direction_path}")

    print(f"Loading {args.model_name}...")
    model = HookedTransformer.from_pretrained(
        args.model_name,
        fold_ln=False,
        center_writing_weights=False,
        center_unembed=False,
        dtype=torch.bfloat16,
        device=device,
    )

    # Pre-flight: create per-slug dirs before model load failure modes are
    # buried by per-prompt mkdir errors.
    for entry in entries:
        os.makedirs(os.path.join(RUNS_DIR, entry["slug"]), exist_ok=True)

    hooks = all_ablation_hooks(model, r_hat)

    for entry in entries:
        slug = entry["slug"]
        prompt = format_user_only(model.tokenizer, entry["system_prompt"], entry["user_message"])
        out_dir = os.path.join(RUNS_DIR, slug)

        print(f"\n--- {slug} ---")
        baseline = generate_completion(model, prompt, args.max_new_tokens, hooks=None)
        print(f"baseline: {baseline[:200]!r}")
        ablated = generate_completion(model, prompt, args.max_new_tokens, hooks=hooks)
        print(f"ablated:  {ablated[:200]!r}")

        with open(os.path.join(out_dir, "baseline.txt"), "w") as f:
            f.write(baseline)
        with open(os.path.join(out_dir, "ablated.txt"), "w") as f:
            f.write(ablated)
        with open(os.path.join(out_dir, "meta.json"), "w") as f:
            json.dump({
                "slug": slug,
                "user_message": entry["user_message"],
                "system_prompt": entry["system_prompt"],
                "model_name": args.model_name,
                "direction_path": direction_path,
                "direction_layer": layer,
                "direction_pos": pos,
                "max_new_tokens": args.max_new_tokens,
            }, f, indent=2)

    print(f"\nWrote {len(entries)} run(s) to {RUNS_DIR}")


if __name__ == "__main__":
    main()
