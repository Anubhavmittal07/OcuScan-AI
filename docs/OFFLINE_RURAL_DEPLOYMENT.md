# Offline Screening Deployment for Remote Health Centers

In rural camps where mobile internet and cellular data are unavailable:
1. **Local SQLite Persistence**: By default, OcuScan stores all screening sessions in local SQLite (`eyehealthai.db`).
2. **Local AI Guidance**: The deterministic fallback engine operates entirely offline without calling external APIs.
3. **Local PDF Printing**: Reports are generated using client-side ReportLab binaries and can be handed directly to patients.
