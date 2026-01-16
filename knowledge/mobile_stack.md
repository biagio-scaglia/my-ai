# Mobile Development: Flutter, Dart, Kotlin

## Flutter & Dart

- **Immutabilità**: Estendi `StatelessWidget` quando possibile. Usa `final` per i campi.
- **State Management**:
  - **Bloc/Cubit**: Per logica di business complessa e separazione netta.
  - **Riverpod**: Una versione moderna e sicura di Provider (compile-time safety).
- **Widget Lifecycle**:
  - Usa `const` costruttori per dire a Flutter di non ricostruire widget statici.
- **Dart Features**:
  - **Null Safety**: È attiva di default. Gestisci i null (`?`) esplicitamente.
  - **Extensions**: Aggiungi metodi a classi esistenti senza ereditare.
    ```dart
    extension StringExt on String {
      bool get isEmail => contains('@');
    }
    ```

## Kotlin (Android & Multiplatform)

- **Data Classes**: Per contenitori di dati (generano `toString`, `equals`, `copy` gratis).
  ```kotlin
  data class User(val name: String, val age: Int)
  ```
- **Coroutines**: Gestione asincrona leggera. Usa `suspend` functions e `viewModelScope`.
  ```kotlin
  viewModelScope.launch {
      val data = repository.fetchData()
  }
  ```
- **Extension Functions**: Come in Dart, rendono il codice leggibile.
- **Jetpack Compose**: UI dichiarativa (simile a Flutter/React). Abbandona l'XML per le nuove view.
