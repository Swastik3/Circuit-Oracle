#!/usr/bin/env python3
"""Launch the local autointerp FastAPI shim that mimics Neuronpedia.

Default config targets the qwen3-8b-transcoders feature cache used by the
ELK / taboo experiments. Override paths via flags or AUTOINTERP_* env vars.

Example:
    OPENROUTER_API_KEY=sk-or-... python experiments/secret-elicitation/run_autointerp_server.py
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_GIT_ROOT = _HERE.parent.parent

DEFAULT_FEATURES_DIR = str(
    _GIT_ROOT
    / "weights"
    / "hf_cache"
    / "hub"
    / "models--mwhanna--qwen3-8b-transcoders"
    / "snapshots"
    / "dc677109cde096a85d03fff4f73a3ec88e7e2105"
    / "features"
)
DEFAULT_CACHE_DIR = str(_HERE / "autointerp_cache")


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--features-dir", default=DEFAULT_FEATURES_DIR)
    p.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    p.add_argument("--model", default="minimax/minimax-m2.7",
                   help="Autointerp LLM (OpenRouter model id).")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--reload", action="store_true")
    args = p.parse_args()

    load_env_file(_GIT_ROOT / ".env")
    sys.path.insert(0, str(_GIT_ROOT / "src"))

    if not os.environ.get("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY not set (env or .env).", file=sys.stderr)
        return 1

    Path(args.cache_dir).mkdir(parents=True, exist_ok=True)
    os.environ["AUTOINTERP_FEATURES_DIR"] = args.features_dir
    os.environ["AUTOINTERP_CACHE_DIR"] = args.cache_dir
    os.environ["AUTOINTERP_MODEL"] = args.model

    import uvicorn
    print(
        f"Serving local autointerp on http://{args.host}:{args.port}\n"
        f"  features_dir = {args.features_dir}\n"
        f"  cache_dir    = {args.cache_dir}\n"
        f"  model        = {args.model}\n"
        f"Point ToolContext.neuronpedia_base_url at this server."
    )
    uvicorn.run(
        "circuit_oracle.autointerp_server:create_app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=True,
        workers=8
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
