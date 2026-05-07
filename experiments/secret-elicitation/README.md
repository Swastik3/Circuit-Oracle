# Secret Knowledge Elicitation on Taboo LoRAs

Paper §5 (Table 2). The oracle sees a taboo-LoRA attribution graph alongside a same-prompt sibling graph from the base Qwen3-8B and decides which 20-word menu option is the LoRA's hidden secret. Closed-mode evaluation in the main paper; open-vocab in Appendix F.1.

Subject model: `Qwen/Qwen3-8B` + `mwhanna/qwen3-8b-transcoders`. Taboo LoRAs from [Karvonen et al. 2025](https://huggingface.co/adamkarvonen).

## Folder layout

```
secret-elicitation/
├── README.md                                # this file
├── download_graphs.py                       # fetch pre-computed taboo + base sibling graphs
├── build_taboo_graphs.py                    # GPU: builds the .pt graphs from scratch
├── run_oracle_on_taboo.py                   # closed-mode oracle (Table 2)
├── run_oracle_on_taboo_no_options.py        # open-vocab oracle (Appendix F.1)
├── eval_oracle_taboo.py                     # judge for closed-mode
├── eval_oracle_taboo_no_options.py          # judge for open-vocab
├── run_autointerp_server.py                 # local feature-description server (Qwen3-8B transcoders aren't on Neuronpedia)
├── print_table.sh                           # render side-by-side Table 2
├── autointerp_cache/                        # cached per-feature LLM descriptions
├── graphs/                                  # populated by download_graphs.py (gitignored)
├── oracle_taboo_results/                    # closed-mode outputs (eval.json + per-run dirs)
└── oracle_taboo_results_no_options/         # open-vocab outputs
```

8 of 20 taboo models × 6 prompts each = 48 runs per model. Each prompt is a (user request → "The word is") prefill pair.

## Running

`cwd = experiments/secret-elicitation/` for everything below.

### 0. One-time downloads

```bash
python3 download_graphs.py     # fetches taboo + sibling base attribution graphs
```

To regenerate from scratch on a GPU (slow):
```bash
python3 build_taboo_graphs.py  # iterates over taboo models × prompts
```

### 1. Local autointerp server (required)

The Qwen3-8B transcoders are not on Neuronpedia, so the oracle's `inspect_feature` tool talks to a local FastAPI shim that pulls feature descriptions from the transcoder's local feature cache and labels them via OpenRouter.

In a separate terminal:
```bash
OPENROUTER_API_KEY=sk-or-... python3 run_autointerp_server.py
# Listens on http://127.0.0.1:8765
```

Override `--features-dir` if your `mwhanna/qwen3-8b-transcoders` HF cache is elsewhere; `--cache-dir` defaults to `./autointerp_cache/` next to the script.

### 2. Oracle (paper's method)

```bash
# Closed-mode (paper's main result, Table 2)
python3 run_oracle_on_taboo.py

# Open-vocab (Appendix F.1)
python3 run_oracle_on_taboo_no_options.py
```

Per-run outputs land under `oracle_taboo_results/exp/<slug>/<timestamp>/` (or the `_no_options` sibling).

### 3. Reproducing Table 2 (compute-free)

The shipped `oracle_taboo_results/` already contains the 48 × 8 = 384 runs reported in the paper. Re-score:

```bash
python3 eval_oracle_taboo.py            # closed-mode  → oracle_taboo_results/eval.json
python3 eval_oracle_taboo_no_options.py # open-vocab   → oracle_taboo_results_no_options/eval.json

# Side-by-side rendering of Table 2 (oracle + projection baselines)
bash print_table.sh
```

`print_table.sh` consumes baseline result files from an external `BLS=...` directory (the SAE-proj / Trans-proj projection baselines, computed outside this repo). Set `BLS=/path/to/activation_oracles/experiments` before running.
