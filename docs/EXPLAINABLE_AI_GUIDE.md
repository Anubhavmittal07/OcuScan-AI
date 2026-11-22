# Explainable AI & Grad-CAM Layer Attribution Guide

## Attribution Methodology
To avoid black-box decision making in clinical screening, EyeHealthAI implements Gradient-weighted Class Activation Mapping (Grad-CAM):
- **ResNet-50 (Anemia)**: Targets `model.layer4[2].conv3` feature activations.
- **MobileNetV3 (SLID / Jaundice)**: Targets the final convolutional layer of `model.features`.

## Clinical Interpretation
- **Red/Yellow Regions**: High positive feature attribution driving the diagnostic classification or regression value.
- **Blue Regions**: Neutral or low attribution background regions.
- **Validation Rule**: Heatmaps must concentrate anatomically on the palpebral conjunctiva or sclera. If attention shifts to eyelashes or background skin, results are flagged with low confidence.
