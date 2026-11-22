# Contributing to EyeHealthAI (OcuScan)

Thank you for your interest in contributing to the EyeHealthAI clinical computer vision research framework.

## Clinical Safety & Research Principles
1. **Investigational Prototype**: EyeHealthAI is an investigational medical AI tool. It does not provide certified medical diagnoses.
2. **Ground Truth Integrity**: Never commit synthetic, altered, or fabricated laboratory reference labels.
3. **Data Privacy**: Never commit patient images, recognizable faces, or unanonymized metadata.
4. **Leakage Prevention**: All model evaluations must adhere to strict zero-leakage subject-level train/validation/test splits.

## Development Workflow
1. Fork and clone the repository.
2. Create an isolated virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the full verification suite before submitting PRs: `pytest tests/ -v`.
5. Maintain standard Conventional Commits naming (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
