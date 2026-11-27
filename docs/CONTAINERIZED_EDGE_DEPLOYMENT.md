# Containerized Edge Deployment with Podman & Docker

For hospital networks requiring air-gapped container runtimes:

```bash
# Build multi-stage container
podman build -t eyehealthai:latest .

# Run container binding to local clinical interface
podman run -d --name ocuscan-node \
  -p 127.0.0.1:8000:8000 \
  -e ENV=production \
  -v ./data:/app/data:Z \
  eyehealthai:latest
```

The container isolates filesystem permissions and runs as an unprivileged service user.
