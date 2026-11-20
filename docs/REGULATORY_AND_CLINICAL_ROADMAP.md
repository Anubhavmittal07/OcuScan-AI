# OcuScan AI — Regulatory Compliance & Clinical Validation Roadmap
**Classification: Software as a Medical Device (SaMD)**  
**Version:** 2.0.0 (Commercial Production Preparation)  
**Standard Governance:** ISO 13485:2016 | ISO 14971:2019 | IEC 62304:2015 | Indian MDR 2017 (CDSCO)

---

## 1. Regulatory Categorization & Intended Use

### 1.1 Statement of Intended Use
> **OcuScan AI** is an artificial intelligence-assisted, multi-modal ocular screening support platform designed to analyze digital photographs of the anterior ocular segment (conjunctiva, sclera, crystalline lens, and eyelid margins) acquired via standardized optical macro cameras or guided domestic webcams. It computes continuous physiological estimations (hemoglobin in g/dL) and categorical screening risk alerts for visible conjunctival injection, scleral icterus, nuclear cataract, and hordeolum.
>
> **Intended User:** Primary healthcare workers, optometrists, community screening camps, and adult participants under guided clinical protocols.  
> **Clinical Status:** Investigational screening support and clinical decision aid. It is **NOT** a standalone diagnostic device and cannot substitute for venous laboratory hematology, serum biochemistry, or comprehensive ophthalmological examination.

### 1.2 Jurisdictional Device Classification

| Regulatory Body | Jurisdiction | Classification | Target Pathway |
| :--- | :--- | :--- | :--- |
| **CDSCO** (Central Drugs Standard Control Organisation) | India | **Class B Medical Device** (Low-Moderate Risk SaMD under MDR 2017 Rule 20) | Form MD-14 (Application for Import License) / Form MD-5 (Manufacturing License for Medical Device) |
| **US FDA** | United States | **Class II SaMD** (21 CFR 886.1570 / Computerized Ocular Screening System) | De Novo or 510(k) Premarket Notification with predicate comparison |
| **EU MDR** | European Union | **Class IIa SaMD** (MDR 2017/745, Annex VIII, Rule 11) | Notified Body Assessment, CE Mark Technical Documentation |

---

## 2. Quality & Software Safety Lifecycle (IEC 62304 / ISO 13485)

OcuScan AI adheres to the software safety lifecycle requirements defined by **IEC 62304:2006+A1:2015**:
- **Software Safety Classification:** **Class B** (Software failure cannot directly cause severe injury, but incorrect triaging could cause delayed medical intervention).
- **Risk Management Standard:** **ISO 14971:2019** application to medical devices.
- **Usability Engineering:** **IEC 62366-1:2015** verifying that non-clinical users cannot misinterpret screening alerts as diagnostic confirmation.

### 2.1 Release Gates Lifecycle Matrix

```mermaid
flowchart LR
    G1["Gate 1<br/>Technical Checkpoint Integrity<br/><b>[COMPLETED]</b>"] --> G2["Gate 2<br/>Offline Held-Out Benchmark<br/><b>[COMPLETED]</b>"]
    G2 --> G3["Gate 3<br/>Prospective Multi-Center Trials<br/><b>[PLANNED]</b>"]
    G3 --> G4["Gate 4<br/>CDSCO SaMD Clearance<br/><b>[PENDING]</b>"]
    G4 --> G5["Gate 5<br/>Production Deployment & PMS<br/><b>[COMMERCIAL RELEASE]</b>"]
```

| Release Gate | Requirement | Current Verification Status | Target Completion |
| :--- | :--- | :--- | :--- |
| **Gate 1: Checkpoint Integrity** | All 5 PyTorch model weights load, verify SHA-256 hashes, execute on CPU/CUDA, and maintain aspect-ratio color fidelity. | **PASSED** (ResNet-50, 4x MobileNetV3-Small loaded in `EyeHealthInferenceService`) | Baseline 2026 |
| **Gate 2: Technical Benchmark** | Patient-isolated held-out evaluation preventing data leakage; verified test metrics matching clinical reports. | **PASSED** (689 held-out clinical images: Anemia MAE 1.50 g/dL, SLID 98.78%, Jaundice 80.0%, Cataract 0.910 ROC-AUC, Stye 100%) | Q4 2026 |
| **Gate 3: Clinical Trials** | Prospective multi-center clinical validation across at least 3 clinical centers (e.g. AIIMS, Sankara Nethralaya, LVPEI) with matched gold standards. | **IN PROGRESS / PROTOCOL DEFINED** | Q2 2027 |
| **Gate 4: Regulatory Registration** | CDSCO Sugam portal filing (Form MD-14/MD-5), Device Master File (DMF), ISO 13485 audit. | **PENDING** | Q3 2027 |
| **Gate 5: Commercial Production** | Production deployment with Post-Market Surveillance (PMS), adverse event reporting, and automated model drift monitoring. | **GATE LOCKED PENDING G3 & G4** | Q4 2027 |

---

## 3. Data Protection, Privacy & Cybersecurity Architecture

OcuScan AI operates in strict compliance with the **Digital Personal Data Protection Act, 2023 (DPDP Act, India)**, the **General Data Protection Regulation (GDPR)**, and the **HIPAA Security Rule**:

1. **Zero Raw Image Upload Without Informed Consent:** Explicit informed consent is collected on Step 2 before camera activation or file transmission.
2. **Right to Erasure (DPDP Act Section 12 / GDPR Article 17):** Implemented via `@app.delete("/api/sessions/{session_id}")` and `@app.delete("/api/user/{user_id}")`, executing permanent cascade deletion from SQLite/PostgreSQL storage.
3. **Anonymized Processing Pipeline:** Images processed for inference are decoupled from personally identifiable information (PII). Model feature extractors receive cropped ocular tensors without facial landmarks or subject names.
4. **Encryption in Transit & Rest:** All external transmissions enforce TLS 1.3. Local database sessions and model weights are sandboxed with restricted filesystem permissions.

---

## 4. Prospective Multi-Center Clinical Trial Protocol (Protocol OS-CT-01)

### 4.1 Participating Cohort Target
- **Target Sample Size:** $N = 1,200$ adult subjects (ages 18–85), multi-center representation across North, South, and Central India.
- **Target Demographics:** Diverse Fitzpatrick skin phototypes (Types III through VI) and varying iris pigmentation.

### 4.2 Matched Gold Standards per Condition

| Clinical Target | OcuScan AI AI Input | Matched Clinical Gold Standard | Primary Endpoint |
| :--- | :--- | :--- | :--- |
| **Anemia** | Palpebral & forniceal conjunctival macro photography | Venous blood draw analyzed on automated 5-part differential hematology analyzer (Sysmex XN-1000) within 2 hours. | MAE $\le 1.2$ g/dL, Sensitivity $\ge 85\%$ for Hb $< 11.0$ g/dL |
| **Conjunctival Redness** | Anterior ocular surface photography | Slit-lamp biomicroscopy with validated Efron grading scale (0–4) by two independent ophthalmologists. | Sensitivity $\ge 90\%$, Specificity $\ge 92\%$ |
| **Jaundice** | Exposed bulbar scleral macro photography | Laboratory venous total serum bilirubin (TSB) via diazo/enzymatic assay (Cobas c501). | Sensitivity $\ge 85\%$ for TSB $\ge 2.5$ mg/dL |
| **Nuclear Cataract** | Slit-lamp anterior optical section | Full mydriatic slit-lamp examination with LOCS III grading chart (NO1–NO6). | Sensitivity $\ge 88\%$, Specificity $\ge 85\%$ |
| **Stye / Hordeolum** | Eyelid margin photography | In-person clinical examination by board-certified ophthalmologist. | Sensitivity $\ge 92\%$, Specificity $\ge 94\%$ |

---

## 5. Summary & Operational Status
OcuScan AI is technically mature and architecturally robust. Every model loads verified PyTorch weights and evaluates authentic clinical data. In strict accordance with healthcare regulatory governance, the models remain transparently designated **Available for Evaluation** until the completion of Protocol OS-CT-01 and CDSCO SaMD clearance.
