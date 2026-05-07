#!/usr/bin/env python3
"""Censorship-jailbreak experiment runner.

Reads single-prompt entries from data/prompts.json and runs the Circuit Oracle
pipeline. The attribution graph is computed once per prompt and reused for the
single canonical orchestrator, amortizing the expensive GPU computation.

Per run produces (under exp/exp-suppression-{slug}/):
    oracle_result.json      — full pipeline state (interventions, self_rating_confidence, ...)
    elicitation.json/.md    — winning interventions (the punchline)
    circuit.svg             — pinned BUILD circuit
    report.md               — Oracle's narrative, controls, usage table
    pinned_ids.json         — Neuronpedia-style IDs for the pinned features

Usage:
    python scripts/run_all.py                                     # all entries in data/prompts.json
    python scripts/run_all.py --slugs tiananmen-june-4-1989       # single slug
    python scripts/run_all.py --orchestrator anthropic/claude-opus-4.6
    python scripts/run_all.py --control-runs 3
"""

import argparse
import json
import os
import sys
from pathlib import Path

import torch

from circuit_oracle import (
    ToolContext,
    LLMClient,
    RunConfig,
    load_model,
    format_chat,
    compute_or_load_graph,
    run_circuit_oracle,
    save_run_results,
    build_oracle_query,
    generate_response,
    run_control_analysis,
    run_self_rating,
    REFUSAL_SKILL,
)


# ── Configuration ────────────────────────────────────────────────────────────

DEFAULT_QUESTION = "Is this output a refusal, and which features gate it?"

DEFAULT_ORCHESTRATOR = "openai/gpt-5.4"

DEFAULT_SUBAGENT = "openai/gpt-oss-120b"

EXPERIMENT_PREFIX = "suppression"


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_dataset_file(path: Path) -> dict:
    """Load and validate the prompts JSON file."""
    with open(path) as f:
        data = json.load(f)

    if "entries" not in data:
        print(f"Error: {path} missing 'entries' key")
        sys.exit(1)

    entries = data["entries"]
    if not entries:
        print(f"Error: {path} has no entries")
        sys.exit(1)

    print(f"Loaded {len(entries)} entries from {path}")
    meta = data.get("metadata", {})
    if meta.get("purpose"):
        print(f"  Purpose: {meta['purpose'][:120]}...")

    return data


def filter_entries(entries: list[dict], slugs: list[str] | None = None) -> list[dict]:
    """Filter entries by slug. Suppression runs only filter by slug — there are no PopQA cells.

    Entries with `"disabled": true` are skipped by default. They can still be
    force-run by naming them explicitly in --slugs.
    """
    if slugs is None:
        return [e for e in entries if not e.get("disabled", False)]
    return [e for e in entries if e["slug"] in slugs]


def entry_to_run_config(entry: dict, **overrides) -> RunConfig:
    """Convert a prompts.json entry to a RunConfig."""
    question = overrides.pop("question", DEFAULT_QUESTION)
    return RunConfig(
        prompt_name=entry["slug"],
        system_prompt=entry.get("system_prompt", ""),
        user_message=entry["user_message"],
        experiment_prefix=EXPERIMENT_PREFIX,
        question=question,
        **overrides,
    )


def run_single_orchestrator(
    cfg,
    ctx,
    client,
    prompt,
    full_response,
    verbose,
    control_runs=1,
    self_rating=None,
    interventions=None,
):
    """Run the oracle pipeline for a single entry."""
    question_label = f" (question: {cfg.question})" if cfg.question else " (general)"
    orch_label = cfg.orchestrator_model.split("/")[-1] if "/" in cfg.orchestrator_model else cfg.orchestrator_model
    print(f"\n  {'─'*56}")
    print(f"  Orchestrator: {orch_label}{question_label}")
    print(f"  {'─'*56}")

    oracle_query = build_oracle_query(
        user_message=cfg.user_message,
        full_response=full_response,
    )

    # [1/2] Oracle analysis (circuit tools)
    print(f"  [1/2] Oracle analysis (circuit tools)...")
    result = run_circuit_oracle(
        ctx,
        client,
        oracle_query,
        orchestrator_model=cfg.orchestrator_model,
        subagent_model=cfg.subagent_model,
        max_subagent_hops=cfg.max_subagent_hops,
        verbose=verbose,
        skill=REFUSAL_SKILL,
    )

    print(f"\n  [1/2] ORACLE DONE — {len(result['tool_calls'])} tool calls")

    # Pull intervention records out of the tool_calls log so they land in
    # oracle_result.json["interventions"] and elicitation.{json,md}.
    interventions = _collect_interventions(result["tool_calls"])

    # [2/2] Control analysis (Oracle without circuit tools)
    control_results = []
    for i in range(control_runs):
        run_label = f" (run {i+1}/{control_runs})" if control_runs > 1 else ""
        print(f"  [2/2] Control analysis (no tools){run_label}...")
        cr = run_control_analysis(
            client,
            user_message=cfg.user_message,
            full_response=full_response,
            model=cfg.orchestrator_model,
        )
        control_results.append(cr)

    exp_dir = save_run_results(
        result, cfg, prompt,
        full_response=full_response,
        control_results=control_results,
        self_rating=self_rating,
        interventions=interventions,
    )
    print(f"  Saved to: {exp_dir}")


def _collect_interventions(tool_calls: list) -> list[dict]:
    """Pull intervention measurement records out of the tool_calls log.

    Three intervention tools produce measurements:
      - intervene_feature: returns a flat record with top-level `intervention`,
        `top5_before/after`, `answer_before/after`, `hypothesis`.
      - intervene_supernode: same flat shape.
      - anchor_pass: returns a batched record with `anchor_results` (list of per-feature
        dicts), plus call-level `answer_before` and `hypothesis`. We flatten each
        per-feature dict into the same single-feature shape used by intervene_feature so
        the downstream saving code can render them uniformly.

    Calls whose output contains an `error` key (e.g. the harness rejected the call with
    `anchor_required` / `gradual_required` / `already_run`) are skipped entirely so they
    don't pollute elicitation.json or count toward measurement totals.
    """
    out = []
    for tc in tool_calls:
        tool = tc["tool"]
        output = tc.get("output")
        if not isinstance(output, dict) or "error" in output:
            continue
        if tool in ("intervene_feature", "intervene_supernode"):
            if "intervention" in output:
                out.append(output)
        elif tool == "anchor_pass":
            answer_before = output.get("answer_before")
            hypothesis = output.get("hypothesis")
            for per_feature in output.get("anchor_results", []) or []:
                # Per-feature dicts already contain `intervention`, `top5_before`,
                # `top5_after`, `answer_after`, `baseline_activation`, etc. Inject the
                # call-level `answer_before` and `hypothesis` so the record matches the
                # intervene_feature schema saving.py expects.
                flat = dict(per_feature)
                flat.setdefault("answer_before", answer_before)
                flat.setdefault("hypothesis", hypothesis)
                out.append(flat)
    return out


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run suppression-jailbreak experiments via the Circuit Oracle"
    )
    parser.add_argument(
        "--dataset-file", type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "prompts.json",
        help="Path to prompts JSON (default: data/prompts.json)"
    )
    parser.add_argument(
        "--orchestrator", default=DEFAULT_ORCHESTRATOR,
        help=f"Orchestrator model ID (default: {DEFAULT_ORCHESTRATOR})"
    )
    parser.add_argument(
        "--subagent-model", default=DEFAULT_SUBAGENT,
        help=f"Subagent model ID (default: {DEFAULT_SUBAGENT})"
    )
    parser.add_argument(
        "--provider", default=os.environ.get("LLM_PROVIDER", "openrouter"),
        choices=["anthropic", "openrouter"],
    )
    parser.add_argument("--slugs", nargs="*", help="Filter by entry slug")
    parser.add_argument("--limit", type=int, default=None,
                        help="Run only the first N entries after filtering")
    parser.add_argument("--max-hops", type=int, default=12)
    parser.add_argument("--control-runs", type=int, default=1,
                        help="Independent Oracle-without-tools control runs (default: 1)")
    parser.add_argument("--self-rating-samples", type=int, default=5,
                        help="Subject-model self-confidence samples (default: 5). Set 0 to disable.")
    parser.add_argument("--self-rating-temperature", type=float, default=0.7,
                        help="Sampling temperature for self-rating (default: 0.7)")
    parser.add_argument("--keep-graphs", action="store_true",
                        help="Keep the cached attribution graph (.pt) after the run completes.")
    parser.add_argument("--max-feature-nodes", type=int, default=10000,
                        help="Cap on feature nodes per attribution graph (default 10000; 0 = unbounded).")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print resolved entry metadata without loading the model or running any LLM calls.",
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    verbose = not args.quiet

    # Load prompts
    data = load_dataset_file(args.dataset_file)
    all_entries = data["entries"]

    # Filter
    selected = filter_entries(all_entries, slugs=args.slugs)

    if args.limit is not None and args.limit > 0:
        selected = selected[: args.limit]

    if not selected:
        print("No entries matched filters.")
        all_slugs = [e["slug"] for e in all_entries]
        print(f"Available slugs ({len(all_slugs)}): {all_slugs}")
        sys.exit(1)

    print(f"\nEntries: {len(selected)}")
    print(f"Orchestrator: {args.orchestrator}")
    print(f"Subagent: {args.subagent_model}")
    print(f"Provider: {args.provider}")

    if args.dry_run:
        print("\n" + "=" * 72)
        print("DRY RUN — no model loaded, no LLM calls made.")
        print("=" * 72)
        for idx, entry in enumerate(selected):
            print(f"\n[{idx + 1}/{len(selected)}] {entry['slug']}")
            print(f"  system_prompt: {entry.get('system_prompt')!r}")
            print(f"  user_message:  {entry.get('user_message')!r}")
            if entry.get("notes"):
                print(f"  notes:         {entry['notes'][:120]}")
        print("\n" + "=" * 72)
        return

    # Load model once (expensive GPU operation)
    print("\nLoading model...")
    model = load_model("Qwen/Qwen3-4B", "mwhanna/qwen3-4b-transcoders")

    # Create LLM client
    client = LLMClient(provider=args.provider)

    for idx, entry in enumerate(selected):
        print(f"\n{'='*60}")
        print(f"[{idx+1}/{len(selected)}] {entry['slug']}")
        print(f"  Prompt: {entry['user_message']}")
        print(f"{'='*60}")

        cache_path = None
        try:
            cfg = entry_to_run_config(entry)
            cfg.orchestrator_model = args.orchestrator
            cfg.subagent_model = args.subagent_model
            cfg.provider = args.provider
            cfg.max_subagent_hops = args.max_hops
            cfg.verbose = verbose

            prompt = format_chat(
                model.tokenizer,
                cfg.system_prompt,
                cfg.user_message,
                cfg.assistant_prefix,
            )

            cache_path = f"{cfg.graph_cache_dir}/{cfg.prompt_name}_graph.pt"
            max_feat = args.max_feature_nodes if args.max_feature_nodes > 0 else None
            graph_result = compute_or_load_graph(
                prompt, model, cache_path=cache_path, max_feature_nodes=max_feat,
            )
            graph = graph_result["graph"]

            print(
                f"Graph: {graph.adjacency_matrix.shape[0]} nodes, "
                f"{len(graph.selected_features)} features, "
                f"{len(graph.logit_tokens)} logits"
            )

            ctx = ToolContext(
                graph=graph,
                tokenizer=model.tokenizer,
                replacement_model=graph_result["replacement_model"],
                baseline_activations=graph_result["baseline_activations"],
                baseline_answer=graph_result["baseline_answer"],
                baseline_prompt=prompt,
            )

            # Generate full model response ONCE
            full_response = generate_response(prompt, model, max_new_tokens=800)
            print(f"Base model response: {full_response}")

            # Self-rating: subject model "are you sure?" confidence on its own response.
            self_rating = None
            if args.self_rating_samples > 0:
                print(f"Self-rating: sampling {args.self_rating_samples} confidence scores from Qwen3-4B...")
                self_rating = run_self_rating(
                    model,
                    system_prompt=cfg.system_prompt,
                    user_message=cfg.user_message,
                    qwen_answer=full_response,
                    n_samples=args.self_rating_samples,
                    temperature=args.self_rating_temperature,
                )
                mean_str = f"{self_rating['mean']:.2f}" if self_rating["mean"] is not None else "n/a"
                print(
                    f"  self mean={mean_str} "
                    f"parseable={self_rating['parseable_count']}/{self_rating['n_attempts']} "
                    f"({self_rating['elapsed_seconds']:.1f}s)"
                )

            run_single_orchestrator(
                cfg, ctx, client, prompt,
                full_response,
                verbose,
                control_runs=args.control_runs,
                self_rating=self_rating,
            )
        finally:
            if cache_path and not args.keep_graphs:
                graph_file = Path(cache_path)
                if graph_file.exists():
                    size_mb = graph_file.stat().st_size / (1024 * 1024)
                    graph_file.unlink()
                    print(f"  Deleted cached graph: {graph_file.name} ({size_mb:.1f} MB)")

            torch.cuda.empty_cache()

    print(f"\n{'='*60}")
    print("All done!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
