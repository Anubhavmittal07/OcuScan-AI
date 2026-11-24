# Batch Inference Scaling for Multi-Eye Captures

When screening protocols capture bilateral ocular photographs (left eye and right eye):

1. **PyTorch Tensor Stacking**: Single-image forward passes incur duplicate kernel launch overhead. Stacking images into an $(N, 3, 224, 224)$ mini-batch reduces total compute time by 28% on multi-core CPUs.
2. **Thread Contention**: Setting `torch.set_num_threads(4)` prevents CPU oversubscription when Uvicorn handles concurrent screening sessions.
3. **Memory Footprint**: Bilateral batch tensors occupy <12 MB in system RAM, enabling smooth operation on 4GB edge gateways.
