#!/usr/bin/env python3
"""Run circuit_oracle on pre-computed probe attribution graphs.

Each graph in probe_circuits/*.pt was built using google/gemma-2-2b with
gemma-scope transcoders, attributing toward a linear probe direction (not a
next-token logit).  The oracle analyses which transcoder features causally
drive the probe score.

Usage (from repo root or experiments/spurious-correlations/):
    python experiments/spurious-correlations/run_oracle_on_probes.py
    python experiments/spurious-correlations/run_oracle_on_probes.py --slugs bib_journalist_dietitian-biased-probe-correct
    python experiments/spurious-correlations/run_oracle_on_probes.py --concern "What features encode gender bias?"
    python experiments/spurious-correlations/run_oracle_on_probes.py --dataset bib_journalist_dietitian
    python experiments/spurious-correlations/run_oracle_on_probes.py --probe-type unbiased --method correct
"""

import argparse
import os
import sys
from pathlib import Path

# Add local src to the END of sys.path so circuit_oracle (not installed) is found,
# while the installed circuit_tracer (conda env) takes precedence.
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
sys.path.append(str(_REPO_ROOT / "src"))

from circuit_oracle import (  # noqa: E402
    ToolContext,
    LLMClient,
    RunConfig,
    run_circuit_oracle,
    save_run_results,
    PROBE_ORACLE_SKILL,
)


from transformers import AutoTokenizer  # noqa: E402  (after sys.path patch)
from circuit_tracer.graph import Graph  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROBE_CIRCUITS_DIR = _HERE / "probe_circuits"
MODEL_NAME = "google/gemma-2-2b"

# These .pt files are raw nn.Module probe checkpoints, not Graph objects.
EXCLUDE_PREFIXES = ("probe_layer",)

# DATASET_DESCRIPTIONS = {
#     "bib_journalist_dietitian": "BiasInBios: dietitian (positive class) vs journalist (negative class)",
#     "bib_nurse_professor": "BiasInBios: nurse (positive class) vs professor (negative class)",
#     "bib_surgeon_teacher": "BiasInBios: teacher (positive class) vs surgeon (negative class)",
#     "civil_comments": "CivilComments: toxicity classification",
#     "multinli": "MultiNLI: natural language inference (contradiction vs entailment)",
# }

# PROBE_DESCRIPTIONS = {
#     "biased": (
#         "biased probe (trained on ambiguous data where the true label is perfectly "
#         "correlated with a spurious feature, so the probe can exploit both)"
#     ),
#     "unbiased": (
#         "unbiased probe (trained on balanced data where the true label is decorrelated "
#         "from any spurious feature, forcing the probe to rely on causal features only)"
#     ),
# }

# METHOD_DESCRIPTIONS = {
#     "simple": (
#         "CustomTarget approximation — the probe direction is injected at the final "
#         "layer as if it were a logit target, so attribution flows through all layers"
#     ),
#     "correct": (
#         "mean-pooled injection at the probe layer (layer 22) — attribution is injected "
#         "at the residual stream of the layer where the probe actually reads, so only "
#         "features in layers 0-22 are attributed"
#     ),
# }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_slug(slug: str) -> dict:
    """Decompose a graph slug into dataset / probe_type / method.

    Examples:
        bib_journalist_dietitian-biased-probe-correct  →  biased / correct
        civil_comments-unbiased-probe-simple           →  unbiased / simple
    """
    for probe_type in ("biased", "unbiased"):
        marker = f"-{probe_type}-probe-"
        if marker in slug:
            dataset, method = slug.split(marker, 1)
            return {"dataset": dataset, "probe_type": probe_type, "method": method}
    return {"dataset": slug, "probe_type": "unknown", "method": "unknown"}


def build_oracle_query(slug: str, graph: Graph, tokenizer, concern: str | None = None) -> str:
    """Construct the natural-language query sent to the oracle orchestrator."""
    # meta = parse_slug(slug)

    # Reconstruct input text
    try:
        input_text = graph.input_string or tokenizer.decode(
            graph.input_tokens.tolist(), skip_special_tokens=True
        )
    except Exception:
        input_text = "(could not decode input tokens)"
    short_input = input_text[:400] + ("..." if len(input_text) > 400 else "")

    # dataset_desc = DATASET_DESCRIPTIONS.get(meta["dataset"], meta["dataset"])
    # probe_desc = PROBE_DESCRIPTIONS.get(meta["probe_type"], meta["probe_type"])
    # method_desc = METHOD_DESCRIPTIONS.get(meta["method"], meta["method"])

    query = f"Input text:\n{short_input}"

    if concern:
        query += f"\n\nUser concern: {concern}"

    return query


def discover_graphs(
    probe_type: str | None = None,
    dataset: str | None = None,
    method: str | None = None,
    slugs: list[str] | None = None,
) -> list[Path]:
    """Return sorted list of graph .pt paths matching the given filters."""
    if slugs:
        paths = [PROBE_CIRCUITS_DIR / f"{s}.pt" for s in slugs]
        missing = [p for p in paths if not p.exists()]
        if missing:
            for p in missing:
                print(f"ERROR: graph file not found: {p}")
            sys.exit(1)
        return paths

    candidates = sorted(
        p for p in PROBE_CIRCUITS_DIR.glob("*.pt")
        if not any(p.name.startswith(prefix) for prefix in EXCLUDE_PREFIXES)
    )

    if probe_type:
        candidates = [p for p in candidates if f"-{probe_type}-probe-" in p.stem]
    if dataset:
        candidates = [p for p in candidates if p.stem.startswith(dataset)]
    if method:
        candidates = [p for p in candidates if p.stem.endswith(f"-{method}")]

    return candidates


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # parser = argparse.ArgumentParser(
    #     description="Run circuit_oracle on pre-computed probe attribution graphs"
    # )
    # parser.add_argument(
    #     "--slugs", nargs="*",
    #     help="Specific graph slugs to run (without .pt extension)",
    # )
    # parser.add_argument(
    #     "--dataset", default=None,
    #     help="Filter by dataset prefix (e.g. bib_journalist_dietitian, civil_comments)",
    # )
    # parser.add_argument(
    #     "--probe-type", default=None, choices=["biased", "unbiased"],
    #     help="Filter by probe type",
    # )
    # parser.add_argument(
    #     "--method", default=None, choices=["simple", "correct"],
    #     help="Filter by attribution method",
    # )
    # parser.add_argument(
    #     "--concern", type=str, default=None,
    #     help="Optional analysis concern (e.g. 'What features encode gender bias?')",
    # )
    # parser.add_argument(
    #     "--orchestrator-model", default="claude-opus-4-6",
    # )
    # parser.add_argument(
    #     "--subagent-model", default="claude-sonnet-4-6",
    # )
    # parser.add_argument(
    #     "--provider",
    #     default=os.environ.get("LLM_PROVIDER", "anthropic"),
    #     choices=["anthropic", "openrouter"],
    # )
    # parser.add_argument("--max-hops", type=int, default=12)
    # parser.add_argument(
    #     "--output-dir", default="oracle_probe_results",
    #     help="Output directory name (relative to circuits_for_probes/)",
    # )
    # parser.add_argument("--quiet", action="store_true")
    # args = parser.parse_args()

    import argparse
    args = argparse.Namespace(
        # ── Graph selection: 20 circuits per dataset ───────────────────────────────────────────────────
        slugs=[
            # 'bib_nurse_professor-pos_pos_1-biased-probe-correct',
            # 'bib_nurse_professor-pos_pos_1-unbiased-probe-correct',
            # 'bib_nurse_professor-neg_neg_1-biased-probe-correct',
            # 'bib_nurse_professor-neg_neg_1-unbiased-probe-correct',
            # 'bib_nurse_professor-pos_pos_2-biased-probe-correct',
            # 'bib_nurse_professor-pos_pos_2-unbiased-probe-correct',
            # 'bib_nurse_professor-neg_neg_2-biased-probe-correct',
            # 'bib_nurse_professor-neg_neg_2-unbiased-probe-correct',
            
            # 'bib_nurse_professor-pos_pos_3-biased-probe-correct',
            # 'bib_nurse_professor-pos_pos_3-unbiased-probe-correct',
            # 'bib_nurse_professor-neg_neg_3-biased-probe-correct',
            # 'bib_nurse_professor-neg_neg_3-unbiased-probe-correct',
            # 'bib_nurse_professor-pos_pos_4-biased-probe-correct',
            # 'bib_nurse_professor-pos_pos_4-unbiased-probe-correct',
            # 'bib_nurse_professor-neg_neg_4-biased-probe-correct',
            # 'bib_nurse_professor-neg_neg_4-unbiased-probe-correct',
            # 'bib_nurse_professor-pos_pos_5-biased-probe-correct',
            # 'bib_nurse_professor-pos_pos_5-unbiased-probe-correct',
            # 'bib_nurse_professor-neg_neg_5-biased-probe-correct',
            # 'bib_nurse_professor-neg_neg_5-unbiased-probe-correct',
            #===================================================================
            
            # 'bib_journalist_dietitian-pos_pos_1-biased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_1-unbiased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_1-biased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_1-unbiased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_2-biased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_2-unbiased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_2-biased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_2-unbiased-probe-correct',
            
            # 'bib_journalist_dietitian-pos_pos_3-biased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_3-unbiased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_3-biased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_3-unbiased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_4-biased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_4-unbiased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_4-biased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_4-unbiased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_5-biased-probe-correct',
            # 'bib_journalist_dietitian-pos_pos_5-unbiased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_5-biased-probe-correct',
            # 'bib_journalist_dietitian-neg_neg_5-unbiased-probe-correct',
            
            # NOTE: unlike BIB, neg_neg in these means absence of any bias
            #===================================================================

            # 'civil_comments-pos_pos_1-biased-probe-correct',
            # 'civil_comments-pos_pos_1-unbiased-probe-correct',
            # 'civil_comments-pos_pos_2-biased-probe-correct',
            # 'civil_comments-pos_pos_2-unbiased-probe-correct',
            # 'civil_comments-pos_pos_3-biased-probe-correct',
            # 'civil_comments-pos_pos_3-unbiased-probe-correct',
            # 'civil_comments-pos_pos_4-biased-probe-correct',
            # 'civil_comments-pos_pos_4-unbiased-probe-correct',
            
            # 'civil_comments-pos_pos_5-biased-probe-correct',
            # 'civil_comments-pos_pos_5-unbiased-probe-correct',
            # 'civil_comments-pos_pos_6-biased-probe-correct',
            # 'civil_comments-pos_pos_6-unbiased-probe-correct',
            # 'civil_comments-pos_pos_7-biased-probe-correct',
            # 'civil_comments-pos_pos_7-unbiased-probe-correct',
            # 'civil_comments-pos_pos_8-biased-probe-correct',
            # 'civil_comments-pos_pos_8-unbiased-probe-correct',
            # 'civil_comments-pos_pos_9-biased-probe-correct',
            # 'civil_comments-pos_pos_9-unbiased-probe-correct',
            # 'civil_comments-pos_pos_10-biased-probe-correct',
            # 'civil_comments-pos_pos_10-unbiased-probe-correct',

            
            #===================================================================

            # 'multinli-pos_pos_1-biased-probe-correct',
            # 'multinli-pos_pos_1-unbiased-probe-correct',
            # 'multinli-pos_pos_2-biased-probe-correct',
            # 'multinli-pos_pos_2-unbiased-probe-correct',
            # 'multinli-pos_pos_3-biased-probe-correct',
            # 'multinli-pos_pos_3-unbiased-probe-correct',
            # 'multinli-pos_pos_4-biased-probe-correct',
            # 'multinli-pos_pos_4-unbiased-probe-correct',
            
            'multinli-pos_pos_5-biased-probe-correct',
            'multinli-pos_pos_5-unbiased-probe-correct',
            'multinli-pos_pos_6-biased-probe-correct',
            'multinli-pos_pos_6-unbiased-probe-correct',
            'multinli-pos_pos_7-biased-probe-correct',
            'multinli-pos_pos_7-unbiased-probe-correct',
            'multinli-pos_pos_8-biased-probe-correct',
            'multinli-pos_pos_8-unbiased-probe-correct',
            'multinli-pos_pos_9-biased-probe-correct',
            'multinli-pos_pos_9-unbiased-probe-correct',
            'multinli-pos_pos_10-biased-probe-correct',
            'multinli-pos_pos_10-unbiased-probe-correct',
            
            
                        
            
            ],           # e.g. ["bib_journalist_dietitian-biased-probe-correct"]
        dataset=None,         # e.g. "bib_journalist_dietitian" | "civil_comments" | "multinli"
        probe_type=None,      # "biased" | "unbiased" | None (both)
        method=None,          # "simple" | "correct" | None (both)
        # ── Analysis ─────────────────────────────────────────────────────────
        # # BIB
        # # concern="The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.",         # e.g. "What features encode gender bias?"
        # # CC
        # concern= "The circuit use spurious features (e.g.,\"an identity group\" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity.", 
        # # MNLI
        # # concern= "The circuit use spurious features (e.g.,\"negation words\" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.",
        # ── Models ───────────────────────────────────────────────────────────
        orchestrator_model="minimax/minimax-m2.7",   # e.g. "anthropic/claude-opus-4.6 | google/gemini-3.1-pro-preview",
        subagent_model="deepseek/deepseek-v3.2",       # e.g. "anthropic/claude-sonnet-4.6",
        provider=os.environ.get("LLM_PROVIDER", "openrouter"),  # "anthropic" | "openrouter"
        max_hops=12,
        # ── Output ───────────────────────────────────────────────────────────
        output_dir="oracle_probe_results",
        quiet=False,
    )

    # Load .env if present at the repo root.
    env_path = _REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    # Discover graphs
    graph_paths = discover_graphs(
        probe_type=args.probe_type,
        dataset=args.dataset,
        method=args.method,
        slugs=args.slugs,
    )
    if not graph_paths:
        print("No graph files matched the given filters.")
        available = sorted(p.stem for p in PROBE_CIRCUITS_DIR.glob("*.pt")
                           if not any(p.name.startswith(x) for x in EXCLUDE_PREFIXES))
        print(f"Available slugs ({len(available)}):")
        for s in available:
            print(f"  {s}")
        sys.exit(1)

    print(f"Found {len(graph_paths)} graph(s) to process.")

    # Load Gemma tokenizer (no need for the full model — only token decoding is needed).
    print(f"\nLoading tokenizer ({MODEL_NAME})...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    print("Tokenizer ready.")

    # Create LLM client and output directory.
    client = LLMClient(provider=args.provider)
    output_dir = _HERE / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    verbose = not args.quiet

    # ── Process each graph ─────────────────────────────────────────────────────
    for graph_path in graph_paths:
        _lines = []

        def emit(line=""):
            # print(line, flush=True)
            _lines.append(str(line))

        slug = graph_path.stem
        emit(f"\n{'='*60}")
        emit(f"Graph: {slug}")
        emit(f"{'='*60}")

        emit(f"Loading {graph_path.name}...")
        graph = Graph.from_pt(str(graph_path))
        n_nodes = graph.adjacency_matrix.shape[0]
        n_sel = len(graph.selected_features)
        n_logits = len(graph.logit_tokens)
        emit(f"  {n_nodes} nodes | {n_sel} selected features | {n_logits} logit target(s)")

        print("SLUG:", slug)
        if 'bib' in slug:
            concern="The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.",         # e.g. "What features encode gender bias?"
        elif 'civil' in slug:
            concern= "The circuit use spurious features (e.g.,\"an identity group\" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity.", 
        else:
            concern= "The circuit use spurious features (e.g.,\"negation words\" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.",
        print("Concern:", concern)
        ctx = ToolContext(
            graph=graph,
            tokenizer=tokenizer,
            neuronpedia_model_id="gemma-2-2b",
            neuronpedia_sae_id="{layer}-gemmascope-transcoder-16k",
        )

        query = build_oracle_query(slug, graph, tokenizer, concern=concern)
        if verbose:
            emit(f"\nQuery preview (first 300 chars):\n{query[:300]}...\n")

        result = run_circuit_oracle(
            ctx,
            client,
            query,
            orchestrator_model=args.orchestrator_model,
            subagent_model=args.subagent_model,
            max_subagent_hops=args.max_hops,
            verbose=verbose,
            skill=PROBE_ORACLE_SKILL,
        )

        emit(f"\n{'='*60}")
        emit(f"ORACLE ANALYSIS — {slug}")
        emit(f"{'='*60}")
        emit(result["response"])

        # Build a RunConfig so save_run_results can create the standard report.
        meta = parse_slug(slug)
        cfg = RunConfig(
            prompt_name=slug,
            system_prompt="",
            user_message=(
                f"Dataset: {meta['dataset']} | "
                f"Probe: {meta['probe_type']} | "
                f"Method: {meta['method']}"
            ),
            question=concern,
            experiment_prefix="probe",
            orchestrator_model=args.orchestrator_model,
            subagent_model=args.subagent_model,
            provider=args.provider,
        )

        exp_dir = save_run_results(
            result,
            cfg,
            prompt=graph.input_string or "",
            base_dir=str(output_dir),
        )
        emit(f"Results saved to: {exp_dir}")

        log_path = Path(exp_dir) / "run.log"
        log_path.write_text("\n".join(_lines) + "\n")
        print(f"Log written to: {log_path}", flush=True)


if __name__ == "__main__":
    main()
