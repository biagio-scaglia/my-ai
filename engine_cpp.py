import os
import sys

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None
    print("[ERROR] llama-cpp-python non trovato. Esegui: pip install llama-cpp-python")


class CoddyEngine2:
    def __init__(self, model_dir="models", n_ctx=8192, n_threads=10):
        """
        Motore v2.0 basato su llama.cpp.
        Gestisce DUE modelli in RAM simultaneamente (Godmode).
        """
        self.model_dir = model_dir
        self.n_ctx = n_ctx
        self.n_threads = n_threads

        # Paths
        self.path_coder = os.path.join(
            model_dir, "Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf"
        )
        self.path_light = os.path.join(model_dir, "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf")

        self.llm_light = None

    def close(self):
        """Libera la memoria dei modelli."""
        if self.llm_coder:
            del self.llm_coder
            self.llm_coder = None
        if self.llm_light:
            del self.llm_light
            self.llm_light = None
        # Force garbage collection
        import gc

        gc.collect()

        # Carica i modelli (Lazy load nel metodo start per gestire errori gracefully)

    def start(self):
        """Carica fisicamente i modelli in RAM."""
        if not os.path.exists(self.path_coder) or not os.path.exists(self.path_light):
            raise FileNotFoundError(
                "Modelli GGUF non trovati in 'models/'. Esegui download_models_gguf.py"
            )

        print("⚡ [Engine v2] Caricamento CODER (1.5B)...")
        self.llm_coder = Llama(
            model_path=self.path_coder,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            verbose=False,
        )

        print("⚡ [Engine v2] Caricamento LIGHT (0.5B)...")
        self.llm_light = Llama(
            model_path=self.path_light,
            n_ctx=self.n_ctx // 2,  # Contesto minore per il light
            n_threads=self.n_threads,
            verbose=False,
        )
        print("✅ [Godmode] Doppio Cervello Attivo (RAM OK).")

    def route_query(self, query):
        """
        Classifier Euristico per scegliere il modello.
        Ritorna 'coder' o 'light'.
        """
        triggers_coder = [
            "codice",
            "script",
            "funzione",
            "class",
            "debug",
            "fix",
            "refactor",
            "python",
            "javascript",
            "java",
            "ruby",
            "rails",
            "sql",
            "error",
        ]

        q_lower = query.lower()

        # Se c'è codice esplicito o keyword tecniche -> Coder
        if any(t in q_lower for t in triggers_coder):
            return "coder"

        # Default -> Light (molto più veloce per chiacchiere)
        return "light"

    def stream_chat(self, history, model_type="auto"):
        """
        Genera risposta in streaming.
        model_type: 'auto', 'coder', 'light'
        """
        # Parsing ultima query per routing
        last_msg = history[-1]["content"]

        if model_type == "auto":
            target = self.route_query(last_msg)
        else:
            target = model_type

        llm = self.llm_coder if target == "coder" else self.llm_light
        # print(f"[DEBUG] Usando modello: {target.upper()}")

        # Llama.cpp chat format
        # Converte history se necessario, ma llama.cpp .create_chat_completion accetta dict
        stream = llm.create_chat_completion(
            messages=history,
            max_tokens=2048,
            temperature=0.4 if target == "coder" else 0.7,
            stream=True,
        )

        for chunk in stream:
            if "content" in chunk["choices"][0]["delta"]:
                yield chunk["choices"][0]["delta"]["content"]
