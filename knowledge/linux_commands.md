# Linux & Terminal Commands

## File System

- `ls -la`: Lista tutti i file (inclusi nascosti) con dettagli.
- `cd <dir>`: Cambia directory.
- `pwd`: Stampa la directory corrente.
- `mkdir -p <path>`: Crea directory (e genitori se necessario).
- `rm -rf <path>`: Rimuove file/cartelle ricorsivamente (PERICOLOSO!).
- `cp -r <src> <dest>`: Copia ricorsivamente.

## Permessi

- `chmod +x <file>`: Rende eseguibile.
- `chown user:group <file>`: Cambia proprietario.

## Processi

- `ps aux`: Mostra tutti i processi attivi.
- `top` / `htop`: Monitoraggio risorse in tempo reale.
- `kill <pid>`: Termina un processo.
- `killall <name>`: Termina processi per nome.

## Networking

- `curl <url>`: Scarica o fa richieste HTTP.
- `ping <host>`: Verifica connessione.
- `netstat -tuln`: Mostra porte in ascolto.
- `ssh user@host`: Connessione remota sicura.

## Ricerca

- `grep "text" <file>`: Cerca testo in un file.
- `find . -name "*.py"`: Trova file per nome.
