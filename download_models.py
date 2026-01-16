import os

# Force online mode explicitly before other imports
os.environ["HF_HUB_OFFLINE"] = "0"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from huggingface_hub import snapshot_download


def download_models():
    print("Inizio download dei modelli (ONLINE MODE)...")

    # 1. Download Models
    models = ["Qwen/Qwen2.5-Coder-1.5B-Instruct", "Qwen/Qwen2.5-0.5B-Instruct"]

    for model in models:
        print(f"\nScaricando LLM: {model}...")
        try:
            snapshot_download(repo_id=model)
            print(f"✅ {model} scaricato.")
        except Exception as e:
            print(f"❌ Errore scaricamento {model}: {e}")

    # 2. Download Embedding Model for RAG
    print("\n2. Scaricando all-MiniLM-L6-v2 (per RAG)...")
    try:
        snapshot_download(repo_id="sentence-transformers/all-MiniLM-L6-v2")
        print("✅ Modello RAG scaricato.")
    except Exception as e:
        print(f"❌ Errore scaricamento Modello RAG: {e}")
        return

    print(
        "\n✅ Tutti i modelli sono stati scaricati! Ora puoi lanciare 'python coddy.py'."
    )


if __name__ == "__main__":
    download_models()
