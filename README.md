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

## Local run (K3d)
k3d cluster create crud-ultra \
  -p "8081:80@loadbalancer" \
  -p "8443:443@loadbalancer" \
  --k3s-arg "--disable=traefik@server:0"

k3d image import crud-ultra:dev -c crud-ultra

kubectl apply -f k8s/

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml

kubectl apply -f k8s/ingress.yaml

### Проверка

curl -H "Host: crud-ultra.local" http://localhost:8081/health

