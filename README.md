# Circuit Oracle

Code accompanying *Circuit Oracle: Automating Attribution Graph Analysis via Natural-Language Queries* (NeurIPS 2026 submission).

A frontier LLM is wrapped in a multi-agent harness that consumes pre-computed transcoder attribution graphs and answers safety-relevant natural-language questions about a target model. We evaluate it on three proxy tasks:

| # | Experiment | Paper section | Subject model | Folder |
|---|---|---|---|---|
| 1 | Spurious-correlation detection on probe circuits | §4 (Table 1) | Gemma-2-2B + PLT transcoders | [`experiments/spurious-correlations/`](experiments/spurious-correlations/) |
| 2 | Secret elicitation on taboo LoRAs | §5 (Table 2) | Qwen3-8B + transcoders | [`experiments/secret-elicitation/`](experiments/secret-elicitation/) |
| 3 | Suppression-jailbreaking via intervention | §6 (Table 3) | Qwen3-4B + transcoders | [`experiments/refusal/`](experiments/refusal/) |

## Layout

```
.
├── src/
│   ├── circuit_oracle/        # multi-agent orchestrator + tools (shared)
│   └── circuit_tracer/        # vendored — attribution + intervention runtime
├── experiments/
│   ├── refusal/               # §6 — suppression-jailbreaking
│   ├── spurious-correlations/ # §4 — probe circuits
│   └── secret-elicitation/    # §5 — taboo LoRAs
├── pyproject.toml             # `pip install -e .` from here
└── .env.example               # copy → .env, fill in API keys
```

## Setup

```bash
git clone <this-repo> && cd circuit-analysis
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env  # then fill in ANTHROPIC_API_KEY / OPENROUTER_API_KEY / HF_TOKEN
```

GPU is required for graph extraction (Gemma-2-2B / Qwen3-4B / Qwen3-8B forward passes). The oracle agents themselves call hosted LLMs via API and run anywhere.

## Pre-computed attribution graphs

The probe and taboo experiments consume `.pt` attribution graphs that are too large for git. Each experiment ships a `download_graphs.py` script that pulls them from a HuggingFace dataset:

```bash
python3 experiments/spurious-correlations/download_graphs.py
python3 experiments/secret-elicitation/download_graphs.py
```

(The HF repo URL is set as a placeholder in those scripts — fill in once the dataset is uploaded.)

## Running each experiment

See the README in each experiment folder for the exact commands, expected outputs, and where the paper's table values live.

- [Spurious-correlation detection (§4)](experiments/spurious-correlations/README.md)
- [Secret elicitation (§5)](experiments/secret-elicitation/README.md)
- [Suppression-jailbreaking (§6)](experiments/refusal/README.md)
