#!/usr/bin/env python3
"""
Run circuit_extraction.py on the top-5 neg_neg and top-5 pos_pos prompts
from probe_spuriosity/analysis.md for a given dataset.

Usage:
    python run_extraction_batch.py --dataset bib_nurse_professor
    python run_extraction_batch.py --dataset bib_journalist_dietitian --skip-existing
    python run_extraction_batch.py --dataset civil_comments --tags neg_neg_1 pos_pos_2

Each run appends stdout/stderr to probe_circuits/logs/<dataset>.log.<n>,
where <n> is the next available integer.
"""
import json    
import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
# ANALYSIS_MD = SCRIPT_DIR / "probe_spuriosity" / "analysis_2.md"
# Analysis 1[:5]+3+2
DATASET_JSON = SCRIPT_DIR / "prompts.json"
EXTRACTION_SCRIPT = SCRIPT_DIR / "circuit_extraction.py"
PROBE_CIRCUITS_DIR = SCRIPT_DIR / "probe_circuits"
LOGS_DIR = PROBE_CIRCUITS_DIR / "logs"

VALID_DATASETS = [
    "bib_nurse_professor",
    "bib_journalist_dietitian",
    "bib_surgeon_teacher",
    "civil_comments",
    "multinli",
]


# ---------------------------------------------------------------------------
# analysis.md parser
# ---------------------------------------------------------------------------

def parse_dataset_prompts(dataset: str) -> dict[str, list[str]]:
    """
    Parse probe_spuriosity/analysis.md and return
    {'neg_neg': [...prompts...], 'pos_pos': [...prompts...]}
    for the given dataset.

    neg_neg = subgroup with (target=0, spurious=0)
    pos_pos = subgroup with (target=1, spurious=1)
    """
    prompt_dataset = json.load(open(DATASET_JSON, "r"))
    result = prompt_dataset[dataset]
    return result
    # Load existing data from JSON if it exists
    # existing: dict[str, dict[str, list[str]]] = {}
    # if DATASET_JSON.exists():
    #     with open(DATASET_JSON, 'r') as f:
    #         existing = json.load(f)

    # text = ANALYSIS_MD.read_text()
    # lines = text.split('\n')

    # result: dict[str, list[str]] = {'neg_neg': [], 'pos_pos': []}
    # in_dataset = False
    # current_key: str | None = None
    # in_top_prompts = False
    # in_quoted = False
    # current_prompt_lines: list[str] = []

    # for line in lines:

    #     # ── Dataset section header (## dataset) ────────────────────────────
    #     if line.startswith('## '):
    #         in_dataset = (line[3:].strip() == dataset)
    #         current_key = None
    #         in_top_prompts = False
    #         in_quoted = False
    #         current_prompt_lines = []
    #         continue

    #     if not in_dataset:
    #         continue

    #     # ── Subgroup header (### ...) ───────────────────────────────────────
    #     if line.startswith('### '):
    #         m = re.search(r'\(target=(\d+), spurious=(\d+)\)', line)
    #         if m:
    #             tv, sv = int(m.group(1)), int(m.group(2))
    #             current_key = {(0, 0): 'neg_neg', (1, 1): 'pos_pos'}.get((tv, sv))
    #         else:
    #             current_key = None
    #         in_top_prompts = False
    #         in_quoted = False
    #         current_prompt_lines = []
    #         continue

    #     # ── Top prompts subsection (#### Top N prompts …) ──────────────────
    #     if line.startswith('#### Top ') and 'prompts' in line:
    #         in_top_prompts = True
    #         in_quoted = False
    #         current_prompt_lines = []
    #         continue

    #     # Stop at the next section header of any level
    #     if line.startswith('###') or line.startswith('##'):
    #         in_top_prompts = False
    #         continue

    #     if not in_top_prompts or current_key is None:
    #         continue

    #     # ── Inside a Top-N prompts block ────────────────────────────────────
    #     stripped = line.strip()

    #     if in_quoted:
    #         # Continuing a multi-line quoted prompt
    #         current_prompt_lines.append(line)
    #         if stripped.endswith('"'):
    #             full = '\n'.join(current_prompt_lines).strip()
    #             if full.startswith('"') and full.endswith('"'):
    #                 full = full[1:-1]
    #             result[current_key].append(full)
    #             current_prompt_lines = []
    #             in_quoted = False
    #     else:
    #         if stripped.startswith('"'):
    #             if stripped.endswith('"') and len(stripped) > 1:
    #                 # Single-line quoted prompt
    #                 result[current_key].append(stripped[1:-1])
    #             else:
    #                 # Start of a multi-line prompt
    #                 in_quoted = True
    #                 current_prompt_lines = [stripped]
    # # Merge with existing data, deduplicating prompts
    # if dataset in existing:
    #     for key in ('neg_neg', 'pos_pos'):
    #         existing_prompts = existing[dataset].get(key, [])
    #         seen = set(existing_prompts)
    #         merged = list(existing_prompts)
    #         for prompt in result[key]:
    #             if prompt not in seen:
    #                 merged.append(prompt)
    #                 seen.add(prompt)
    #         result[key] = merged

    # # Write back
    # existing[dataset] = result
    # with open(DATASET_JSON, 'w') as f:
    #     json.dump(existing, f, indent=2)

    # return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def next_log_number(dataset: str) -> int:
    """Return the next unused log number for the given dataset."""
    existing = list(LOGS_DIR.glob(f"{dataset}.log.*"))
    nums: list[int] = []
    for p in existing:
        try:
            nums.append(int(p.name.rsplit('.', 1)[-1]))
        except ValueError:
            pass
    return (max(nums) + 1) if nums else 1


def output_exists(dataset: str, tag: str) -> bool:
    """True if both biased and unbiased correct .pt files already exist."""
    biased   = PROBE_CIRCUITS_DIR / f"{dataset}-{tag}-biased-probe-correct.pt"
    unbiased = PROBE_CIRCUITS_DIR / f"{dataset}-{tag}-unbiased-probe-correct.pt"
    return biased.exists() and unbiased.exists()


# ---------------------------------------------------------------------------
# Per-prompt extraction runner
# ---------------------------------------------------------------------------

def run_extraction(dataset: str, prompt_tag: str, prompt: str, log_path: Path) -> int:
    """
    Invoke circuit_extraction.py for one (dataset, prompt_tag, prompt) triple.
    Streams combined stdout+stderr to the console and appends to log_path.
    Returns the subprocess exit code.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, 'w') as log_f:
        log_f.write(f"# Dataset:    {dataset}\n")
        log_f.write(f"# Tag:        {prompt_tag}\n")
        short = prompt[:120] + ('…' if len(prompt) > 120 else '')
        log_f.write(f"# Prompt:     {short}\n")
        log_f.write("=" * 60 + "\n\n")
        log_f.flush()

        proc = subprocess.Popen(
            [
                sys.executable, str(EXTRACTION_SCRIPT),
                "--dataset",    dataset,
                "--prompt-tag", prompt_tag,
                "--prompt",     prompt,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=str(SCRIPT_DIR),
        )
        for line in proc.stdout:
            sys.stdout.write(line)
            log_f.write(line)
        proc.wait()

    return proc.returncode


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch circuit extraction on top neg_neg / pos_pos prompts from analysis.md",
    )
    parser.add_argument(
        '--dataset', required=True, choices=VALID_DATASETS,
        help="Dataset slug to process",
    )
    parser.add_argument(
        '--skip-existing', action='store_true',
        help="Skip runs where output .pt files already exist in probe_circuits/",
    )
    parser.add_argument(
        '--tags', nargs='+', metavar='TAG',
        help="Only run specific tags, e.g. --tags neg_neg_1 pos_pos_3",
    )
    args = parser.parse_args()

    # ── Parse prompts ────────────────────────────────────────────────────────
    print(f"Parsing analysis.md for dataset: {args.dataset}", flush=True)
    prompts = parse_dataset_prompts(args.dataset)

    start_idx = 5
    pos_pos = prompts['pos_pos'][start_idx:10]
    neg_neg = [] # prompts['neg_neg'][start_idx:10]
    print(f"  pos_pos prompts found: {len(pos_pos)}", flush=True)
    print(f"  neg_neg prompts found: {len(neg_neg)}", flush=True)

    if not neg_neg and not pos_pos:
        print("ERROR: no prompts found — check dataset name and analysis.md", flush=True)
        sys.exit(1)

    # ── Build run list ───────────────────────────────────────────────────────
    runs: list[tuple[str, str]] = []
    for i, prompt in enumerate(pos_pos, start_idx+1):
        runs.append((f"pos_pos_{i}", prompt))
    for i, prompt in enumerate(neg_neg, start_idx+1):
        runs.append((f"neg_neg_{i}", prompt))


    if args.tags:
        allowed = set(args.tags)
        runs = [(tag, p) for tag, p in runs if tag in allowed]
        print(f"Filtered to {len(runs)} run(s) by --tags", flush=True)

    # ── Run ──────────────────────────────────────────────────────────────────
    print(f"\nStarting {len(runs)} extraction(s) for '{args.dataset}':\n", flush=True)

    log_num = next_log_number(args.dataset)
    errors: list[str] = []

    for tag, prompt in runs:
        short = prompt[:80].replace('\n', ' ') + ('…' if len(prompt) > 80 else '')
        print(f"[{tag}] prompt: {short!r}", flush=True)

        if args.skip_existing and output_exists(args.dataset, tag):
            print(f"  → skipping (output {args.dataset}-{tag}*.pt files already exist)\n", flush=True)
            continue

        log_path = LOGS_DIR / f"{args.dataset}.log.{log_num}"
        print(f"  → log: {log_path.relative_to(SCRIPT_DIR)}", flush=True)

        rc = run_extraction(args.dataset, tag, prompt, log_path)
        log_num += 1

        if rc != 0:
            print(f"  → FAILED (exit code {rc})\n", flush=True)
            errors.append(tag)
        else:
            print(f"  → OK\n", flush=True)

    # ── Summary ──────────────────────────────────────────────────────────────
    if errors:
        print(f"Finished with errors in tags: {errors}", flush=True)
        sys.exit(1)
    else:
        print("All extractions completed successfully.", flush=True)


if __name__ == '__main__':
    # prompt_data = {}
    # for dataset in VALID_DATASETS:
    #     print(f"Parsing analysis.md for dataset: {dataset}", flush=True)
    #     prompts = parse_dataset_prompts(dataset)
    #     prompt_data[dataset] = prompts
    #     prompts['pos_pos']=prompts['pos_pos']
    #     prompts['neg_neg']=prompts['neg_neg']
    #     print(f"  pos_pos prompts found: {len(prompts['pos_pos'])}", flush=True)
    #     print(f"  neg_neg prompts found: {len(prompts['neg_neg'])}", flush=True)

    # with open(DATASET_JSON, 'w') as f:
    #     json.dump(prompt_data, f, indent=4)
    # print(f"Wrote {DATASET_JSON}")

    
    main()
