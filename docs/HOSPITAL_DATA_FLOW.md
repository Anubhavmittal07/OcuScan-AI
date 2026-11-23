# End-to-End Hospital Data Flow & System Telemetry

```
[Patient Ingestion] -> [On-screen Informed Consent]
        │
        ▼
[Ocular Capture] -> [Laplacian Sharpness Check] -> [Macro Eye ROI Crop]
        │
        ▼
[Inference Engine] -> [Grad-CAM Attribution] -> [Demographic Stratification]
        │
        ▼
[Encrypted Session Store] -> [Two-Page PDF Generation] -> [Optional EHR Push]
```
