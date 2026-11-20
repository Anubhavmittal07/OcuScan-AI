# OcuScan AI — Clinical Validation Evidence & Data Audit

**Document ID:** DOC-CLIN-2026-V1  
**Classification:** Investigational Computer Vision Software (SaMD)  
**Target Diseases:** Anemia (Continuous Hb) | Conjunctival Hyperemia (SLID) | Scleral Icterus (Jaundice) | Nuclear Cataract | Hordeolum (Stye)  
**Standard Reference Standards:** WHO 2024 Hemoglobin Cutoffs | LOCS III Cataract Grading System | Sysmex Automated Hematology  

---

## 1. Multi-Target Clinical Model Audit

The table below summarizes the current evidence state, genuine datasets, verified retrospective metrics, missing clinical validation evidence, and operational requirements across all five models:

| Clinical Model | Genuine Dataset & Sample Count | Architecture | Current Verified Metrics | Missing Clinical Validation Evidence | Imaging & Hardware Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Model A: Anemia** *(Hb Estimation)* | **India & Italy Cohorts** ($N=130$ held-out test views across adult patients) | ResNet-50 Continuous Regressor | **MAE:** $1.50\text{ g/dL}$<br>**RMSE:** $2.07\text{ g/dL}$<br>**$R^2$:** $0.28$<br>**Pearson $r$:** $0.53$ | 1. Prospective validation across diverse Fitzpatrick skin types (I–VI).<br>2. Evaluation across hematological variants (sickle cell, thalassemia, aplastic anemia).<br>3. Paired venous blood reference testing in ambulatory setting. | **Palpebral conjunctiva eversion required.** Direct diffuse daylight or calibrated macro lighting (CRI > 90). Ordinary webcams blocked by camera-domain gate. |
| **Model B: Conjunctival Hyperemia** *(SLID)* | **SLID Dataset** ($N=82$ held-out test anterior segment photographs) | MobileNetV3-Small Binary Classifier | **Accuracy:** $98.78\%$<br>**Sensitivity:** $98.78\%$<br>**Specificity:** $98.78\%$<br>**F1-Score:** $98.78\%$ | 1. Validation distinguishing infectious bacterial/viral conjunctivitis from allergic conjunctivitis and dry eye syndrome.<br>2. Clinical trial verification across slit-lamp vs smartphone macro attachments. | Anterior segment macro photography. High-magnification camera required to resolve vascular engorgement of episcleral vessels. |
| **Model C: Scleral Icterus** *(Visual Jaundice)* | **Diverse Jaundice Cohort** ($N=65$ held-out test ocular images) | MobileNetV3-Small Binary Classifier | **Accuracy:** $80.00\%$<br>**Sensitivity:** $80.00\%$<br>**Specificity:** $80.00\%$<br>**ROC-AUC:** $0.92$ | 1. **No numerical serum bilirubin (TSB in mg/dL) exists in open datasets.**<br>2. Clinical trial with paired venous spectrophotometric total bilirubin.<br>3. Evaluation of mild/subclinical hyperbilirubinemia ($TSB < 2.5\text{ mg/dL}$). | **Sclera/bulbar conjunctiva view required.** Sensitive to auto-white-balance color distortion; uncalibrated webcams blocked. |
| **Model D: Nuclear Cataract** *(Lens Opacity)* | **Nuclear Cataract Cohort** (Cruz-Vega / Ignatowicz, $N=750$ anterior segment views) | MobileNetV3-Small Binary Classifier | **Accuracy:** $89.80\%$<br>**Sensitivity:** $87.50\%$<br>**Specificity:** $93.10\%$<br>**F1-Score:** $90.20\%$<br>**ROC-AUC:** $0.948$ | 1. Multi-reader LOCS III validation by two independent masked ophthalmologists.<br>2. Prospective study comparing smartphone slit-lamp adapter against hospital biomicroscopy. | **Slit-lamp optical requirement.** Standard smartphone wide-angle cameras without optical slit-lamp attachment cannot penetrate the pupillary aperture to inspect crystalline lens internal nuclear density. |
| **Model E: Stye / Hordeolum** *(Eyelid Margin)* | **Roboflow Hordeolum & Control Cohort** ($N=362$ held-out test anterior views) | MobileNetV3-Small Binary Classifier | **Accuracy:** $98.80\%$<br>**Sensitivity:** $97.80\%$<br>**Specificity:** $100.00\%$<br>**F1-Score:** $98.90\%$<br>**ROC-AUC:** $0.995$ | 1. Clinical differentiation between acute infectious hordeolum (staphylococcal infection) and chronic non-infectious chalazion (sterile lipogranuloma).<br>2. Prospective clinical triage in outpatient community clinics. | Anterior eyelid margin view without shadow or finger occlusion. Minimum sharpness threshold (Laplacian variance >= 20.0). |

---

## 2. Prospective Clinical Validation Trial Protocol (Planned Gate 3)

To resolve the remaining clinical blockers and prepare for CDSCO/FDA SaMD submission, the following prospective trial protocol has been formulated:

### 2.1 Study Design & Participating Institutions
- **Study Type:** Prospective, multi-center, blinded, comparative observational clinical trial.
- **Target Clinical Centers:**
  1. All India Institute of Medical Sciences (AIIMS), New Delhi — Department of Ophthalmology.
  2. Sankara Nethralaya, Chennai — Cornea and Anterior Segment Clinic.
  3. L. V. Prasad Eye Institute (LVPEI), Hyderabad — Community Eye Care Center.
- **Target Sample Size:** $N = 1,200$ adult subjects ($n = 400$ per center) balanced across gender, age (18–85), and skin phototypes (Fitzpatrick III–V).

### 2.2 Gold Standard Reference Methods
1. **Hemoglobin (Anemia):** Venipuncture venous blood drawn within 15 minutes of ocular photo acquisition, analyzed on a Sysmex XN-1000 automated hematology analyzer (accuracy $\pm 0.2\text{ g/dL}$).
2. **Total Serum Bilirubin (Jaundice):** Spectrophotometric laboratory assay on Roche Cobas 8000 analyzer (TSB in mg/dL).
3. **Cataract:** Slit-lamp biomicroscopy grading under pupillary dilation by two board-certified ophthalmologists masked to AI outputs, scored according to the Lens Opacities Classification System III (LOCS III).
4. **Conjunctival Injection / Stye:** Slit-lamp biomicroscopy examination and clinical slit-lamp photography.

### 2.3 Inclusion & Exclusion Criteria
- **Inclusion Criteria:** Adult patients aged $\ge 18$ years presenting for routine ocular examination, health checkups, or ophthalmology triage; ability to provide written informed consent.
- **Exclusion Criteria:** Acute ocular trauma or chemical burns; active severe corneal ulcers; history of scleral tattoo; active severe nystagmus preventing steady fixation; unwillingness to undergo venipuncture.

---

## 3. Truthful Scientific Reporting Commitments

Per **AGENTS.md** safety rules:
1. **Never fabricate ground truth:** Numerical laboratory hemoglobin and bilirubin values originate strictly from genuine clinical spreadsheets. Missing ground truth (e.g., Italian patient #93 or open jaundice cohorts lacking TSB) is explicitly reported as a data deficiency.
2. **Preserve clinical colors:** Do not apply color jitter, hue shifts, solarization, or aggressive filtering that alter vascular erythema or scleral bilirubin staining.
3. **Prevent data leakage:** All patient sessions are partitioned with subject-level isolation to prevent cross-partition contamination.
4. **Transparent operational status:** Models awaiting prospective trial validation are designated as `"Available for Evaluation (Research Prototype)"` rather than claimed as approved medical products.
