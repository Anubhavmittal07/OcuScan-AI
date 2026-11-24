# FHIR & HL7 Interoperability Specification

EyeHealthAI screening summaries map to HL7 FHIR (Fast Healthcare Interoperability Resources) R4:

### Resource Mapping
- **DiagnosticReport**: Represents the complete ocular screening session.
  - `status`: `preliminary` (investigational research prototype).
  - `category`: `LP29708-2` (Cardiology/Hematology point-of-care screening).
- **Observation (Hemoglobin)**:
  - `code`: LOINC `718-7` (Hemoglobin [Mass/volume] in Blood).
  - `valueQuantity`: Predicted numerical value ($g/dL$) with 95% confidence bounds.
- **Observation (Hyperemia / SLID)**:
  - `code`: SNOMED-CT `43878008` (Conjunctival hyperemia).
