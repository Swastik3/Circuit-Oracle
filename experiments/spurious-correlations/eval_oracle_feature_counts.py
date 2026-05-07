"""
Feature-counting meta-evaluation of oracle probe results.

For each probe experiment, ask the judge to enumerate every feature the oracle
surfaced and classify it as spurious / causal / other, then report counts and
spurious_fraction. Biased and unbiased probes are judged independently — no
pairing, no confirmation-biased prior about which class should dominate.

Passes richer context than eval_oracle_spuriosity.py:
  - full analysis response (no truncation)
  - the oracle's curated build_circuit node list (authoritative feature set)
  - inspect_feature outputs (Neuronpedia labels + top activating snippets)
  - input prompt tokens recovered from embed-node labels

Usage:
    python experiments/spurious-correlations/eval_oracle_feature_counts.py
    python experiments/spurious-correlations/eval_oracle_feature_counts.py --results-dir experiments/spurious-correlations/oracle_probe_results
    python experiments/spurious-correlations/eval_oracle_feature_counts.py --force   # re-judge cached runs
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import dotenv

from anthropic import Anthropic

_HERE       = Path(__file__).parent
dotenv.load_dotenv(_HERE.parent.parent / ".env")
RESULTS     = _HERE / "oracle_probe_results"
JUDGE_MODEL = "openai/gpt-5.4-mini"
OUTPUT_FILE_FULL = "judge_feature_counts.json"
OUTPUT_FILE_SLIM = "judge_feature_counts_slim.json"


# Dataset-specific definitions. Adding a new dataset = a 4-line entry here;
# the judge prompt itself stays generic.
DATASET_DEFS = {
    "bib_nurse_professor": {
        "task":     "profession classification from short biographies",
        "spurious": "gender markers — pronouns (she/he/her/him), gendered names, "
                    "honorifics (Mr./Mrs./Ms.), gendered relational terms "
                    "(mother, husband, wife), features whose promoted tokens are gendered.",
        "causal":   "profession indicators — job titles, profession-specific vocabulary, "
                    "workplace/tool/skill/education terminology, plus content-neutral "
                    "lexical or syntactic features.",
    },
    "bib_journalist_dietitian": {
        "task":     "profession classification from short biographies",
        "spurious": "gender markers — pronouns (she/he/her/him), gendered names, "
                    "honorifics (Mr./Mrs./Ms.), gendered relational terms "
                    "(mother, husband, wife), features whose promoted tokens are gendered.",
        "causal":   "profession indicators — job titles, profession-specific vocabulary, "
                    "workplace/tool/skill/education terminology, plus content-neutral "
                    "lexical or syntactic features.",
    },
    "bib_surgeon_teacher": {
        "task":     "profession classification from short biographies",
        "spurious": "gender markers — pronouns (she/he/her/him), gendered names, "
                    "honorifics (Mr./Mrs./Ms.), gendered relational terms "
                    "(mother, husband, wife), features whose promoted tokens are gendered.",
        "causal":   "profession indicators — job titles, profession-specific vocabulary, "
                    "workplace/tool/skill/education terminology, plus content-neutral "
                    "lexical or syntactic features.",
    },
    "civil_comments": {
        "task":     "binary toxicity classification on online comments",
        "spurious": "identity-group signals — detectors for demographic tokens "
                    "(race, religion, gender, nationality, sexual orientation), "
                    "morphology matchers that fire on ethnic terms, identity-phrase "
                    "syntax (\"I'm a X\"), features whose promoted tokens are "
                    "demographic labels without toxic content.",
        "causal":   "toxic-content detectors — profanity, threats, insults, harassment, "
                    "slurs, abuse/violence semantics, plus identity-independent lexical "
                    "or syntactic features (punctuation, sentence structure, tone).",
    },
    "multinli": {
        "task":     "binary NLI — entailment vs. contradiction",
        "spurious": "negation-word detectors in the hypothesis — features whose role "
                    "is spotting \"no, not, never, nobody, nothing, nor, neither, "
                    "without, n't\" regardless of meaning.",
        "causal":   "semantic-relation features — meaning overlap between premise and "
                    "hypothesis, logical consistency, factual alignment, plus "
                    "content-neutral lexical or syntactic features.",
    },
}


EVAL_PROMPT_HEADER = """\
You are analyzing a circuit-oracle report for a linear probe. The probe's
prediction can be driven by two kinds of features:

- SPURIOUS features detect signals that correlate with the label in training
  data but are not causally related to the task.
- CAUSAL features detect signals that genuinely determine the label.

Task: {task}
SPURIOUS features on this task: {spurious_def}
CAUSAL features on this task: {causal_def}

Classification rules:
1. Classify by the feature's SEMANTIC ROLE, not the token that triggers it.
2. Purely structural features (generic word/punctuation/BOS detectors) or
   features the oracle dismisses go in "other".
3. Enumerate BOTH classes exhaustively BEFORE counting.
4. Judge only what the oracle actually claims.

Probe type: {probe_type}    Subgroup: {subgroup}
"""

EVAL_PROMPT_EXTRAS = """\

Input prompt tokens (from embed nodes): {input_tokens}

--- Oracle's curated circuit (authoritative feature list) ---
{circuit_nodes}

--- Feature labels looked up by the oracle (Neuronpedia) ---
{feature_labels}
"""

EVAL_PROMPT_FOOTER = """\

--- Oracle's written analysis ---
{analysis}
---

Respond in JSON only. spurious_fraction = n_spurious / (n_spurious + n_causal),
or null if the denominator is 0.

{{
  "spurious_features": [
    {{"id": "L5:F14124", "label": "<oracle's label>", "reason": "<≤15 words>"}}
  ],
  "causal_features": [
    {{"id": "L4:F148", "label": "<oracle's label>", "reason": "<≤15 words>"}}
  ],
  "other_features": [
    {{"id": "L0:F8444", "label": "<oracle's label>", "reason": "<≤15 words>"}}
  ],
  "n_spurious": <int>,
  "n_causal": <int>,
  "n_other": <int>,
  "spurious_fraction": <float in [0,1] or null>,
  "dominant": "spurious" | "causal" | "mixed" | "none",
  "notes": "<≤25 words>"
}}"""


def build_prompt(meta, ctx, defs, slim: bool) -> str:
    parts = [EVAL_PROMPT_HEADER.format(
        task=defs["task"],
        spurious_def=defs["spurious"],
        causal_def=defs["causal"],
        probe_type=meta["probe_type"],
        subgroup=meta["subgroup"],
    )]
    if not slim:
        parts.append(EVAL_PROMPT_EXTRAS.format(
            input_tokens=ctx["input_tokens"],
            circuit_nodes=ctx["circuit_nodes"],
            feature_labels=ctx["feature_labels"],
        ))
    parts.append(EVAL_PROMPT_FOOTER.format(analysis=ctx["analysis"]))
    return "".join(parts)


def parse_exp_name(name: str) -> dict:
    """
    Parse folder names like:
      exp-probe-civil_comments-pos_pos_4-unbiased-probe-correct-question
      exp-probe-bib_nurse_professor-pos_pos_1-biased-probe-correct-question
    """
    name = name.removeprefix("exp-probe-")
    probe_type = None
    for pt in ("biased", "unbiased"):
        suffix = f"-{pt}-probe-correct-question"
        if suffix in name:
            prefix = name[: name.index(suffix)]
            probe_type = pt
            break
    if probe_type is None:
        return {}

    m = re.search(r"-((?:pos_pos|neg_neg)_\d+)$", prefix)
    if not m:
        return {}
    subgroup_n = m.group(1)
    dataset    = prefix[: m.start()]
    subgroup   = "_".join(subgroup_n.split("_")[:2])
    n          = subgroup_n.split("_")[-1]
    return {"dataset": dataset, "subgroup": subgroup, "n": n, "probe_type": probe_type}


def latest_run(exp_dir: Path) -> Path | None:
    runs = sorted(exp_dir.iterdir(), key=lambda p: p.name)
    return runs[-1] if runs else None


def extract_context(oracle_result: dict) -> dict:
    """Pull analysis + curated circuit + feature labels out of oracle_result.json."""
    analysis = oracle_result.get("response", "") or ""
    tool_calls = oracle_result.get("tool_calls", []) or []

    # ── 1. Curated circuit from build_circuit ───────────────────────────────
    circuit_nodes_text = "(no build_circuit call found)"
    input_tokens_text  = "(unknown)"
    for c in tool_calls:
        if c.get("tool") != "build_circuit":
            continue
        nodes = (c.get("input") or {}).get("nodes", []) or []
        # Sometimes the orchestrator passes `nodes` as a JSON-encoded string.
        if isinstance(nodes, str):
            try:
                nodes = json.loads(nodes)
            except Exception:
                nodes = []
        if not isinstance(nodes, list):
            nodes = []
        lines        = []
        embed_labels = []
        for n in nodes:
            if not isinstance(n, dict):
                continue
            label = n.get("label", "?")
            feats = n.get("features", []) or []
            if isinstance(feats, str):
                try:
                    feats = json.loads(feats)
                except Exception:
                    feats = []
            if not isinstance(feats, list):
                feats = []
            feat_ids = []
            for f in feats:
                if not isinstance(f, dict):
                    continue
                L, idx = f.get("layer"), f.get("feature_idx")
                if L is None or idx is None or L < 0 or idx < 0:
                    continue
                pos = f.get("pos")
                feat_ids.append(f"L{L}:F{idx}@{pos}" if pos is not None else f"L{L}:F{idx}")
            id_str = ", ".join(feat_ids) if feat_ids else "(embed/output)"
            lines.append(f"  - {label}  [{id_str}]")
            low = label.lower()
            if low.startswith("emb") or "emb:" in low or low.startswith("input"):
                embed_labels.append(label)
        circuit_nodes_text = "\n".join(lines) if lines else "(empty)"
        if embed_labels:
            input_tokens_text = " | ".join(embed_labels)
        break

    # ── 2. inspect_feature outputs → feature label dictionary ───────────────
    feat_label_lines = []
    for c in tool_calls:
        if c.get("tool") != "inspect_feature":
            continue
        inp = c.get("input") or {}
        out = c.get("output") or {}
        L, idx = inp.get("layer"), inp.get("feature_idx")
        label = out.get("label", "?") if isinstance(out, dict) else "?"
        examples = []
        if isinstance(out, dict):
            for ex in (out.get("top_activating_examples") or [])[:2]:
                snippet = ex.get("text_snippet", "") if isinstance(ex, dict) else ""
                if snippet:
                    # Neuronpedia snippets use U+2581 for spaces; make readable.
                    snippet = snippet.replace("\u2581", " ").replace("\n", " ")
                    examples.append(snippet.strip()[:100])
        ex_str = f"    top-acts: {'  ||  '.join(examples)}" if examples else ""
        feat_label_lines.append(f"  L{L}:F{idx}: {label}{('  ' + ex_str) if ex_str else ''}")
    feature_labels_text = "\n".join(feat_label_lines) if feat_label_lines else "(no inspect_feature calls)"

    return {
        "analysis":       analysis,
        "circuit_nodes":  circuit_nodes_text,
        "feature_labels": feature_labels_text,
        "input_tokens":   input_tokens_text,
    }


def judge(client: Anthropic, meta: dict, ctx: dict, slim: bool) -> dict:
    defs = DATASET_DEFS.get(meta["dataset"])
    if defs is None:
        raise ValueError(f"No DATASET_DEFS entry for {meta['dataset']!r}")

    prompt = build_prompt(meta, ctx, defs, slim=slim)

    msg = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    text = next(b.text for b in msg.content if b.type == "text").strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    try:
        result = json.loads(cleaned)
    except Exception as ex:
        print("JSON parse failed:", ex)
        print(text[:2000])
        raise

    # Recompute spurious_fraction from counts so it's always consistent with
    # n_spurious / n_causal (the judge occasionally reports inconsistent
    # arithmetic). Prefer the lengths of the feature lists over the
    # reported n_* fields when both are present, since lists are harder
    # for the judge to miscount.
    def _len(key):
        v = result.get(key)
        return len(v) if isinstance(v, list) else 0

    n_s = _len("spurious_features") or int(result.get("n_spurious") or 0)
    n_c = _len("causal_features")   or int(result.get("n_causal")   or 0)
    n_o = _len("other_features")    or int(result.get("n_other")    or 0)
    result["n_spurious"] = n_s
    result["n_causal"]   = n_c
    result["n_other"]    = n_o
    denom = n_s + n_c
    result["spurious_fraction"] = (n_s / denom) if denom > 0 else None
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default=str(RESULTS))
    parser.add_argument("--force", action="store_true", help="Re-judge even if cached")
    parser.add_argument("--slim", action="store_true",
                        help="Ablation: drop curated-circuit and feature-label context; "
                             "pass only the oracle's analysis prose. Caches separately.")
    args = parser.parse_args()

    output_file = OUTPUT_FILE_SLIM if args.slim else OUTPUT_FILE_FULL

    results_dir = Path(args.results_dir)
    exp_dirs = sorted(
        d for d in results_dir.iterdir()
        if d.is_dir() and d.name.startswith("exp-probe-")
    )
    if not exp_dirs:
        print(f"No experiment directories found in {results_dir}")
        sys.exit(1)

    key = os.environ.get("OPENROUTER_API_KEY", "")
    client = Anthropic(
        base_url="https://openrouter.ai/api",
        auth_token=key,
        api_key="",
    )

    rows = []
    for exp_dir in exp_dirs:
        meta = parse_exp_name(exp_dir.name)
        if not meta:
            print(f"  SKIP (could not parse): {exp_dir.name}")
            continue
        if meta["dataset"] not in DATASET_DEFS:
            print(f"  SKIP (unknown dataset {meta['dataset']}): {exp_dir.name}")
            continue

        run_dir = latest_run(exp_dir)
        if not run_dir:
            continue

        out_path = run_dir / output_file
        if out_path.exists() and not args.force:
            result = json.loads(out_path.read_text())
            rows.append({**meta, **result, "exp": exp_dir.name})
            frac = result.get("spurious_fraction")
            frac_s = f"{frac:.2f}" if isinstance(frac, (int, float)) else "—"
            print(f"  CACHED  {meta['dataset']:26} {meta['subgroup']}_{meta['n']:<3} "
                  f"{meta['probe_type']:8} → s={result.get('n_spurious')} "
                  f"c={result.get('n_causal')} frac={frac_s}")
            continue

        result_path = run_dir / "oracle_result.json"
        if not result_path.exists():
            continue
        oracle_result = json.loads(result_path.read_text())
        ctx = extract_context(oracle_result)
        if not ctx["analysis"]:
            print(f"  SKIP (no analysis): {exp_dir.name}")
            continue

        print(f"  Judging {meta['dataset']:26} {meta['subgroup']}_{meta['n']:<3} "
              f"{meta['probe_type']:8} ...", flush=True)
        result = judge(client, meta, ctx, slim=args.slim)
        out_path.write_text(json.dumps(result, indent=2))
        rows.append({**meta, **result, "exp": exp_dir.name})
        frac = result.get("spurious_fraction")
        frac_s = f"{frac:.2f}" if isinstance(frac, (int, float)) else "—"
        print(f"    → s={result.get('n_spurious')} c={result.get('n_causal')} "
              f"o={result.get('n_other')} frac={frac_s} "
              f"dom={result.get('dominant')}")

    # ── Summary ────────────────────────────────────────────────────────────
    DATASETS = [
        "bib_nurse_professor",
        "bib_journalist_dietitian",
        "bib_surgeon_teacher",
        "civil_comments",
        "multinli",
    ]

    def fmt_stats(subset):
        fracs = [r["spurious_fraction"] for r in subset
                 if isinstance(r.get("spurious_fraction"), (int, float))]
        if not fracs:
            return "n=0"
        mean = sum(fracs) / len(fracs)
        srt  = sorted(fracs)
        med  = srt[len(srt) // 2]
        dom = defaultdict(int)
        for r in subset:
            dom[r.get("dominant", "?")] += 1
        dom_str = " ".join(f"{k}={v}" for k, v in sorted(dom.items()))
        return f"n={len(fracs):2d}  mean={mean:.2f}  median={med:.2f}  [{dom_str}]"

    print("\n" + "=" * 78)
    print("FEATURE-COUNT SUMMARY  (spurious_fraction, independent per probe)")
    print("=" * 78)
    for dataset in DATASETS:
        subset = [r for r in rows if r["dataset"] == dataset]
        if not subset:
            continue
        biased   = [r for r in subset if r["probe_type"] == "biased"]
        unbiased = [r for r in subset if r["probe_type"] == "unbiased"]
        print(f"\n  {dataset}")
        print(f"    Biased    {fmt_stats(biased)}")
        print(f"    Unbiased  {fmt_stats(unbiased)}")
        for r in sorted(subset, key=lambda r: (r["probe_type"], r["subgroup"], int(r["n"]))):
            frac = r.get("spurious_fraction")
            frac_s = f"{frac:.2f}" if isinstance(frac, (int, float)) else "—"
            ns = r.get("n_spurious", 0)
            nc = r.get("n_causal", 0)
            no = r.get("n_other", 0)
            print(f"      [{r['probe_type']:8}] {r['subgroup']}_{r['n']:<3} "
                  f"s={ns} c={nc} o={no} frac={frac_s} dom={r.get('dominant','?')}")

    # ── Accuracy derived from `dominant` ───────────────────────────────────
    # Rule:
    #   biased   probe → CORRECT if dominant == "spurious"
    #   unbiased probe → CORRECT if dominant in {"causal", "mixed"}
    def is_correct(r):
        dom = r.get("dominant")
        if r["probe_type"] == "biased":
            return dom == "spurious"
        return dom in ("causal", "mixed")

    print("\n" + "=" * 78)
    mode = "SLIM (analysis only)" if args.slim else "FULL (analysis + circuit + labels)"
    print(f"ACCURACY SUMMARY  [{mode}]  "
          "(biased→spurious-dominated, unbiased→causal/mixed)")
    print("=" * 78)

    overall_b_total = overall_b_correct = 0
    overall_u_total = overall_u_correct = 0

    for dataset in DATASETS:
        subset = [r for r in rows if r["dataset"] == dataset]
        if not subset:
            continue
        biased   = [r for r in subset if r["probe_type"] == "biased"]
        unbiased = [r for r in subset if r["probe_type"] == "unbiased"]

        b_total   = len(biased)
        b_correct = sum(is_correct(r) for r in biased)
        u_total   = len(unbiased)
        u_correct = sum(is_correct(r) for r in unbiased)

        overall_b_total   += b_total
        overall_b_correct += b_correct
        overall_u_total   += u_total
        overall_u_correct += u_correct

        b_pct = 100 * b_correct / b_total if b_total else 0
        u_pct = 100 * u_correct / u_total if u_total else 0
        print(f"\n  {dataset}")
        print(f"    Biased:   {b_correct}/{b_total} ({b_pct:.0f}%)")
        print(f"    Unbiased: {u_correct}/{u_total} ({u_pct:.0f}%)")
        for r in sorted(subset, key=lambda r: (r["probe_type"], r["subgroup"], int(r["n"]))):
            mark   = "✓" if is_correct(r) else "✗"
            frac   = r.get("spurious_fraction")
            frac_s = f"{frac:.2f}" if isinstance(frac, (int, float)) else "—"
            print(f"      {mark} [{r['probe_type']:8}] {r['subgroup']}_{r['n']:<3} "
                  f"dom={r.get('dominant','?'):8} frac={frac_s}")

    if overall_b_total or overall_u_total:
        b_pct = 100 * overall_b_correct / overall_b_total if overall_b_total else 0
        u_pct = 100 * overall_u_correct / overall_u_total if overall_u_total else 0
        total   = overall_b_total + overall_u_total
        correct = overall_b_correct + overall_u_correct
        print(f"\n  {'─' * 50}")
        print(f"  OVERALL  Biased: {overall_b_correct}/{overall_b_total} ({b_pct:.0f}%)   "
              f"Unbiased: {overall_u_correct}/{overall_u_total} ({u_pct:.0f}%)   "
              f"Total: {correct}/{total} ({100 * correct / total:.0f}%)")

    # ── AUROC on spurious_fraction (threshold-free) ────────────────────────
    # Positive class = biased (score = spurious_fraction, higher = more biased).
    # Rows with None fraction (empty counts) are excluded.
    print("\n" + "=" * 78)
    print(f"AUROC  [{mode}]  (spurious_fraction as score, biased=positive)")
    print("=" * 78)

    def _valid(rs):
        return [r for r in rs if isinstance(r.get("spurious_fraction"), (int, float))]

    def _auroc(scores_pos, scores_neg):
        """Mann-Whitney-U AUROC with ties counted as 0.5."""
        n_p, n_n = len(scores_pos), len(scores_neg)
        if n_p == 0 or n_n == 0:
            return float("nan")
        wins = 0.0
        for p in scores_pos:
            for n in scores_neg:
                if p > n:
                    wins += 1.0
                elif p == n:
                    wins += 0.5
        return wins / (n_p * n_n)

    dataset_roc = {}  # dataset -> (auroc, n_pos, n_neg, n_dropped)
    for dataset in DATASETS:
        subset = [r for r in rows if r["dataset"] == dataset]
        if not subset:
            continue
        valid   = _valid(subset)
        dropped = len(subset) - len(valid)
        pos = [r["spurious_fraction"] for r in valid if r["probe_type"] == "biased"]
        neg = [r["spurious_fraction"] for r in valid if r["probe_type"] == "unbiased"]
        auc = _auroc(pos, neg)
        dataset_roc[dataset] = (auc, len(pos), len(neg), dropped)
        drop_s = f"  dropped={dropped}" if dropped else ""
        print(f"  {dataset:26} AUROC = {auc:.3f}   "
              f"(n_biased={len(pos)}, n_unbiased={len(neg)}){drop_s}")

    # Overall (pooled across datasets)
    all_valid = _valid(rows)
    all_dropped = len(rows) - len(all_valid)
    pos_all = [r["spurious_fraction"] for r in all_valid if r["probe_type"] == "biased"]
    neg_all = [r["spurious_fraction"] for r in all_valid if r["probe_type"] == "unbiased"]
    auc_all = _auroc(pos_all, neg_all)
    drop_s = f"  dropped={all_dropped}" if all_dropped else ""
    print(f"  {'OVERALL (pooled)':26} AUROC = {auc_all:.3f}   "
          f"(n_biased={len(pos_all)}, n_unbiased={len(neg_all)}){drop_s}")

    # ── Plot ───────────────────────────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        labels = list(dataset_roc.keys()) + ["OVERALL"]
        values = [dataset_roc[d][0] for d in dataset_roc] + [auc_all]
        colors = ["#4c72b0"] * len(dataset_roc) + ["black"]

        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.5)
        ax.axhline(0.5, linestyle="--", color="gray", linewidth=1, label="chance")
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.01,
                    f"{v:.3f}", ha="center", va="bottom", fontsize=9)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("AUROC  (spurious_fraction, biased=positive)")
        ax.set_title(f"AUROC per dataset  [{mode}]")
        ax.tick_params(axis="x", rotation=20)
        for lbl in ax.get_xticklabels():
            lbl.set_ha("right")
        ax.legend(loc="lower right", fontsize=8)
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()

        plot_path = _HERE / (
            "auroc_feature_counts_slim.png" if args.slim else "auroc_feature_counts.png"
        )
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)
        print(f"\n  AUROC bar chart saved to: {plot_path}")
    except ImportError:
        print("\n  (matplotlib not available — skipping plot)")


if __name__ == "__main__":
    main()
