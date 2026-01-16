# Advanced Python Concepts

## Generator & Iterators

Usa `yield` per creare generatori che consumano memoria lazy.

```python
def my_gen():
    yield 1
    yield 2
```

## Decorators

Funzioni che modificano altre funzioni.

```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

## Context Managers

Usa `with` per gestire risorse (file, lock, connessioni).

```python
with open("file.txt") as f:
    content = f.read()
# File chiuso automaticamente
```

## Concurrency

- **Threading**: Per I/O bound tasks.
- **Multiprocessing**: Per CPU bound tasks (bypass GIL).
- **Asyncio**: Per concorrenza su singolo thread (network requests).

## Type Hinting

Usa `typing` per codice robusto.

```python
from typing import List, Optional

def process_items(items: List[str]) -> Optional[int]:
    return len(items) if items else None
```
