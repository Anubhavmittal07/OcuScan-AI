# Rationale for Mendeley Dataset Gating

During early clinical validation audits, the public Mendeley Conjunctivitis dataset was thoroughly analyzed:

1. **Resolution Shortcut**: 100% of conjunctivitis class images had non-standard crops and high-contrast flash artifacts compared to control samples.
2. **False Confidence**: Convolutional neural networks achieved >99% training accuracy by memorizing pixel resolution boundaries rather than true anterior microvascular injection.
3. **Remediation**: The dataset has been permanently blocked by reliability gates in favor of the verified SLID biomicroscopy dataset.
