# Software Design Patterns

## Creazionali (Creazione Oggetti)

- **Singleton**: Una sola istanza di una classe (es. connessione Database). _Attenzione: difficile da testare._
- **Factory**: Interfaccia per creare oggetti, lasciando alle sottoclassi la decisione di quale classe istanziare.
- **Builder**: Costruisce oggetti complessi passo dopo passo.

## Strutturali (Composizione Classi)

- **Adapter**: Fa collaborare interfacce incompatibili (es. vecchio sistema pagamento -> nuovo sistema).
- **Facade**: Fornisce un'interfaccia semplificata a un sistema complesso.

## Comportamentali (Interazione)

- **Observer**: Un oggetto notifica altri oggetti dei cambiamenti di stato (es. Event Listeners).
- **Strategy**: Definisce una famiglia di algoritmi interscambiabili (es. strategie di ordinamento diverse).

## Quando usarli?

Non forzarli! Usa i pattern per risolvere problemi comuni che emergono, non per anticiparli inutilmente (YAGNI).
