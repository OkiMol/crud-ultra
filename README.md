# CRUD Ultra (Python)

Цель проекта — демонстрационный стенд полного DevOps lifecycle для одного сервиса:
CI/CD → Docker → Kubernetes → Monitoring/Alerts → Rollback.

## Stack
- Python (FastAPI)
- Docker
- Kubernetes (k3s/minikube)
- GitHub Actions
- Prometheus + Grafana + Alertmanager
- Loki (опционально)

## Definition of Done
- FastAPI сервис с /health, /ready, /metrics
- Docker image build + push через GitHub Actions
- Kubernetes deployment + service + ingress
- readiness/liveness probes + resource limits
- Prometheus scraping + Grafana dashboard
- минимум 1 алерт, который реально срабатывает
- documented rollback scenario
- runbook в README

## Local run (Docker)

docker build -t crud-ultra:dev .
docker run --rm -p 8000:8000 crud-ultra:dev
