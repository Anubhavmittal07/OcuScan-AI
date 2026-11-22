# Image Artifact Rejection & Quality Gates

## Deterministic Quality Gates
Every ocular photograph ingested via camera or upload passes three automated validation checks:
1. **Motion Blur & Sharpness**: Laplacian variance must exceed 100.0. Blurry images are rejected prior to inference to prevent hallucinated vascular features.
2. **Exposure Boundaries**: Mean grayscale luminance must fall between 40 and 220 (out of 255). Severely underexposed or overexposed images are gated.
3. **Corneal Flash Glare**: Specular reflections occupying >15% of the visible iris or conjunctiva trigger a recommendation to adjust flash angle.
