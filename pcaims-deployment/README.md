# PCAIMS Helm Chart

This Helm chart deploys the Product Catalog and Inventory Management System (PCAIMS) with separate pods for frontend, backend, and MySQL database.

## Architecture

The deployment consists of three main components:

1. **Frontend Pod**: Flask-based web interface
2. **Backend Pod**: FastAPI-based REST API
3. **MySQL Pod**: Database with persistent storage

## Prerequisites

- Kubernetes cluster (kind, minikube, or cloud provider)
- Helm 3.x installed
- kubectl configured to access your cluster
- Docker images built and pushed to ghcr.io

## Quick Start

### 1. Build and Push Images

First, ensure your images are built and pushed to GitHub Container Registry:

```bash
# Build and push frontend
docker build -t ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-frontend:latest ./src/frontend
docker push ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-frontend:latest

# Build and push backend
docker build -t ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-backend:latest ./src/backend
docker push ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-backend:latest
```

### 2. Deploy with Helm

```bash
# Using the deployment script
./deploy.sh

# Or manually with Helm
helm install pcaims-app . --namespace pcaims --create-namespace
```

### 3. Access the Application

```bash
# Port forward to access locally
kubectl port-forward -n pcaims svc/pcaims-app-frontend 5000:5000
kubectl port-forward -n pcaims svc/pcaims-app-backend 8000:8000

# Access frontend at http://localhost:5000
# Access backend API at http://localhost:8000
```

## Configuration

### Image Configuration

Update the image repositories in `values.yaml`:

```yaml
frontend:
  image:
    repository: ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-frontend
    tag: "latest"

backend:
  image:
    repository: ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-backend
    tag: "latest"
```

### Database Configuration

The MySQL database includes:
- Persistent storage (configurable size)
- Automatic initialization with schema and sample data
- Health checks and probes

```yaml
mysql:
  persistence:
    enabled: true
    size: 10Gi
    storageClass: ""  # Use default storage class
```

### Resource Limits

Configure resource limits for each component:

```yaml
frontend:
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
```

## Ingress Configuration

Enable ingress to expose the application:

```yaml
ingress:
  enabled: true
  hosts:
    - host: pcaims.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: backend
```

Add to your `/etc/hosts` file:
```
127.0.0.1 pcaims.local
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n pcaims
kubectl describe pod <pod-name> -n pcaims
```

### Check Logs
```bash
kubectl logs -f deployment/pcaims-app-frontend -n pcaims
kubectl logs -f deployment/pcaims-app-backend -n pcaims
kubectl logs -f deployment/pcaims-app-mysql -n pcaims
```

### Database Connection Issues

If the backend can't connect to MySQL:

1. Check if MySQL pod is running and ready
2. Verify the service name resolution
3. Check environment variables in backend pod

```bash
kubectl exec -it deployment/pcaims-app-backend -n pcaims -- env | grep DB_
```

### Init SQL Not Loading

The init.sql is embedded in a ConfigMap and mounted to the MySQL container. Check:

```bash
kubectl get configmap pcaims-app-mysql-init -n pcaims -o yaml
kubectl exec -it deployment/pcaims-app-mysql -n pcaims -- ls -la /docker-entrypoint-initdb.d/
```

## Scaling

Scale individual components:

```bash
# Scale frontend
kubectl scale deployment pcaims-app-frontend --replicas=3 -n pcaims

# Scale backend
kubectl scale deployment pcaims-app-backend --replicas=2 -n pcaims
```

## Cleanup

```bash
helm uninstall pcaims-app -n pcaims
kubectl delete namespace pcaims
```

## Values Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.enabled` | Enable frontend deployment | `true` |
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `backend.enabled` | Enable backend deployment | `true` |
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.image.repository` | Backend image repository | `ghcr.io/vinitchauhan/product-catalog-and-inventory-management-system-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `mysql.enabled` | Enable MySQL deployment | `true` |
| `mysql.persistence.enabled` | Enable persistent storage | `true` |
| `mysql.persistence.size` | Storage size | `10Gi` |
| `ingress.enabled` | Enable ingress | `true` |