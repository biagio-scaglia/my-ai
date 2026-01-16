# Clean Code Principles

## Naming Conventions

- **Sii descrittivo**: `getUserByName` è meglio di `func1`.
- **Usa verbi per le funzioni**: `calculateTotal()`, `isValid()`.
- **Usa sostantivi per le classi**: `User`, `AccountManager`.

## Funzioni

- **Una sola responsabilità**: Una funzione deve fare una cosa sola e farla bene (SRP).
- **Keep it small**: Le funzioni dovrebbero essere brevi.
- **Evita effetti collaterali**: Non modificare variabili globali inaspettatamente.

## Commenti

- **Non commentare il "cosa" ma il "perché"**: Il codice dovrebbe spiegarsi da solo. Usa i commenti per spiegare decisioni complesse o workaround.
- **Evita codice commentato**: Usa Git per la storia, cancella il codice morto.

## DRY (Don't Repeat Yourself)

- Evita la duplicazione. Se copi e incolli codice, probabilmente dovresti estrarlo in una funzione.
