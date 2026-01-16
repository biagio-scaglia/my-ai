# React Design Patterns

## Component Patterns

- **Container/Presentational**: Separa la logica (Container) dalla UI (Presentational). Anche se con gli Hooks è meno usato, il principio di separazione vale.
- **Higher-Order Components (HOC)**: Funzioni che prendono un componente e ne ritornano uno arricchito.
- **Render Props**: Condividere codice tra componenti usando una prop il cui valore è una funzione.

## Hooks Pattern

Il moderno standard React.

- **Custom Hooks**: Estrai logica riutilizzabile in funzioni `useSomething`.
  ```javascript
  function useWindowSize() { ... }
  ```

## State Management

- **Local State**: `useState` per cose effimere.
- **Context API**: Per dati globali "lenti" (temi, auth).
- **Zustand / Redux**: Per stato globale complesso e aggiornamenti frequenti.

## Performance

- `useMemo`: Memorizza calcoli costosi.
- `useCallback`: Memorizza istanze di funzioni.
- `React.memo`: Previene re-render se le props non cambiano.
