from rag_engine import RagEngine

print("Initializing RAG Engine...")
rag = RagEngine()

query = "consigliami progetti"
print(f"\nQuery: {query}")
results = rag.search(query)

if results:
    print(f"Found {len(results)} results:")
    for i, res in enumerate(results):
        print(f"--- Result {i + 1} (Source: {res['source']}) ---")
        print(res["text"][:200] + "...")
else:
    print("No results found.")
