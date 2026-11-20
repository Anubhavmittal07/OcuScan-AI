import time
import torch
from PIL import Image
from src.inference.unified_service import get_inference_service

service = get_inference_service()
torch.set_num_threads(4)
img_path = r"test_images\demo\normal.jpeg"
pil_img = Image.open(img_path).convert("RGB")
prep = service._prepare_image_input(pil_img)
resized = prep["final_model_input"]
tensor = service._transform(resized).unsqueeze(0).to(service.device)

# 1. Pure PyTorch Forward Pass for all 5 models
t0 = time.time()
with torch.no_grad():
    m1 = service._get_anemia_model()(tensor)
    m2 = service._get_slid_model()(tensor)
    m3 = service._get_jaundice_model()(tensor)
    m4 = service._get_cataract_model()(tensor)
    m5 = service._get_stye_model()(tensor)
t1 = time.time()
print(f"PURE FORWARD PASS FOR ALL 5 MODELS: {t1 - t0:.4f} s ({((t1-t0)/5)*1000:.1f} ms per model!)")
