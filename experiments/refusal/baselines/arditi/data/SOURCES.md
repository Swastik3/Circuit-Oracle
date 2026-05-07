# Contrastive pair sources

`refusal_train.json` is populated by `python -m baselines.arditi.fetch_data` on first run, then committed for reproducibility.

## What we use

| Side | Source | n |
|---|---|---|
| Harmful (suppressed) | AdvBench from `walledai/AdvBench` on HuggingFace, `prompt` column | 128 |
| Harmless (complied)  | Alpaca-Cleaned (`yahma/alpaca-cleaned`), instructions with empty `input` | 128 |

Selection: `seed=42` deterministic shuffle of each pool, take first 128.

## What Arditi actually uses (full recipe)

The Arditi paper's harmful pool is broader than just AdvBench. From their `dataset/generate_datasets.ipynb`:

| Source | n | Notes |
|---|---|---|
| AdvBench | up to 128 | `harmful_behaviors.csv`, original `goal` column (HF mirror `walledai/AdvBench` renamed it to `prompt`) |
| MaliciousInstruct | up to 128 | Princeton-SysML benchmark |
| TDC2023 | up to 128 | CAIS Trojan Detection Challenge dev+test |

The three sources are concatenated and deduped, then capped at `n_train=128` total. For harmless, Arditi uses `tatsu-lab/alpaca` (we use `yahma/alpaca-cleaned`, near-identical).

### Why we use AdvBench only

- AdvBench alone has 520 prompts — at n=128 with seed=42 that's a 24% subsample, plenty of phrasing diversity.
- One source = simpler `fetch_data.py`, no inter-source dedup logic, fewer dataset dependencies.
- The diff-in-mean direction is empirically robust to harmful-pool composition (Arditi's ablations show similar directions across pool subsets).

If extraction underperforms (e.g. the chosen direction gives weak refusal-drop on val, or the locked-10 ablation results look bias-against-AdvBench-phrasing), expand `fetch_data.py:fetch_refusal()` to load and concatenate MaliciousInstruct + TDC2023:

```python
malicious = load_dataset("walledai/MaliciousInstruct", split="train")
tdc = load_dataset("walledai/TDC23-RedTeaming", split="dev")  # check exact slug on HF
harmful_pool = (
    [r["prompt"] for r in advbench]
    + [r["prompt"] for r in malicious]
    + [r["prompt"] for r in tdc]
)
```

Then dedup and shuffle.

## Out-of-sample discipline

We do NOT explicitly dedup the train pool against the 10 locked eval prompts. Two reasons:

1. **Distribution mismatch**: our locked prompts were LLM-generated inspired by HarmBench categories — a different distribution from AdvBench. Verbatim or near-verbatim overlap is unlikely.
2. **Diff-in-mean averaging**: each prompt contributes 1/128 ≈ 0.8% to the direction. Any incidental near-duplicate has negligible effect on the extracted direction.

If you want to audit overlap, eyeball `refusal_train.json` against `circuit-oracle-dev-causal/data/prompts.json` after fetch.

## Eval set

The 10 locked eval prompts live at `circuit-oracle-dev-causal/data/prompts.json` and are *never* read into the training pool. `apply_direction.py` reads that file directly.

## Reproducibility

```bash
python -m baselines.arditi.fetch_data --seed 42 --n 128
```

Deterministic given the seed and upstream dataset versions. If AdvBench or Alpaca update, the materialized `refusal_train.json` will drift; re-run and commit the new file.
