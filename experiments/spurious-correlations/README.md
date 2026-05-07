# Spurious-Correlation Detection on Probe Circuits

Paper §4 (Table 1). Given two attribution graphs from the same prompt — one toward a *biased* probe (trained on stereotype-correlated data) and one toward an *unbiased* probe (trained on a balanced split) — the oracle decides whether the biased decision is driven by spurious or causal features. Head-to-head against SAE-cos and Trans-cos cosine-similarity baselines.

Subject model: `google/gemma-2-2b` + Gemma-Scope per-layer transcoders (PLTs).
Orchestrator: Minimax-M2.7 with DeepSeek-V3.2 subagents (configurable).

## Folder layout

```
spurious-correlations/
├── README.md                       # this file
├── download_graphs.py              # fetch pre-computed .pt graphs from HF
├── run_oracle_on_probes.py         # main oracle entry point
├── eval_oracle_feature_counts.py   # primary judge: gpt-5.4-mini counts spurious vs causal features
├── judge_sae_features.py           # baseline judge: Minimax-M2.7 verdict on SAE-cos / Trans-cos rankings
├── rank_sae_features_by_probe.py   # builds the SAE-cos / Trans-cos cosine rankings
├── circuit_extraction.py           # GPU: builds .pt attribution graphs from probes
├── run_extraction_batch.py         # batch driver around circuit_extraction.py
├── prompts.json                    # 10 prompts × 4 datasets × 2 probe types = 80 settings
├── adapters/                       # dataset adapters (BIB, CivilComments, MultiNLI)
├── probe_extraction/               # probe training code + configs
├── probe_circuits/                 # populated by download_graphs.py (gitignored)
└── oracle_probe_results/           # shipped oracle outputs — one subdir per (slug)
```

Datasets: `bib_journalist_dietitian` (BIB-JD), `bib_nurse_professor` (BIB-NP), `civil_comments` (CC), `multinli` (MNLI). `bib_surgeon_teacher` was excluded from the paper.

## Running

`cwd = experiments/spurious-correlations/` for everything below; package installed via `pip install -e .` at repo root.

### 0. One-time downloads

```bash
python3 download_graphs.py    # fetches probe attribution-graph .pt files
```

The probe weight checkpoints live in `probe_extraction/probes/`. To regenerate from scratch (GPU), see `probe_extraction/README.md`.

### 1. Oracle (paper's method)

```bash
# All 80 settings
python3 run_oracle_on_probes.py

# Filter
python3 run_oracle_on_probes.py --dataset bib_journalist_dietitian
python3 run_oracle_on_probes.py --probe-type biased --method correct
python3 run_oracle_on_probes.py --slugs bib_journalist_dietitian-biased-probe-correct
python3 run_oracle_on_probes.py --concern "Which features encode gender bias?"
```

Per-setting outputs land in `oracle_probe_results/<slug>/<timestamp>/` with `report.md`, `oracle_result.json`, `circuit.svg`.

### 2. Cosine baselines (SAE-cos, Trans-cos)

```bash
# GPU: rank features by cosine similarity to probe weights
python3 rank_sae_features_by_probe.py --all                # all 4 datasets, both SAE + transcoder
python3 rank_sae_features_by_probe.py --dataset bib_journalist_dietitian --type sae

# CPU/API: ask Minimax-M2.7 for a YES/NO spurious-vs-causal verdict on the rankings
python3 judge_sae_features.py
```

### 3. Reproducing Table 1 (compute-free)

The shipped `oracle_probe_results/` already contains the runs. Re-score:

```bash
python3 eval_oracle_feature_counts.py
```

This calls `gpt-5.4-mini` on each report.md, counts spurious / causal features, and reports per-dataset accuracy matching Table 1.
