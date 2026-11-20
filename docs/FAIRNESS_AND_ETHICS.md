# Algorithmic Fairness & Demographic Calibration

## Fitzpatrick Skin Type Parity
Ocular biomarkers (conjunctival erythema, scleral reflectance) can be influenced by periocular skin pigmentation. EyeHealthAI ensures:
- **Adaptive Region-of-Interest Extraction**: Scleral and conjunctival masks exclude external melanin-rich skin surfaces.
- **Stratified Accuracy Auditing**: Performance metrics are evaluated across Fitzpatrick skin scales I through VI to prevent disparate false-positive rates.
- **WHO Guidelines Alignment**: Cutoffs for anemia risk staging strictly follow World Health Organization age-stratified thresholds.
