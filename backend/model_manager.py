import os
from huggingface_hub import HfApi, hf_hub_download
from pathlib import Path

# Where models are stored locally
MODEL_DIR = Path.home() / ".aperture/models"

def ensure_model_dir():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

def search_models(query: str, limit: int = 10):
    """
    Search Hugging Face Hub for GGUF models.
    """
    api = HfApi()
    try:
        # We filter for 'gguf' in the tag or name to ensure compatibility
        models = api.list_models(
            search=query,
            limit=limit,
            sort="downloads",
            direction="-1",
            filter="gguf"
        )
        return [
            {
                "id": m.id,
                "downloads": m.downloads,
                "likes": m.likes,
                "created_at": str(m.created_at)
            }
            for m in models
        ]
    except Exception as e:
        print(f"HF Search Error: {e}")
        return []

def list_local_models():
    """
    List GGUF files in the local model directory.
    """
    ensure_model_dir()
    files = list(MODEL_DIR.glob("*.gguf"))
    return [
        {
            "name": f.name,
            "path": str(f),
            "size_mb": f.stat().st_size / (1024 * 1024)
        }
        for f in files
    ]

# Note: Actual downloading is a blocking long-running process.
# In a real app, this should be handled by a separate worker/thread that reports progress.
# For this MVP step, we will just define the function.
