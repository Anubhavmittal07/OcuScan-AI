# Grad-CAM Attribution Layer Tradeoffs

In ResNet-50, convolutional activations provide different spatial granularities:
- `layer3`: Captures broader anatomical context (eyelid boundaries, orbital symmetry) with higher spatial resolution (14×14).
- `layer4`: Captures rich semantic representations (microvascular beds, conjunctival pallor) at 7×7 resolution.

EyeHealthAI extracts attribution from the final convolutional stage of `layer4` and upsamples via bicubic interpolation with Gaussian smoothing for optimal anatomical alignment.
