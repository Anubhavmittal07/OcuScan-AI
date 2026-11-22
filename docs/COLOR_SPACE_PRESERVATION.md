# CIE-L*a*b* Color Space Preservation

## Preprocessing Safety Rule
Standard computer vision pipelines frequently apply histogram equalization across all RGB channels, which distorts subtle erythema and icterus signals.
EyeHealthAI enforces:
1. RGB to CIE-LAB color space transformation.
2. Contrast-Limited Adaptive Histogram Equalization (CLAHE) applied **strictly to the Luminance (L) channel**.
3. Chromatic channels **a*** (green-red) and **b*** (blue-yellow) are left 100% unaltered.
4. LAB back-converted to RGB tensor for deep neural network input.
