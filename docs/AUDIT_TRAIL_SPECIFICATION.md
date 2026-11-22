# Audit Trail & Session Export Specification

## Cryptographic Provenance
To facilitate integration with Hospital Information Systems (HIS) and Electronic Health Records (EHR):
- Every screening session generates a SHA-256 integrity hash combining participant identifier, UTC timestamp, quantitative predictions, and quality indices.
- Session export endpoint (`/api/export`) emits standardized FHIR-compatible JSON summaries.
- Any post-hoc modification to the session database invalidates the audit hash.
