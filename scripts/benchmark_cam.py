import time
import torch
from PIL import Image
from src.inference.unified_service import get_inference_service

service = get_inference_service()
img_path = r"test_images\demo\normal.jpeg"
pil_img = Image.open(img_path).convert("RGB")
prep = service._prepare_image_input(pil_img)
model_input = prep["final_model_input"]

# Benchmark pure forward pass of ResNet50
model = service._get_anemia_model()
tensor = service.preprocess_tensor(model_input).to(service.device)

t0 = time.time()
with torch.no_grad():
    for _ in range(5):
        out = model(tensor)
t1 = time.time()
print(f"ResNet-50 pure forward pass (average of 5): {(t1 - t0)/5:.4f} s")

# Benchmark pure forward pass of MobileNetV3
mobilenet = service._get_slid_model()
t0 = time.time()
with torch.no_grad():
    for _ in range(5):
        out = mobilenet(tensor)
t1 = time.time()
print(f"MobileNetV3 pure forward pass (average of 5): {(t1 - t0)/5:.4f} s")

# Benchmark Grad-CAM
from src.inference.attribution_cam import compute_cam
t0 = time.time()
cam_res = compute_cam(model, tensor, target_layer=model.layer4)
t1 = time.time()
print(f"ResNet-50 Grad-CAM time: {t1 - t0:.4f} s")
