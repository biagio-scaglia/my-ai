import os
import glob
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models


class RagEngine:
    def __init__(
        self,
        knowledge_dir="knowledge",
        db_path="qdrant_data",
        model_name="all-MiniLM-L6-v2",
    ):
        """
        Inizializza il motore RAG con Qdrant (Persistent Storage).
        """
        self.knowledge_dir = knowledge_dir
        self.collection_name = "coddy_knowledge"

        # Inizializza Qdrant Locale (File basato, niente server richiesto)
        print(f"Inizializzazione Qdrant DB in: {db_path}...")
        self.client = QdrantClient(path=db_path)

        # Carica il modello di embedding
        print(f"Caricamento modello Embedding: {model_name}...")
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_size = self.model.get_sentence_embedding_dimension()

            # Crea la collezione se non esiste
            self._ensure_collection()

            # Indicizza i documenti
            self.load_knowledge()
            print("Motore RAG (Qdrant) pronto.")
        except Exception as e:
            print(f"Errore inizializzazione RAG: {e}")
            self.client = None

    def _ensure_collection(self):
        """Assicura che la collezione Qdrant esista con la configurazione corretta."""
        collections = self.client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.embedding_size, distance=models.Distance.COSINE
                ),
            )

    def load_knowledge(self):
        """
        Legge i file, crea embedding e li salva su Qdrant se non esistono.
        Nota: Per ora è un approccio semplice (svuota e ricarica o upsert cieco).
        Per produzione si dovrebbe usare hashing dei file per evitare ri-embedding.
        """
        print("Scansione documenti...")
        files = glob.glob(
            os.path.join(self.knowledge_dir, "**/*.md"), recursive=True
        ) + glob.glob(os.path.join(self.knowledge_dir, "**/*.txt"), recursive=True)

        if not files:
            print("Nessun file trovato nella knowledge base.")
            return

        # Recupera conteggio attuale per info
        count_before = self.client.count(self.collection_name).count

        # Batch processing
        batch_points = []

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                # Chunking per paragrafi
                chunks = text.split("\n\n")
                for chunk in chunks:
                    chunk = chunk.strip()
                    if not chunk:
                        continue

                    # Genera ID univoco (deterministic basato sul contenuto per evitare duplicati esatti)
                    doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk))

                    # Calcola embedding
                    vector = self.model.encode(chunk).tolist()

                    # Crea punto Qdrant
                    point = models.PointStruct(
                        id=doc_id,
                        vector=vector,
                        payload={"text": chunk, "source": os.path.basename(file_path)},
                    )
                    batch_points.append(point)

            except Exception as e:
                print(f"Errore lettura {file_path}: {e}")

        if batch_points:
            # Upsert (inserisce o aggiorna)
            self.client.upsert(
                collection_name=self.collection_name, points=batch_points
            )
            count_after = self.client.count(self.collection_name).count
            new_elements = count_after - count_before
            print(
                f"Knowledge Base aggiornata. Totale frammenti: {count_after} (+{new_elements} nuovi)."
            )

    def search(self, query, top_k=3):
        """
        Cerca i frammenti più rilevanti usando la ricerca vettoriale di Qdrant.
        """
        if not self.client:
            return []

        query_vector = self.model.encode(query).tolist()

        search_result = self.client.search(
            collection_name=self.collection_name, query_vector=query_vector, limit=top_k
        )

        results = []
        for hit in search_result:
            if hit.score > 0.45:  # Soglia di rilevanza
                results.append(
                    {
                        "text": hit.payload["text"],
                        "source": hit.payload["source"],
                        "score": hit.score,
                    }
                )

        return results
