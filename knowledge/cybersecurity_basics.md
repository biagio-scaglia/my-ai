# Cybersecurity & Secure Coding

## OWASP Top 10 (Difesa)

1.  **Injection (SQLi)**: Usa SEMPRE Prepared Statements o ORM. Mai concatenare stringhe in query.
2.  **Broken Auth**: Usa MFA, password hashing forti (Argon2, bcrypt), gestione sessioni sicura (HttpOnly Cookies).
3.  **Sensitive Data Exposure**: Crittografa dati a riposo (AES-256) e in transito (TLS 1.3).
4.  **XSS (Cross Site Scripting)**: Sanitizza l'input utente, usa Content Security Policy (CSP).

## Principi Generali

- **Least Privilege**: Dai ai processi solo i permessi strettamente necessari.
- **Defense in Depth**: Muri multipli (Firewall -> WAF -> App Auth -> DB Enc).
- **Zero Trust**: Non fidarti mai della rete interna.
- **Input Validation**: Valida tutto (lunghezza, tipo, formato) lato server.

## Tooling

- **SAST**: SonarQube (analisi statica codice).
- **Dependency Check**: `npm audit`, `pip-audit` (vulnerabilità librerie).
