# Edge Device Optimization & Mobile Inference

## Architecture Considerations
For point-of-care mobile deployment (e.g. community health centers and field clinics):
1. **Lightweight Backbones**: MobileNetV3-Small is prioritized for classification tasks due to its minimal parameter footprint (~2.5M params) and low memory bandwidth requirements.
2. **Quantization Strategies**: Post-training dynamic int8 quantization yields a 3.4x latency reduction on ARM64 processors with <0.02 degradation in AUROC.
3. **Memory Footprint**: Input tensors are constrained to 224x224 RGB to maintain peak memory usage under 150MB during forward passes.
