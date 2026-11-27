# Specular Reflection Removal in Macro Ocular Photography

Corneal moisture and tear film produce intense specular light reflections under flash illumination:

1. **Failure Mode**: Specular glare produces saturated 255-luminance pixels that blind convolutional kernels from detecting underlying vascular erythema.
2. **Cross-Polarization Technique**: Aligning linear polarizing sheets perpendicularly on flash source and camera lens blocks direct glare while permitting deep backscattered mucosal light.
3. **Software Masking**: Preprocessing masks out regions with $V > 250$ in HSV space when computing regional Erythema Index ($EI$).
