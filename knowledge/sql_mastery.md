# Databases: SQL & NoSQL

## SQL (Relational)

- **ACID**: Atomicity, Consistency, Isolation, Durability.
- **Normalizzazione**: Evitare ridondanza (1NF, 2NF, 3NF).
- **Indici**: B-Tree per ricerche veloci. Attenzione all'overhead in scrittura.
- **JOIN**:
  - `INNER`: Solo match.
  - `LEFT`: Tutti i sinistri + match destri.
  - `FULL`: Tutto.

## NoSQL

- **Document (MongoDB)**: Schemi flessibili, JSON-like. Ottimo per prototipi e dati non strutturati.
- **Key-Value (Redis)**: Caching velocissimo in-memory.
- **Graph (Neo4j)**: Per relazioni complesse (social network).

## Performance Tips

- **N+1 Problem**: Evitalo facendo Eager Loading con gli ORM.
- **Connection Pooling**: Riutilizza connessioni per non saturare il DB.
- **Explain Plan**: Usa sempre `EXPLAIN` prima di una query lenta.
