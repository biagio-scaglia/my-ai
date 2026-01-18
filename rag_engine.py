import os
import glob
import uuid


class RagEngine:
    def __init__(
        self,
        knowledge_dir="knowledge",
        db_path="qdrant_data",
        model_name="all-MiniLM-L6-v2",
    ):
        """
        Inizializza il motore RAG con Qdrant (Persistent Storage).
        Usa Lazy Loading per le dipendenze pesanti.
        """
        self.knowledge_dir = knowledge_dir
        self.collection_name = "coddy_knowledge"
        self.db_path = db_path
        self.model_name = model_name
        self.client = None
        self.model = None

        # Lazy Loading delle dipendenze
        try:
            print(f"RAG: Importazione moduli pesanti (Lazy Loading)...")
            from sentence_transformers import SentenceTransformer
            from qdrant_client import QdrantClient
            from qdrant_client.http import models

            self.models = models

            # Inizializza Qdrant Locale
            print(f"RAG: Apertura DB in {self.db_path}...")
            # Tentiamo di forzare la locazione in memoria se path è "memory" (opzionale)
            self.client = QdrantClient(path=self.db_path)

            # Carica Modello Embedding
            print(f"RAG: Caricamento modello {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            self.embedding_size = self.model.get_sentence_embedding_dimension()

            self._ensure_collection()
            self.load_knowledge()
            print("RAG: Sistema pronto.")

        except ImportError as e:
            print(
                f"RAG Error: Modulo mancante ({e}). Esegui 'pip install -r requirements.txt'"
            )
        except Exception as e:
            print(f"RAG Error: Inizializzazione fallita ({e})")
            # Fallback sicuro: client None

    def _ensure_collection(self):
        """Assicura che la collezione esista."""
        if not self.client:
            return

        try:
            collections = self.client.get_collections()
            exists = any(
                c.name == self.collection_name for c in collections.collections
            )

            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=self.models.VectorParams(
                        size=self.embedding_size, distance=self.models.Distance.COSINE
                    ),
                )
        except Exception as e:
            print(f"RAG Init Collection Error: {e}")

    def load_knowledge(self):
        """Indicizza i file."""
        if not self.client:
            return

        files = glob.glob(
            os.path.join(self.knowledge_dir, "**/*.md"), recursive=True
        ) + glob.glob(os.path.join(self.knowledge_dir, "**/*.txt"), recursive=True)

        if not files:
            return

        try:
            count_before = self.client.count(self.collection_name).count
        except:
            count_before = 0

        batch_points = []

        print("RAG: Scansione nuovi documenti...")
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                chunks = text.split("\n\n")
                for chunk in chunks:
                    chunk = chunk.strip()
                    if not chunk:
                        continue

                    doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk))
                    vector = self.model.encode(chunk).tolist()

                    point = self.models.PointStruct(
                        id=doc_id,
                        vector=vector,
                        payload={"text": chunk, "source": os.path.basename(file_path)},
                    )
                    batch_points.append(point)
            except Exception as e:
                print(f"Errore lettura {file_path}: {e}")

        if batch_points:
            try:
                self.client.upsert(
                    collection_name=self.collection_name, points=batch_points
                )
                count_after = self.client.count(self.collection_name).count
                if count_after > count_before:
                    print(
                        f"RAG: +{count_after - count_before} nuovi frammenti indicizzati."
                    )
            except Exception as e:
                print(f"RAG Upsert Error: {e}")

    def search(self, query, top_k=3):
        """Esegue la ricerca vettoriale."""
        if not self.client:
            return []

        try:
            query_vector = self.model.encode(query).tolist()

            # --- FIX CRITICO ---
            # QdrantClient su alcune versioni/config locali potrebbe non esporre .search
            # Usiamo query_points che è l'API standard più robusta
            search_result = self.client.query_points(
                collection_name=self.collection_name, query=query_vector, limit=top_k
            ).points

            results = []
            for hit in search_result:
                if hit.score > 0.45:
                    results.append(
                        {
                            "text": hit.payload["text"],
                            "source": hit.payload["source"],
                            "score": hit.score,
                        }
                    )
            return results
        except Exception as e:
            print(f"RAG Search Error (final try): {e}")
            return []

    def close(self):
        """Chiude la connessione al DB in modo pulito."""
        if self.client:
            try:
                # Evita errori se Python sta chiudendo (sys.meta_path None)
                import sys

                if sys.meta_path is None:
                    return
                self.client.close()
            except:
                pass
            finally:
                self.client = None
