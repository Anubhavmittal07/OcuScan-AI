# Multi-Center Dataset Cross-Validation Strategy

## Subject Leakage Prevention
In clinical image analysis, multiple photographs are often collected from the same individual patient.
- **Failure Mode**: Standard random row-based splitting leaks identity and ambient lighting patterns between train and test sets, inflating apparent accuracy.
- **EyeHealthAI Solution**: Subject-level GroupKFold splitting ensures 100% of photographs from any given participant are assigned strictly to either training, validation, or test partitions. Zero cross-fold patient overlap.
