# Git Cheat Sheet & Workflow

## Comandi Base

- `git init`: Inizia un nuovo repository.
- `git clone <url>`: Clona un repository esistente.
- `git status`: Vedi lo stato dei file.
- `git add .`: Aggiungi tutti i file allo stage.
- `git commit -m "messaggio"`: Registra le modifiche.

## Branching

- `git branch`: Lista i branch.
- `git checkout -b <nome>`: Crea e sposta su un nuovo branch.
- `git checkout <nome>`: Sposta su un branch esistente.
- `git merge <nome>`: Unisci il branch specificato in quello corrente.

## Workflow Moderno (Feature Branch)

1.  Tira sempre il `main` aggiornato (`git pull origin main`).
2.  Crea un branch per la tua feature (`git checkout -b feature/nuova-login`).
3.  Lavora e committa spesso.
4.  Pusha il branch (`git push origin feature/nuova-login`).
5.  Apri una Pull Request (PR) per la code review.
