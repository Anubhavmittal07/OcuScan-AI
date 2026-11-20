# Troubleshooting & Hospital Deployment FAQ

### 1. Server Fails to Start (Address already in use)
- **Cause**: Another process is occupying port 8000.
- **Remedy**: Change `PORT=8001` in `.env` or terminate the conflicting process.

### 2. Checkpoint Not Found Warnings
- **Cause**: Pretrained weights are being downloaded or staged in `saved_models/`.
- **Behavior**: The framework gracefully continues in fallback mode and reports `missing_checkpoint` on `/api/health`.

### 3. Camera Access Denied in Browser
- **Cause**: Browser permissions or non-secure origin.
- **Remedy**: Ensure accessing via `http://localhost:8000` or `https://` for external IPs. Modern browsers block WebRTC on unencrypted remote IP addresses.
