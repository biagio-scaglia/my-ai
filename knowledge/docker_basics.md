# Docker Basics

## Concetti Chiave

- **Image**: Il progetto compilato e pronto (come un CD di installazione). È immutabile.
- **Container**: L'istanza in esecuzione di un'immagine (come il computer acceso).
- **Dockerfile**: Le istruzioni per costruire l'immagine.
- **Docker Compose**: Strumento per gestire multi-container (es. App + Database).

## Comandi Utili

- `docker build -t mia-app .`: Costruisce l'immagine.
- `docker run -p 3000:3000 mia-app`: Lancia l'app mappando la porta 3000.
- `docker ps`: Lista container attivi.
- `docker stop <id>`: Ferma un container.

## Esempio Dockerfile (Node.js)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```
