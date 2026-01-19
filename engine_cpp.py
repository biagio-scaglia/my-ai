import os

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None
    print("[ERROR] llama-cpp-python non trovato. Esegui: pip install llama-cpp-python")


class CoddyEngine2:
    def __init__(self, model_dir="models"):
        """
        Motore v2.0 basato su llama.cpp.
        Gestisce DUE modelli in RAM simultaneamente (Godmode).
        Auto-Tuning powered by HardwareProfiler.
        """
        from src.profiler import HardwareProfiler
        from src.context_awareness import ContextAwareness

        # Load Hardware Profile
        self.profiler = HardwareProfiler()
        self.config = self.profiler.get_config()

        # Init Context Awareness
        self.scanner = ContextAwareness()
        self.project_context = self.scanner.get_system_prompt_injection()
        print(f"👁️ [Mini LSP] {self.scanner.stack_summary}")

        self.model_dir = model_dir
        self.n_ctx = self.config["n_ctx"]
        self.n_threads = self.config["cpu_threads"]
        self.n_batch = self.config["n_batch"]

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

        print("[Engine v2] Caricamento CODER (1.5B)...")
        self.llm_coder = Llama(
            model_path=self.path_coder,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_batch=self.n_batch,
            verbose=False,
        )

        print("[Engine v2] Caricamento LIGHT (0.5B)...")
        self.llm_light = Llama(
            model_path=self.path_light,
            n_ctx=self.n_ctx // 2,  # Contesto minore per il light
            n_threads=self.n_threads,
            n_batch=self.n_batch,
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
        # Inject Context into System Prompt
        working_history = [msg.copy() for msg in history]

        if self.project_context:
            # Check if system message exists
            if working_history[0]["role"] == "system":
                if "[CONTEXT AWARENESS]" not in working_history[0]["content"]:
                    working_history[0]["content"] += self.project_context
            else:
                # Insert system message
                working_history.insert(
                    0,
                    {
                        "role": "system",
                        "content": "You are Coddy." + self.project_context,
                    },
                )

        # Parse ultima query
        last_msg = working_history[-1]["content"]

        if model_type == "auto":
            target = self.route_query(last_msg)
        else:
            target = model_type

        llm = self.llm_coder if target == "coder" else self.llm_light
        # print(f"[DEBUG] Usando modello: {target.upper()}")

        # Llama.cpp chat format
        stream = llm.create_chat_completion(
            messages=working_history,
            max_tokens=2048,
            temperature=0.4 if target == "coder" else 0.7,
            stream=True,
            stop=["<|im_end|>", "<|endoftext|>"],
        )

        for chunk in stream:
            if "content" in chunk["choices"][0]["delta"]:
                yield chunk["choices"][0]["delta"]["content"]
