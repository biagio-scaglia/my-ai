import os
import json
import psutil

PROFILE_PATH = "coddy_profile.json"


class HardwareProfiler:
    """
    Analizza l'hardware del sistema per auto-calibrare Coddy.
    """

    def __init__(self):
        self.profile = self.load_profile()

    def detect_hardware(self):
        """
        Rileva CPU threads fisici/logici e RAM totale in GB.
        """
        cpu_count = psutil.cpu_count(logical=True)
        # Alcune CPU Intel 12th+ gen hanno P-cores ed E-cores.
        # Llama.cpp preferisce i thread fisici o count/2 per stabilità.
        physical_cores = psutil.cpu_count(logical=False) or (cpu_count // 2)

        mem_info = psutil.virtual_memory()
        total_ram_gb = round(mem_info.total / (1024**3), 1)

        return physical_cores, total_ram_gb

    def optimize_config(self):
        """
        Genera una configurazione ottimale basata sull'hardware.
        """
        p_cores, ram_gb = self.detect_hardware()

        # Calcolo Threads: Lasciamo un po' di respiro al sistema
        # Se abbiamo pochi core (<=4), usiamoli quasi tutti - 1.
        # Se ne abbiamo tanti, stiamo sui fisici per efficienza cache.
        safe_threads = max(1, p_cores - 2) if p_cores > 6 else max(1, p_cores - 1)

        # Calcolo Context: Dipende dalla RAM.
        # Modelli Q4 occupano ~1-2GB + contesto.
        # >16GB RAM -> 8192 (O più se supportato)
        # >32GB RAM -> 16384 (Godmode vero)
        if ram_gb >= 30:
            n_ctx = 16384
            n_batch = 1024
        elif ram_gb >= 14:
            n_ctx = 8192
            n_batch = 512
        else:
            n_ctx = 2048  # Fallback per macchine "povere"
            n_batch = 256

        return {
            "cpu_threads": safe_threads,
            "ram_gb": ram_gb,
            "n_ctx": n_ctx,
            "n_batch": n_batch,
            "gpu_offload": False,  # Placeholder per futuro supporto GPU
        }

    def load_profile(self):
        if os.path.exists(PROFILE_PATH):
            try:
                with open(PROFILE_PATH, "r") as f:
                    print(
                        f"⚡ [Profiler] Caricamento profilo esistente da {PROFILE_PATH}"
                    )
                    return json.load(f)
            except Exception:
                pass

        print("⚡ [Profiler] Primo avvio: Analisi Hardware in corso...")
        config = self.optimize_config()
        self.save_profile(config)
        print(
            f"✅ [Profiler] Hardware calibrato: {config['cpu_threads']} Threads, {config['n_ctx']} Context"
        )
        return config

    def save_profile(self, config):
        with open(PROFILE_PATH, "w") as f:
            json.dump(config, f, indent=4)

    def get_config(self):
        return self.profile


if __name__ == "__main__":
    # Test Rapido
    p = HardwareProfiler()
    print(json.dumps(p.get_config(), indent=2))
