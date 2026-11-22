import time
from PIL import Image
from src.preprocessing.advanced_pipeline import (
    normalize_image_orientation,
    detect_and_crop_ocular_region,
    enhance_ocular_quality_conservatively,
    evaluate_quality_gate,
    pil_to_base64_thumbnail
)

img_path = r"test_images\demo\normal.jpeg"
pil_img = Image.open(img_path).convert("RGB")

t0 = time.time()
norm_orig = normalize_image_orientation(pil_img)
print(f"normalize_image_orientation: {time.time() - t0:.4f} s")

t0 = time.time()
detection_res = detect_and_crop_ocular_region(norm_orig)
cropped_img = detection_res.pop("cropped_image", norm_orig)
is_macro_flag = detection_res.get("is_macro", False)
print(f"detect_and_crop_ocular_region: {time.time() - t0:.4f} s")

t0 = time.time()
enhanced_crop, enhancement_res = enhance_ocular_quality_conservatively(cropped_img, is_macro=is_macro_flag)
print(f"enhance_ocular_quality_conservatively: {time.time() - t0:.4f} s")

t0 = time.time()
quality_gate_res = evaluate_quality_gate(norm_orig, enhanced_crop, detection_res, enhancement_res)
print(f"evaluate_quality_gate: {time.time() - t0:.4f} s")

t0 = time.time()
t_b64_1 = pil_to_base64_thumbnail(norm_orig, max_dim=320)
t_b64_2 = pil_to_base64_thumbnail(cropped_img, max_dim=320)
t_b64_3 = pil_to_base64_thumbnail(enhanced_crop, max_dim=320)
print(f"pil_to_base64_thumbnail x3: {time.time() - t0:.4f} s")
