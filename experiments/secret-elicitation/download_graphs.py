#!/usr/bin/env python3
"""Download pre-computed taboo + sibling-base attribution graphs from HuggingFace.

For each of the 8 evaluated taboo LoRAs we ship 6 prompts × 2 graphs (taboo +
base sibling) = 12 .pt files per model. Total ~96 graphs. They live in a
HuggingFace dataset repo and sync into ./graphs/ next to the runner.

Usage:
    python3 experiments/secret-elicitation/download_graphs.py
    python3 experiments/secret-elicitation/download_graphs.py --hf-repo your-org/circuit-oracle-graphs
"""

from __future__ import annotations

import argparse
from pathlib import Path

# TODO: replace with the actual HuggingFace dataset repo once uploaded.
DEFAULT_HF_REPO = "TODO-org/circuit-oracle-graphs"
DEFAULT_HF_SUBFOLDER = "taboo_graphs"

_HERE = Path(__file__).resolve().parent
DEFAULT_LOCAL_DIR = _HERE / "graphs"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hf-repo", default=DEFAULT_HF_REPO,
                   help="HuggingFace dataset repo id (org/name).")
    p.add_argument("--hf-subfolder", default=DEFAULT_HF_SUBFOLDER,
                   help="Subfolder inside the HF repo containing the .pt files.")
    p.add_argument("--local-dir", default=str(DEFAULT_LOCAL_DIR),
                   help="Where to download into (default: ./graphs/ next to this script).")
    args = p.parse_args()

    if "TODO" in args.hf_repo:
        raise SystemExit(
            "Set --hf-repo to a real HuggingFace dataset id, or edit DEFAULT_HF_REPO "
            "in this file once the dataset is uploaded."
        )

    from huggingface_hub import snapshot_download

    local_dir = Path(args.local_dir)
    local_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {args.hf_repo}:{args.hf_subfolder}/ → {local_dir}")
    snapshot_download(
        repo_id=args.hf_repo,
        repo_type="dataset",
        allow_patterns=f"{args.hf_subfolder}/*.pt",
        local_dir=str(local_dir.parent),
        local_dir_use_symlinks=False,
    )
    print(f"Done. Graphs in {local_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
