# Refusal — Suppression-Jailbreaking via Intervention

Paper §6 (Table 3). The oracle nominates transcoder features in a refusing Qwen3-4B forward pass, applies multiplicative steering, and verifies that softening the candidate features releases the underlying answer. Head-to-head against the Arditi et al. diff-in-mean refusal-direction baseline.

Subject model: `Qwen/Qwen3-4B` + `mwhanna/qwen3-4b-transcoders`.
Orchestrator: GPT-5.4 with concurrent GPT-OSS-120B subagents (configurable).

## Folder layout

```
refusal/
├── README.md                       # this file
├── scripts/
│   ├── run_all.py                  # main oracle entry point
│   └── download_weights.py         # fetch Qwen3-4B + transcoders → ./weights/
├── data/
│   └── prompts.json                # 10 locked prompts (5 refusal + 5 censorship)
├── exp/                            # oracle results — one dir per prompt + judge_summary.{json,md}
└── baselines/arditi/
    ├── README.md                   # baseline pipeline docs
    ├── runpod_setup.sh             # 4-stage runner (fetch → extract → apply → judge)
    ├── extract_direction.py        # GPU: diff-in-mean direction
    ├── apply_direction.py          # GPU: ablated completions on locked prompts
    ├── fetch_data.py               # AdvBench + Alpaca-Cleaned
    ├── llm_judge.py / exp_judge.py # 2-judge continuous scoring
    └── runs/refusal/               # baseline outputs — 10 dirs + judge_summary.md
```

## Running

All commands assume `cwd = experiments/refusal/` and that you've installed the package at the repo root (`pip install -e .` from there).

### Oracle (Circuit Oracle, the paper's method)

```bash
# 1. Download Qwen3-4B + transcoders (one-time, GPU-side)
python3 scripts/download_weights.py

# 2. Run on all 10 prompts (GPU)
python3 scripts/run_all.py

# Or one prompt at a time
python3 scripts/run_all.py --slugs tiananmen-massacre
python3 scripts/run_all.py --slugs airport-bomb-smuggling --orchestrator anthropic/claude-opus-4-6
```

Per-prompt outputs land in `exp/exp-suppression-{slug}-question/<timestamp>/`:
- `oracle_result.json` — full pipeline state (intervention scales, self-rating, ...)
- `elicitation.json` / `elicitation.md` — winning intervention
- `report.md` — narrative + control comparison
- `circuit.svg` — pinned BUILD circuit
- `pinned_ids.json` — Neuronpedia IDs for pinned features

### Diff-in-mean baseline (Arditi et al. 2024)

```bash
# from experiments/refusal/, GPU machine:
bash baselines/arditi/runpod_setup.sh                            # all 10 slugs, all 4 stages
bash baselines/arditi/runpod_setup.sh --slugs tiananmen-massacre # single slug
bash baselines/arditi/runpod_setup.sh --skip-fetch --skip-judge  # GPU stages only
```

Results land in `baselines/arditi/runs/refusal/<slug>/` (`baseline.txt`, `ablated.txt`, `meta.json`). Aggregate: `baselines/arditi/runs/refusal/judge_summary.md`.

## Reproducing Table 3 (compute-free)

The shipped `exp/` and `baselines/arditi/runs/` directories already contain the runs reported in the paper. To re-score the head-to-head numbers without re-running models:

```bash
python3 baselines/arditi/exp_judge.py        # judges oracle's exp/ runs
python3 baselines/arditi/llm_judge.py        # judges baseline's runs/refusal/ runs
```

Both produce JSON aggregates that match the per-prompt rows in Table 3.
