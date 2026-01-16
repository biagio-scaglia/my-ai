import sys

print("Importing modules...")
try:
    import torch
    import transformers
    from rich.console import Console

    print("Imports successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
print(f"Loading model {MODEL_NAME}...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    # Load on CPU for safety in this test environment if needed, or let auto handle it
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Model load failed: {e}")
    sys.exit(1)
print("Test passed.")
