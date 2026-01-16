# Coddy - Il tuo Assistente di Programmazione Locale

Coddy è un assistente AI da terminale, progettato per girare interamente in locale sul tuo computer.
Usa un LLM specializzato (**Qwen2.5-Coder-1.5B**) per il coding e un sistema **RAG (Retrieval-Augmented Generation)** per imparare dai tuoi documenti personali.

## ✨ Caratteristiche "Godmode"

- **🧠 Doppio Cervello**:
  - **Coder (1.5B)**: Specializzato in scrittura codice, refactoring e architettura.
  - **Light (0.5B)**: Per chat veloci e domande teoriche.
- **⚡ CLI One-Shot**: Chiedi direttamente da terminale senza aprire la chat interattiva.
- **� File Generator**: Crea file automaticamente ("Creami un main.py") con protezione sovrascrittura.
- **�📚 RAG Autonomo**: Impara dai tuoi file e risponde contestualmente.
- **🇮🇹 Assistant Nativo**: Risposte e commenti al codice rigorosamente in Italiano.

## 🚀 Installazione Rapida

1.  **Requisiti**: Python 3.8+ & Git.
2.  **Setup**:
    ```bash
    pip install -r requirements.txt
    python download_models.py
    ```
    _(Scaricherà entrambi i modelli: Coder & Light)_

## 🎮 Utilizzo Avanzato

### 1. Chat Interattiva (Default: Coder)

```bash
python coddy.py
```

Coddy si avvia, indicizza la tua `knowledge/` e aspetta i tuoi ordini.

### 2. Cambio Modello

Coddy supporta due "cervelli":

- **Coder** (Default): `Qwen2.5-Coder-1.5B` - Ottimo per scrivere codice.
- **Light**: `Qwen2.5-0.5B` - Leggerissimo, per chat veloci.

Per cambiare modello all'avvio:

```bash
python coddy.py --model light
```

O per tornare al coder:

```bash
python coddy.py --model coder
```

### 3. Query Rapide (One-Shot)

Puoi fare una domanda diretta senza entrare nella chat:

```bash
python coddy.py "Come creo un array in C#?"
python coddy.py --model light "Chi era Dante?"
```

## 🧠 Knowledge Base (RAG con Qdrant)

Coddy **NON** viene addestrato (fine-tuning). Usa una tecnica chiamata **RAG (Retrieval-Augmented Generation)**.
I tuoi documenti vengono trasformati in vettori e salvati in un database locale veloce (**Qdrant**), permettendo a Coddy di trovare l'informazione giusta al momento giusto.

1.  Metti i tuoi file `.md` o `.txt` nella cartella `knowledge/`.
2.  All'avvio, Coddy aggiornerà automaticamente il database vettoriale.
3.  Quando fai una domanda, lui cercherà i pezzi rilevanti e li userà per risponderti.

**Esempi di file da aggiungere:**

- Il tuo `CV.md` (già incluso!)
- Appunti di progetti (`progetto_x.md`)
- Guide specifiche o documentazione tecnica.

## 🛠️ Tecnologie

- [Rich](https://github.com/Textualize/rich) - UI Terminale
- [Hugging Face Transformers](https://huggingface.co/docs/transformers) - LLM Engine
- [Sentence Transformers](https://sbert.net/) - RAG Embedding
- [Qdrant](https://qdrant.tech/) - Vector Database Locale
- [Qwen2.5](https://huggingface.co/Qwen) - Il modello LLM di base

---

_Fatto con ❤️ da Biagio_
