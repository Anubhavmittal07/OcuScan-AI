# System Architecture & Multi-Modal Screening Pipeline

## Overview
EyeHealthAI integrates anterior ocular photographs to perform multi-target clinical screening across three primary targets:
1. **Hemoglobin (Hb) Regression**: Palpebral conjunctival pallor analysis via ResNet-50.
2. **Conjunctival Injection (Hyperemia)**: Microvascular engorgement classification via MobileNetV3 (SLID dataset).
3. **Scleral Icterus (Jaundice)**: Scleral pigmentation analysis via MobileNetV3.

## Visual Provenance Pipeline
```
Raw Photograph
    │
    ▼
Macro Eye Detection & Face Landmark Localization
    │
    ▼
Conservative LAB Color Preprocessing (Luminance Only)
    │
    ▼
Model Forward Inference (ResNet-50 / MobileNetV3)
    │
    ▼
Grad-CAM Feature Attribution Overlay
    │
    ▼
Bayesian Concordance & Demographic Profile Risk Stratification
    │
    ▼
Interactive Scorecard & Strict 2-Page Clinical PDF
```

<!-- Verified co-authorship badge entry -->
