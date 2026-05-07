import os

# Must be set before importing huggingface_hub so the cache is directed correctly.
# Resolve to absolute path so the script works from any working directory.
if "HF_HOME" not in os.environ:
    os.environ["HF_HOME"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "weights", "hf_cache")

import huggingface_hub  # noqa: E402


MODELS = [
    ("Qwen/Qwen3-4B", "instruction-tuned model"),
    ("mwhanna/qwen3-4b-transcoders", "transcoders"),
]


def download_weights() -> None:
    token = os.environ.get("HF_TOKEN") or None

    # Ensure output directories exist
    os.makedirs("weights/hf_cache", exist_ok=True)
    os.makedirs("weights/graphs", exist_ok=True)

    for repo_id, description in MODELS:
        print(f"\n[download_weights] Downloading {description}: {repo_id} ...")
        local_dir = huggingface_hub.snapshot_download(
            repo_id=repo_id,
            token=token,
        )
        print(f"[download_weights] {repo_id} saved to: {local_dir}")

    print("\n[download_weights] All downloads complete.")
    print("[download_weights] weights/graphs/ directory is ready for circuit output.")


if __name__ == "__main__":
    download_weights()
