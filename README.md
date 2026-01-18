# ⚡ Coddy v2.0 "Godmode"

> **L'Assistente AI locale che gira sul metallo.**
> Nessuna cloud, nessuna API Key, pura potenza CPU su privacy assoluta.

Coddy è un assistente di programmazione avanzato progettato per hardware consumer (i7 + 32GB RAM).
Sfrutta la **Quantizzazione (GGUF)** e un'architettura **"Dual Brain"** per essere leggero come una piuma ma intelligente come un Coder.

---

## 🚀 Caratteristiche Godmode

- **🏎️ Motore C++ Nativo**: Passaggio da Python lento a `llama.cpp` ottimizzato per Intel/AMD.
- **🧠 Dual Brain**:
  - **Light (0.5B)**: Risposte istantanee per teoria e chiacchiere.
  - **Coder (1.5B)**: Si attiva _solo_ quando serve scrivere codice complesso.
- **📚 RAG Persistente**: Memoria a lungo termine su disco (Qdrant) che non satura la RAM.
- **🌍 Web Search**: Cerca su DuckDuckGo se la knowledge base locale non basta.
- **🌊 Streaming Matrix UI**: Codice colorato e formattato in tempo reale con `Rich`.
- **💻 CLI Potenziata**: Comandi `help`, `cls`, `exit` e status indicator intelligenti.
- **🇮🇹 Italiano Nativo**: System prompt sintonizzato per risposte rigorosamente in italiano.

---

## 🛠️ Installazione (2 Comandi)

### 1. Preparazione

Assicurati di avere Python 3.10+ installato.

```bash
pip install -r requirements.txt
python setup.py
```

_(Questo scaricherà ~1.5GB di modelli ottimizzati nella cartella `models/`)_

---

## 🎮 Utilizzo

### Chat Interattiva

La modalità classica. Coddy ricorda la conversazione.

```bash
python coddy.py
```

### One-Shot (Domanda Rapida)

Perfetto per risposte al volo senza entrare nel loop.

```bash
python coddy.py "Come faccio un foreach in Rust?"
```

### Modalità Online

Permette a Coddy di cercare su internet.

```bash
python coddy.py --online
```

---

## 🗂️ Knowledge Base (RAG)

Vuoi che Coddy impari qualcosa di nuovo?

1. Crea un file `.md` o `.txt` nella cartella `knowledge/`.
2. Incollaci dentro documentazione, appunti o snippet.
3. Avvia Coddy. **Fatto.** (Impara automaticamente all'avvio).

---

## ⚙️ Requisiti Tecnici

- **CPU**: Intel i5/i7 (11th gen+) o AMD Ryzen 5/7 (5000+).
- **RAM**: Almeno 16GB (32GB raccomandati per il Godmode fluido).
- **GPU**: Non richiesta (ma supportata se presente).

_Creato per girare 100% Offline e Privato. I tuoi dati restano sul tuo PC._
