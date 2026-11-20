# OcuScan AI — Commercial Deployment & Operational Guide
**Architecture:** FastAPI + PyTorch + OpenCV + SQLite/PostgreSQL  
**Version:** 2.0.0 Production Release

---

## 1. System Requirements & Hardware Specifications

| Component | Minimum Specification (CPU Inference) | Recommended Production Specification |
| :--- | :--- | :--- |
| **Processor** | 4-Core x86_64 CPU (Intel i5/Xeon or AMD Ryzen 5) | 8-Core Intel Xeon / AMD EPYC |
| **RAM** | 8 GB DDR4 | 16 GB - 32 GB DDR4/DDR5 |
| **GPU Acceleration** | Optional (Runs efficiently on CPU) | NVIDIA T4 / A10G / RTX 4000 (16GB VRAM) for batch inference |
| **Storage** | 10 GB free SSD storage | 50 GB NVMe SSD (for session logs & reports) |
| **Operating System** | Ubuntu 22.04 LTS / Debian 12 / Windows Server 2022 | Ubuntu 22.04 LTS (Containerized via Docker) |
| **Python Version** | Python 3.10 or 3.11 | Python 3.11.9 |

---

## 2. Environment Configuration (`.env`)

Create a `.env` file in the repository root directory with the following configuration:

```ini
# Environment Mode
ENV=production
DEBUG=false

# Server Binding
HOST=0.0.0.0
PORT=8000

# Security & CORS (Comma-separated allowed origins)
ALLOWED_ORIGINS=https://screening.yourclinic.com,https://app.ocuscan.ai

# Upload Security Constraints
MAX_UPLOAD_SIZE_MB=15

# Inference Hardware
DEVICE=cpu  # Set to "cuda" if NVIDIA GPU and CUDA 11.8+ installed

# Model Checkpoints (Defaults to local saved_models directory)
ANEMIA_CHECKPOINT_PATH=saved_models/anemia/best_model.pth
CONJUNCTIVITIS_CHECKPOINT_PATH=saved_models/conjunctivitis/best_model_v2_clean.pth
SLID_CHECKPOINT_PATH=saved_models/slid/best_model.pth
JAUNDICE_CHECKPOINT_PATH=saved_models/jaundice/best_model.pth
JAUNDICE_CONFIG_PATH=saved_models/jaundice/jaundice_config.json
CATARACT_CHECKPOINT_PATH=saved_models/cataract/best_model.pth
STYE_CHECKPOINT_PATH=saved_models/stye/best_model.pth

# External AI Personalization (Optional, HIPAA/DPDP Compliant Zero-PII)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
```

---

## 3. Installation & Setup

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/your-org/ocuscan-ai.git
cd ocuscan-ai

python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Verify Checkpoint Integrity & Operational Health
```bash
python -c "
from src.inference.unified_service import get_inference_service
s = get_inference_service()
print('All 5 models loaded successfully:', [
    s._get_anemia_model() is not None,
    s._get_slid_model() is not None,
    s._get_jaundice_model() is not None,
    s._get_cataract_model() is not None,
    s._get_stye_model() is not None
])
"
```

---

## 4. Launching the Production Server

### Direct Uvicorn Launch (Single Worker or Development)
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production Multi-Worker Process (Gunicorn with Uvicorn Workers)
```bash
gunicorn app:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log
```

---

## 5. Health Check & Monitoring Endpoints

| Endpoint | HTTP Method | Description |
| :--- | :--- | :--- |
| `/api/health` | `GET` | System operational health, device status, and model checkpoint availability. |
| `/api/reliability-metrics` | `GET` | Genuine evaluation metrics, confusion matrices, and lifecycle governance statuses. |
| `/api/export` | `GET` | Audit trail export of all recorded screening sessions. |
| `/api/sessions/{session_id}` | `DELETE` | Right to Erasure / GDPR privacy deletion endpoint. |

### Verification Command
```bash
curl -X GET http://127.0.0.1:8000/api/health
```

Expected Response:
```json
{
  "status": "healthy",
  "service": "OcuScan AI Clinical Research & Screening Service",
  "version": "2.0.0",
  "environment": "production",
  "device": "cpu",
  "modules": {
    "anemia": { "checkpoint_present": true, "status": "Available for Evaluation" },
    "conjunctivitis": { "checkpoint_present": true, "status": "Available for Evaluation" },
    "jaundice": { "checkpoint_present": true, "status": "Available for Evaluation" },
    "cataract": { "checkpoint_present": true, "status": "Available for Evaluation" },
    "stye": { "checkpoint_present": true, "status": "Available for Evaluation" }
  }
}
```

---

## 6. Nginx Reverse Proxy Configuration (with SSL/TLS 1.3)

```nginx
server {
    listen 80;
    server_name screening.yourclinic.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name screening.yourclinic.com;

    ssl_certificate /etc/letsencrypt/live/screening.yourclinic.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/screening.yourclinic.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Maximum file upload size (matching MAX_UPLOAD_SIZE_MB)
    client_max_body_size 15M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```
