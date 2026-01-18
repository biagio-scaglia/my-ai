import os

os.environ["HF_HUB_OFFLINE"] = "0"
from huggingface_hub import list_repo_files
import time

repos = [
    "Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF",
    "Qwen/Qwen2.5-0.5B-Instruct-GGUF",
    "bartowski/Qwen2.5-Coder-1.5B-Instruct-GGUF",
    "bartowski/Qwen2.5-0.5B-Instruct-GGUF",
]

print("🔍 Scanning Hugging Face Repos for GGUF files...")

for repo in repos:
    print(f"\n📂 Repo: {repo}")
    try:
        files = list_repo_files(repo_id=repo)
        ggufs = [f for f in files if f.endswith(".gguf") and "q4_k_m" in f.lower()]
        for g in ggufs:
            print(f"   - {g}")
        if not ggufs:
            print("   (No 'q4_k_m' GGUF files found)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
