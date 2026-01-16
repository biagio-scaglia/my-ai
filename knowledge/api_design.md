# API Design Best Practices

## RESTful Principles

- **Risorse non Verbi**: Usa URL come `/users` (GET) per lista, non `/getUsers`.
- **Verbi HTTP corretti**:
  - `GET`: Leggere dati.
  - `POST`: Creare risorse.
  - `PUT/PATCH`: Aggiornare risorse.
  - `DELETE`: Cancellare risorse.
- **Codici di Stato**:
  - `200 OK`: Successo.
  - `201 Created`: Risorsa creata.
  - `400 Bad Request`: Errore client.
  - `401 Unauthorized`: Non loggato.
  - `403 Forbidden`: Vietato.
  - `404 Not Found`: Non trovato.
  - `500 Server Error`: Ops.

## Sicurezza

- Usa sempre **HTTPS**.
- Autenticazione via **Bearer Token** (JWT).
- Valida sempre l'input lato backend, mai fidarsi del client.

## Versione

- Includi la versione nell'URL: `/api/v1/users` per evitare breaking changes future.
