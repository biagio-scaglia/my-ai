import os

os.environ["HF_HUB_OFFLINE"] = "0"
from huggingface_hub import hf_hub_download

# Directory modelli
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Mappa modelli GGUF (Quantized)
# Usiamo Q4_K_M per bilanciamento perfetto RAM/Velocità su i7-1370P
MODELS = {
    "coder": {
        "repo_id": "bartowski/Qwen2.5-Coder-1.5B-Instruct-GGUF",
        "filename": "Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf",
    },
    "light": {
        "repo_id": "bartowski/Qwen2.5-0.5B-Instruct-GGUF",
        "filename": "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
    },
}


def download_model(key, info):
    print(f"\n⬇️  Scaricamento {key.upper()} ({info['filename']})...")
    try:
        path = hf_hub_download(
            repo_id=info["repo_id"],
            filename=info["filename"],
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False,
        )
        print(f"✅ Completato: {path}")
    except Exception as e:
        print(f"❌ Errore scaricamento {key}: {e}")


if __name__ == "__main__":
    print("🚀 Coddy v2.0 - GGUF Model Downloader")
    print("Preparazione modelli ottimizzati per CPU (Q4_K_M)...")

    for key, info in MODELS.items():
        download_model(key, info)

    print("\n✨ Tutti i modelli sono pronti in 'models/'.")
