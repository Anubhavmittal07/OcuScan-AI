# Clinical Dataset Provenance & Reference Standards

## 1. Anemia Optical Dataset
- **Sources**: Multicenter clinical datasets (`India.xlsx`, `Italy.xlsx`).
- **Target**: Venous blood laboratory reference hemoglobin ($Hb$ in g/dL).
- **Demographic Spread**: Pediatric (<12y), Adult Female, Adult Male, Geriatric (>65y).

## 2. Slit-Lamp Biomicroscopy (SLID)
- **Target**: Conjunctival injection / hyperemia grading.
- **Evaluation**: Zero subject leakage across training and held-out validation splits.

## 3. Diverse Jaundice Dataset
- **Target**: Categorical scleral icterus (Normal vs. Jaundiced).
- **Limitation**: Numerical serum bilirubin regression is strictly gated due to lack of paired laboratory ground truth.
