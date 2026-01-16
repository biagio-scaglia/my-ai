# Backend Languages: C#, PHP, Ruby

## C# (.NET)

- **LINQ**: La feature più potente di C# per manipolare collezioni.
  ```csharp
  var adults = users.Where(u => u.Age >= 18).Select(u => u.Name).ToList();
  ```
- **Async/Await**: Standard per I/O. Non bloccare mai il thread principale.
- **Dependency Injection**: Integrata in .NET Core. Registra i servizi in `Program.cs`.
- **Records**: Tipi di riferimento immutabili (ottimi per DTO).
  ```csharp
  public record Person(string FirstName, string LastName);
  ```

## PHP (Moderno 8.x+)

- **Dimentica il vecchio PHP**: Usa tipi, classi e strict mode (`declare(strict_types=1);`).
- **Constructor Property Promotion**: Meno boilerplate.
  ```php
  class Point {
      public function __construct(public float $x, public float $y) {}
  }
  ```
- **Composer**: Gestore di pacchetti essenziale. Usa PSR-4 per l'autoloading.
- **Laravel**: Il framework standard de facto. Usa Eloquent per i DB e Artisan per la CLI.

## Ruby

- **Sintassi Espressiva**: "Programmer happiness". Le parentesi sono spesso opzionali.
- **Blocks & Procs**: Potenti per iterazioni e callback.
  ```ruby
  users.each { |u| puts u.name }
  ```
- **Rails (Ruby on Rails)**: Convention over Configuration.
  - **ActiveRecord**: L'ORM che ha ispirato tutti gli altri.
  - Usa le migrazioni per il DB.
  - Mantieni i controller snelli ("Skinny Controller, Fat Model").
