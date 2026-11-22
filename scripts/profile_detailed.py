import time
from PIL import Image
from src.inference.unified_service import get_inference_service

def time_block(name, fn):
    t0 = time.time()
    res = fn()
    t1 = time.time()
    print(f"[{t1 - t0:.3f} s] {name}")
    return res

def profile_predict_unified():
    service = get_inference_service()
    img_path = r"test_images\demo\normal.jpeg"
    pil_img = Image.open(img_path).convert("RGB")

    print("\n--- PROFILING DETAILED PREDICT_UNIFIED ---")
    
    t_start = time.time()
    res = service.predict_unified([pil_img])
    t_end = time.time()
    print(f"\nTOTAL predict_unified: {t_end - t_start:.3f} s")

if __name__ == '__main__':
    profile_predict_unified()
