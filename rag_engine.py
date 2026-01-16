import os
import glob
import torch
from sentence_transformers import SentenceTransformer, util


class RagEngine:
    def __init__(self, knowledge_dir="knowledge", model_name="all-MiniLM-L6-v2"):
        """
        Inizializza il motore RAG.
        """
        self.knowledge_dir = knowledge_dir
        self.documents = []  # Lista di (testo, sorgente)
        self.embeddings = None

        # Carica il modello di embedding
        print(f"Caricamento modello RAG: {model_name}...")
        try:
            self.model = SentenceTransformer(model_name)
            self.load_knowledge()
            print("Motore RAG pronto.")
        except Exception as e:
            print(f"Errore inizializzazione RAG: {e}")
            self.model = None

    def load_knowledge(self):
        """
        Carica i file dalla directory knowledge.
        Supporta file .md e .txt.
        Splitta il testo in chunk (per ora basico: per paragrafi).
        """
        self.documents = []
        files = glob.glob(
            os.path.join(self.knowledge_dir, "**/*.md"), recursive=True
        ) + glob.glob(os.path.join(self.knowledge_dir, "**/*.txt"), recursive=True)

        if not files:
            print("Nessun file trovato nella knowledge base.")
            return

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                # Chunking semplificato: dividiamo per doppio a capo (paragrafi)
                chunks = text.split("\n\n")
                for chunk in chunks:
                    if chunk.strip():
                        self.documents.append(
                            {
                                "text": chunk.strip(),
                                "source": os.path.basename(file_path),
                            }
                        )
            except Exception as e:
                print(f"Errore caricamento {file_path}: {e}")

        if self.documents:
            # Calcola embeddings per tutti i documenti
            texts = [doc["text"] for doc in self.documents]
            self.embeddings = self.model.encode(texts, convert_to_tensor=True)
            print(f"Indicizzati {len(self.documents)} frammenti di conoscenza.")

    def search(self, query, top_k=3):
        """
        Cerca i frammenti più rilevanti per la query.
        """
        if self.embeddings is None or not self.documents:
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]

        # Trova i top_k
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.documents)))

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            if score > 0.45:  # Soglia aumentata per ridurre falsi positivi
                results.append(self.documents[idx.item()])

        return results
