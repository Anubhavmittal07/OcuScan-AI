import time
from PIL import Image
from src.inference.unified_service import get_inference_service

def benchmark_steps():
    service = get_inference_service()
    img_path = r"test_images\demo\normal.jpeg"
    pil_img = Image.open(img_path).convert("RGB")

    print("--- BENCHMARKING UNIFIED INFERENCE STEPS ---")

    # 1. Image preparation (landmarking, CLAHE, cropping)
    t0 = time.time()
    prep = service._prepare_image_input(pil_img)
    t1 = time.time()
    print(f"1. _prepare_image_input: {t1 - t0:.3f} s")

    # 2. Individual models
    # Anemia (ResNet-50 + Grad-CAM)
    t0 = time.time()
    res_anemia = service.predict_anemia([pil_img])
    t1 = time.time()
    print(f"2a. predict_anemia (ResNet50 + CAM): {t1 - t0:.3f} s")

    # SLID (MobileNetV3 + Grad-CAM)
    t0 = time.time()
    res_slid = service.predict_conjunctival_injection([pil_img])
    t1 = time.time()
    print(f"2b. predict_slid (MobileNetV3 + CAM): {t1 - t0:.3f} s")

    # Jaundice (MobileNetV3 + Grad-CAM)
    t0 = time.time()
    res_jaund = service.predict_scleral_icterus([pil_img])
    t1 = time.time()
    print(f"2c. predict_jaundice (MobileNetV3 + CAM): {t1 - t0:.3f} s")

    # Cataract (MobileNetV3 + Grad-CAM)
    t0 = time.time()
    res_cat = service.predict_cataract([pil_img])
    t1 = time.time()
    print(f"2d. predict_cataract (MobileNetV3 + CAM): {t1 - t0:.3f} s")

    # Stye (MobileNetV3 + Grad-CAM)
    t0 = time.time()
    res_stye = service.predict_stye([pil_img])
    t1 = time.time()
    print(f"2e. predict_stye (MobileNetV3 + CAM): {t1 - t0:.3f} s")

    # 3. Segmentation
    t0 = time.time()
    from src.segmentation import get_ocular_segmenter
    seg_obj = get_ocular_segmenter().segment(prep["image"])
    seg_data = seg_obj.to_dict(include_masks=False)
    t1 = time.time()
    print(f"3. Ocular Segmentation: {t1 - t0:.3f} s")

    # 4. Reference Retrieval
    t0 = time.time()
    from src.inference.reference_retrieval import get_reference_retrieval_service
    ref_data = get_reference_retrieval_service(device=service.device).query(prep["image"], top_k=3)
    t1 = time.time()
    print(f"4. Reference Retrieval: {t1 - t0:.3f} s")

    # 5. Secondary Vision
    t0 = time.time()
    from src.inference.secondary_vision import get_secondary_vision_service
    sec_data = get_secondary_vision_service().analyze_image(prep["image"])
    t1 = time.time()
    print(f"5. Secondary Vision: {t1 - t0:.3f} s")

    # 6. Personalized AI
    t0 = time.time()
    from src.inference.personalized_ai import PersonalizedAIService
    p_service = PersonalizedAIService()
    p_data = p_service.generate_personalized_explanation(
        image=prep["image"],
        anemia_result=res_anemia,
        slid_result=res_slid,
        jaundice_result=res_jaund,
        cataract_result=res_cat,
        stye_result=res_stye
    )
    t1 = time.time()
    print(f"6. Personalized AI: {t1 - t0:.3f} s")

if __name__ == '__main__':
    benchmark_steps()
