# REST API Specification & Data Transfer Models

## Core Endpoints

### 1. `GET /api/health`
Returns system operational health, GPU/CPU device status, and checkpoint availability.

### 2. `POST /api/quality-check`
Pre-screens ocular photographs for image quality prior to clinical inference:
- **Sharpness**: Laplacian variance threshold (>100.0).
- **Illumination**: Mean brightness within clinical bounds (40 - 220).
- **Aspect Ratio**: Standard ocular framing check.

### 3. `POST /api/analyze`
Unified multi-view screening endpoint accepting image file and participant profile parameters:
- `age`: Participant age in years (drives WHO severity cutoffs).
- `sex`: Participant sex (`male`, `female`).
- `notes`: Optional clinical observations.

### 4. `POST /api/export`
Generates a cryptographically hashed, standardized session audit report for electronic health records.
