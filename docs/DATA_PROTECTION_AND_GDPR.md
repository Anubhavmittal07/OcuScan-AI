# Data Protection & GDPR Patient Privacy Lifecycle

## Core Principles
1. **Informed Consent**: Explicit participant consent is captured on-screen before camera activation.
2. **Zero Unconsented Persistence**: If consent is declined, photograph tensors are processed exclusively in volatile memory and purged immediately after inference.
3. **Right to Erasure (GDPR Art. 17)**: The `/api/user/delete` endpoint enables instant, permanent purging of user profile data and all associated screening records.
4. **Data Minimization**: Reports store derived clinical staging, chromatic indices, and attribution metrics rather than uncompressed high-resolution face photographs.
