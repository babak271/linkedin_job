# FastAPI on k3s with Helm & GitHub Actions

This repository contains a minimal FastAPI service, a production-ready container image, a Helm chart for k3s (Traefik) clusters, and a CI/CD workflow that builds the container and deploys it through Helm.

## 1. FastAPI application

The app lives in `src/linked_job/app.py` and exposes:

- `GET /` – welcome payload.
- `GET /health` – probe endpoint wired into the Kubernetes liveness/readiness checks.

Run it locally with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
FASTAPI_RELOAD=1 FASTAPI_PORT=8080 uv run linkedin_job
```

Visit http://127.0.0.1:8080/health to verify responses.

## 2. Dockerization

The project ships with a slim Python 3.12 Dockerfile that installs the package and starts Uvicorn on port 8080.

```bash
docker build -t ghcr.io/<org>/linkedin_job:dev .
docker run --rm -p 8080:8080 ghcr.io/<org>/linkedin_job:dev
```

Adjust `<org>` to match the GitHub organization/user that owns the repository. The `.dockerignore` keeps virtualenvs, git metadata, and build artifacts out of the image.

## 3. Helm chart for k3s

`charts/fastapi` describes the deployment. Key values (see `values.yaml`):

- `image.repository` / `image.tag` – GHCR image to deploy.
- `imagePullSecrets` – list of registry secrets. For GHCR create one in the `fastapi` namespace:

  ```bash
  kubectl create namespace fastapi
  kubectl -n fastapi create secret docker-registry ghcr-creds \
    --docker-server=ghcr.io \
    --docker-username=<github-username> \
    --docker-password=<classic-or-fine-grained-token-with-read:packages>
  ```

  Then set `imagePullSecrets[0].name: ghcr-creds` in `values.yaml`.

- `service.*` – exposes the container on port 80 inside the cluster (maps to container port 8080).
- `ingress.*` – enabled by default and targets Traefik, the k3s default. Update `example.com` to your domain and optionally configure TLS.

Install/upgrade manually:

```bash
helm upgrade --install fastapi charts/fastapi \
  --namespace fastapi \
  --create-namespace \
  --set image.repository=ghcr.io/<org>/linkedin_job \
  --set image.tag=$(git rev-parse HEAD)
```

Traefik will route traffic for `example.com` (or whatever host you set) to the service once the record points to the k3s node(s).

## 4. GitHub Actions pipeline

`.github/workflows/deploy.yaml` automates everything on pushes to `main`:

1. Builds the Docker image, tags it with the commit SHA and `latest`, and pushes both to GHCR.
2. Installs Helm, decodes the kubeconfig secret, and performs `helm upgrade --install` using the chart described above.

### Required repository secrets

| Secret | Description |
| ------ | ----------- |
| `K3S_KUBECONFIG_B64` | Base64-encoded kubeconfig with access to the k3s cluster. Run `base64 -w0 ~/.kube/config` (Linux) or `base64 ~/.kube/config | tr -d '\n'` (macOS) and paste the output into the secret. |

The GITHUB_TOKEN provided to the workflow already has permission to push packages. For private clusters pulling from GHCR you must still provision the `ghcr-creds` secret inside Kubernetes (see Helm section).

## Putting it all together

1. Commit any edits to `charts/fastapi/values.yaml` (ingress host, imagePullSecrets, resources, etc.).
2. Create the `fastapi` namespace and GHCR imagePullSecret in the cluster.
3. Add the `K3S_KUBECONFIG_B64` secret to the GitHub repository.
4. Push to `main`. GitHub Actions will build the Docker image, push to GHCR, and roll the Helm release on your k3s server at `example.com`.

You can track deployment status with:

```bash
kubectl get pods -n fastapi
kubectl get ingress -n fastapi
```
