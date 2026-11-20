# OcuScan AI — Regulatory Compliance & SaMD Checklist

**Document ID:** DOC-REG-2026-V1  
**Classification:** Software as a Medical Device (SaMD)  
**Applicable Jurisdictions:** India (CDSCO MDR 2017) | United States (US FDA 21 CFR 860 / 886) | European Union (EU MDR 2017/745)  
**Effective Date:** October 2026  
**Clinical Status:** **RESEARCH USE ONLY (RUO)** — Not Cleared for Commercial Diagnostic Use  

---

## 1. Intended Use & Jurisdictional Classification

### 1.1 Statement of Intended Use
> **OcuScan AI** is an investigational, multi-modal anterior ocular computer vision software system intended to analyze digital photographs of the human eye (palpebral conjunctiva, bulbar conjunctiva, sclera, crystalline lens, and eyelid margins). The platform generates non-invasive physiological estimates (continuous hemoglobin in g/dL) and categorical screening risk alerts for visible conjunctival hyperemia, scleral icterus, nuclear cataract opacification, and hordeolum/stye.
>
> **Target Population:** Adult individuals aged 18–120 under trained operator guidance.  
> **Clinical Role:** Triage screening aid and clinical decision support. **It does not provide definitive medical diagnoses, does not prescribe pharmaceutical interventions, and does not replace venous laboratory testing (CBC, serum bilirubin) or slit-lamp biomicroscopy by licensed ophthalmologists.**

### 1.2 Jurisdictional Risk Classification

| Regulatory Body | Legal Framework | Device Classification | Regulatory Pathway | Current Status |
| :--- | :--- | :--- | :--- | :--- |
| **CDSCO (India)** | Medical Device Rules (MDR), 2017 (Rule 20) | **Class B SaMD** (Low-to-Moderate Risk screening software) | Form MD-14 (Import) / Form MD-5 (Manufacturing), Clinical Investigation Form MD-22 | **Pre-Submission / Protocol Ready** (Not Yet Approved) |
| **US FDA** | 21 CFR 860 / 21 CFR 886.1570 | **Class II SaMD** (Ophthalmic Computerized Screening System) | 510(k) Premarket Notification or De Novo Classification | **Pre-Submission Ready** (Not Yet Cleared) |
| **EU MDR** | Regulation (EU) 2017/745 (Annex VIII, Rule 11) | **Class IIa SaMD** (Software providing information for triage decisions) | Notified Body Conformity Assessment (CE Mark) | **Pre-Submission Ready** (Not Yet Certified) |

---

## 2. Comprehensive Regulatory Compliance Checklist

### 2.1 Quality Management System (ISO 13485:2016)

| Req ID | Standard Clause | Requirement Description | Implementation in OcuScan AI | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **QMS-01** | Clause 4.2 | Documentation of device master record (DMR) & device history record (DHR). | Device specifications, dependency manifests, and dataset provenance tracked in repository. | **IMPLEMENTED** (Codebase DMR) |
| **QMS-02** | Clause 7.3.2 | Design & Development Planning with explicit user needs and clinical inputs. | Clinical targets specified in `AGENTS.md` and `docs/REGULATORY_AND_CLINICAL_ROADMAP.md`. | **IMPLEMENTED** |
| **QMS-03** | Clause 7.3.7 | Formal design verification & validation (V&V) against reference standards. | 245 automated regression and unit tests in `tests/` verifying all models and API endpoints. | **IMPLEMENTED** |
| **QMS-04** | Clause 7.5.8 | Identification, traceability, and patient data segregation. | Patient/session-isolated splits; zero image persistence without explicit consent. | **IMPLEMENTED** |
| **QMS-05** | Clause 8.2.1 | Post-market feedback, complaint handling, and vigilance reporting. | Formal SOP drafted in `docs/COMMERCIAL_DEPLOYMENT_GUIDE.md`; requires active clinical sponsor. | **DOCUMENTED / PRE-MARKET** |

---

### 2.2 Medical Device Software Lifecycle (IEC 62304:2006 + A1:2015)

| Req ID | Clause | Software Safety Classification: **Class B** | Technical Implementation | Status |
| :--- | :--- | :--- | :--- | :--- |
| **SFT-01** | Clause 5.1 | Software Development Planning & version control governance. | Git repository with strict branching, deterministic seed locking, and hash verification. | **IMPLEMENTED** |
| **SFT-02** | Clause 5.2 | Software requirements specification (SRS) including safety thresholds. | Input quality thresholds (Laplacian >= 20.0, luminance [30, 230]) and WHO 2024 hemoglobin cutoffs. | **IMPLEMENTED** |
| **SFT-03** | Clause 5.3 | Software architectural design separating UI, business logic, and inference. | Clean modular architecture: `src/models/`, `src/preprocessing/`, `src/inference/`, `src/database/`. | **IMPLEMENTED** |
| **SFT-04** | Clause 5.5 | Software unit & integration testing with code coverage and regression gates. | 245 pytest tests covering models, image processing, database cascading, and PDF/Email delivery. | **IMPLEMENTED** |
| **SFT-05** | Clause 7.1 | Software risk analysis for hazardous situations arising from software anomalies. | Documented in ISO 14971 FMEA matrix below; safety gates prevent unvalidated outputs. | **IMPLEMENTED** |

---

### 2.3 Medical Device Risk Management (ISO 14971:2019) — Failure Modes & Effects Analysis (FMEA)

| Hazard ID | Potential Failure Mode | Clinical Severity | Probability | Risk Level | Implemented Mitigation / Safety Gate | Residual Risk |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| **HAZ-01** | **Laptop Webcam Optical Domain Shift:** Sensor auto-white-balance, auto-exposure, and compression distorting conjunctival pallor. | Moderate (Incorrect Hb estimate) | High (if unmitigated) | High | **Camera-Domain Validation Gate:** Automatically blocks webcam inference by default unless researcher experimental override is explicitly passed. | **Low** |
| **HAZ-02** | **Cataract Lens Resolution Failure:** Standard wide-angle smartphone photo unable to resolve crystalline lens opacities inside anterior chamber. | Moderate (Missed early cataract) | High | High | **Optical Hardware Requirement:** Slit-lamp biomicroscopy or anterior macro-lens adapter required. Image quality pre-check validates contrast & resolution. | **Low** |
| **HAZ-03** | **Fabricated Biochemical Numbers (Bilirubin):** Presenting visual scleral discoloration as exact quantitative total serum bilirubin (mg/dL). | High (Diagnostic confusion) | High | Critical | **Strict No-Fabrication Rule (AGENTS.md):** Quantitative bilirubin estimation is strictly blocked. Only categorical visual scleral icterus screening is provided. | **Controlled** |
| **HAZ-04** | **Severe Blurry or Dark Input:** Image motion blur obscuring capillary micro-vasculature. | Low (Inconclusive view) | Medium | Medium | **Laplacian Variance Quality Gate:** Sharpness (< 20.0) and luminance (< 30 or > 230) check automatically halts analysis and provides actionable retake guidance. | **Low** |
| **HAZ-05** | **Data Leakage & Overfitting:** Re-using the same patient's multiple photos across training and validation/test partitions. | High (Artificially inflated metrics) | High | High | **Patient-Isolated Group Splits:** Cross-validation splits strictly enforced by subject/session ID (GroupKFold). Zero sample overlap. | **Controlled** |
| **HAZ-06** | **Misinterpretation of Research Tool as Certified Diagnosis:** Non-clinical participant assumes output is a medical diagnosis. | High (Delayed formal care) | Medium | High | **Mandatory Disclaimers & Informed Consent:** Topbar banner, 2-page PDF disclaimers, and Step 2 explicit consent acknowledge "RESEARCH USE ONLY". | **Low** |

---

### 2.4 Data Protection, Privacy & Cybersecurity (DPDP Act 2023 / HIPAA / GDPR)

| Req ID | Regulation Clause | Legal Requirement | Technical Implementation | Status |
| :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | DPDP Act Sec 6 / GDPR Art 7 | Explicit, itemized, withdrawable informed consent prior to data processing. | Step 2 modal collects separate consents for research screening, session storage, external AI, and email delivery. | **IMPLEMENTED** |
| **SEC-02** | DPDP Act Sec 12 / GDPR Art 17 | Right to Erasure / Right to be Forgotten. | `DELETE /api/session/{id}` and `DELETE /api/user/{id}` execute cascading relational purge of all records and metadata. | **IMPLEMENTED** |
| **SEC-03** | HIPAA Security Rule / DPDP Sec 8 | Data minimization and separation of clinical images from direct patient identifiers. | Model feature extractors operate on in-memory cropped ocular arrays. No direct patient names in model tensors. | **IMPLEMENTED** |
| **SEC-04** | Confidentiality in Transmission | Encryption of email and network traffic; no credential leaks. | TLS enforced; non-sensitive email subjects (no medical diagnoses on phone lockscreens); masked credentials. | **IMPLEMENTED** |

---

## 3. Pre-Market Clearance Blockers & Remaining Dependencies

> [!CAUTION]
> **Commercial Release Prohibition:** Under CDSCO Medical Device Rules 2017 and FDA 21 CFR 860, OcuScan AI **CANNOT** be marketed, sold, or promoted for clinical diagnostic or screening triage in healthcare facilities until the following external dependencies are completed:

1. **Prospective Multi-Center Clinical Investigation:**
   - Ethical Committee (IEC/IRB) approval at minimum 3 accredited tertiary eye hospitals / research centers (e.g. AIIMS New Delhi, Sankara Nethralaya Chennai, LVPEI Hyderabad).
   - Minimum sample size of $N = 1,200$ prospectively enrolled subjects with matched gold-standard laboratory reference tests (Automated hematology analyzer Sysmex XN-1000 for Hb; Roche Cobas 8000 for Bilirubin; LOCS III slit-lamp exam by two independent masked ophthalmologists).
2. **Formal ISO 13485:2016 Audit:**
   - Certification of the sponsor's Quality Management System by an accredited Notified Body (e.g., TUV, BSI, or CDSCO-notified body in India).
3. **CDSCO Sugam Portal Filing:**
   - Submission of Device Master File (DMF), Plant Master File (PMF), Performance Evaluation Report (PER), and Software Validation Dossier via Form MD-14/MD-5.
4. **Post-Market Surveillance (PMS) Infrastructure:**
   - Real-time model drift monitoring, calibration decay tracking, and adverse event reporting system operationalized.
