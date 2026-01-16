# DevOps & CI/CD Essentials

## CI/CD Pipeline

- **Continuous Integration (CI)**: Test ed esecuzione automatica ad ogni commit.
- **Continuous Delivery (CD)**: Deploy automatico in staging (o produzione).

## Docker & Container

- **Dockerfile**: La ricetta dell'immagine.
  - Usa Multi-stage builds per immagini leggere.
  - Non eseguire come `root`.
- **Docker Compose**: Orchestrazione locale multi-container.

## Infrastructure as Code (IaC)

- **Terraform / OpenTofu**: Definisci l'infrastruttura (AWS, Azure) come codice dichiarativo.
- **Ansible**: Configurazione server e deploy.

## Monitoring

- **Logs**: Centralizza (ELK Stack, Loki).
- **Metriche**: Prometheus + Grafana per visualizzare carico CPU/RAM in tempo reale.
- **Tracing**: Jaeger/OpenTelemetry per seguire una richiesta tra microservizi.
