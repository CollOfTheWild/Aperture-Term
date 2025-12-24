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

def get_repo_ggufs(repo_id: str):
    """
    List .gguf files in a specific Hugging Face repository.
    """
    api = HfApi()
    try:
        files = api.list_repo_files(repo_id)
        return [f for f in files if f.endswith(".gguf")]
    except Exception as e:
        print(f"Error listing repo files: {e}")
        return []

def download_model(repo_id: str, filename: str, progress_callback=None):
    """
    Download a specific GGUF file from HF.
    """
    ensure_model_dir()
    try:
        # hf_hub_download handles caching and partial downloads
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False
        )
        return path
    except Exception as e:
        print(f"Download Error: {e}")
        return None
