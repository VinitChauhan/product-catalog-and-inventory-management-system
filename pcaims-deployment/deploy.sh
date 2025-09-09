#!/bin/bash

# PCAIMS Deployment Script
# This script deploys the PCAIMS application using Helm

set -e

# Configuration
NAMESPACE=${NAMESPACE:-pcaims}
RELEASE_NAME=${RELEASE_NAME:-pcaims-app}
CHART_PATH="."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    log_error "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    log_error "helm is not installed or not in PATH"
    exit 1
fi

# Check for required GitHub credentials
if [[ -z "$GITHUB_USERNAME" || -z "$GITHUB_TOKEN" ]]; then
    log_warn "GitHub credentials not provided. Set GITHUB_USERNAME and GITHUB_TOKEN environment variables."
    log_warn "For public repositories, you can skip this by adding --set imagePullSecrets=null to the helm command"
fi

# Create namespace if it doesn't exist
log_info "Creating namespace '$NAMESPACE' if it doesn't exist..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Update image repositories in values.yaml based on your GitHub repository
log_info "Updating image repositories..."
GITHUB_REPO=${GITHUB_REPOSITORY:-"vinitchauhan/product-catalog-and-inventory-management-system"}

# Deploy using Helm
log_info "Deploying PCAIMS application..."
if [[ -n "$GITHUB_USERNAME" && -n "$GITHUB_TOKEN" ]]; then
    log_info "Using provided GitHub credentials for image pull secrets..."
    helm upgrade --install $RELEASE_NAME $CHART_PATH \
        --namespace $NAMESPACE \
        --set frontend.image.repository="ghcr.io/${GITHUB_REPO}-frontend" \
        --set backend.image.repository="ghcr.io/${GITHUB_REPO}-backend" \
        --set frontend.image.tag="${IMAGE_TAG:-latest}" \
        --set backend.image.tag="${IMAGE_TAG:-latest}" \
        --set ghcr.username="${GITHUB_USERNAME}" \
        --set ghcr.token="${GITHUB_TOKEN}" \
        --wait \
        --timeout=10m
else
    log_info "Deploying without image pull secrets (assuming public repositories)..."
    helm upgrade --install $RELEASE_NAME $CHART_PATH \
        --namespace $NAMESPACE \
        --set frontend.image.repository="ghcr.io/${GITHUB_REPO}-frontend" \
        --set backend.image.repository="ghcr.io/${GITHUB_REPO}-backend" \
        --set frontend.image.tag="${IMAGE_TAG:-latest}" \
        --set backend.image.tag="${IMAGE_TAG:-latest}" \
        --set imagePullSecrets=null \
        --wait \
        --timeout=10m
fi

# Check deployment status
log_info "Checking deployment status..."
kubectl get pods -n $NAMESPACE

# Get service information
log_info "Service information:"
kubectl get svc -n $NAMESPACE

# Get ingress information if enabled
if kubectl get ingress -n $NAMESPACE &> /dev/null; then
    log_info "Ingress information:"
    kubectl get ingress -n $NAMESPACE
fi

log_info "Deployment completed successfully!"
log_info "You can check the application status with: kubectl get all -n $NAMESPACE"