# Pre-Release Clinical Model Audit Checklist

Before tagging or deploying any updated checkpoint to production or clinical pilot sites:

- [ ] **Patient Leakage**: Verify zero subject-level overlap between train, validation, and test splits.
- [ ] **Shortcut Analysis**: Ensure model isn't using background skin color or image framing as a proxy.
- [ ] **Blur Sensitivity**: Test inputs with Laplacian variance below 100 to ensure proper rejection.
- [ ] **Age Calibration**: Verify demographic cutoff adaptations match WHO 2024 guidance.
- [ ] **Attribution Check**: Confirm Grad-CAM layer4 heatmaps center on palpebral mucosa rather than eyelashes.
