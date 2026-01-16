# Web Frontend Mastery: JS, TS, Angular, Astro

## JavaScript (Modern ES6+)

- **Destructuring**: `const { name } = user;`
- **Spread Operator**: `const newArr = [...oldArr, 4, 5];`
- **Garantire Immutabilità**: Usa `const` e metodi che non mutano (es. `map`, `filter`, `reduce`) invece di `push/pop`.
- **Async/Await**: Molto più pulito delle Promise chain.
  ```javascript
  async function getData() {
    try {
      const res = await fetch("/api");
      const data = await res.json();
    } catch (e) {
      console.error(e);
    }
  }
  ```

## TypeScript

- **Non usare `any`**: Sconfigge lo scopo di TS. Usa `unknown` se proprio devi.
- **Interfaces vs Types**: Preferisci `interface` per oggetti estendibili, `type` per unioni o utility types.
- **Generics**: Potenti per componenti riutilizzabili.
  ```typescript
  function identity<T>(arg: T): T {
    return arg;
  }
  ```

## Angular

- **Componenti Standalone**: Il nuovo standard (v14+). Meno `NgModule`, più modularità.
- **Signals**: La nuova reattività fine-grained.
  ```typescript
  count = signal(0);
  double = computed(() => this.count() * 2);
  ```
- **RxJS**: Impara gli operatori base (`map`, `switchMap`, `tap`, `catchError`). Evita `subscribe` nei componenti (usa `AsyncPipe`).

## Astro

- **Islands Architecture**: Il JS viene caricato solo per i componenti interattivi (`client:load`, `client:visible`). Il resto è HTML statico (Zero JS).
- **Content Collections**: Il modo type-safe di gestire markdown/MDX.
  ```typescript
  // content/config.ts
  const blog = defineCollection({
    schema: z.object({ title: z.string(), date: z.date() }),
  });
  ```
