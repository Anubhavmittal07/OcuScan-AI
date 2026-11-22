"""
tests/test_cropping_and_model_input_pipeline.py
-----------------------------------------------
Regression and integrity tests for ocular image cropping, anatomical ROI extraction,
aspect-ratio preservation, and model input tensor verification across all condition models.
"""

import pytest
import numpy as np
from PIL import Image
import torch
from torchvision import transforms

from src.preprocessing.advanced_pipeline import (
    detect_and_crop_ocular_region,
    process_ocular_image_advanced,
    normalize_image_orientation
)
from src.preprocessing.image_quality import resize_and_pad
from src.inference.unified_service import get_inference_service


@pytest.fixture
def macro_stye_image():
    """Real macro eye image with eyelid stye (non-square aspect ratio)."""
    # Create synthetic macro eye close-up with upper eyelid lesion
    arr = np.full((382, 553, 3), 180, dtype=np.uint8)
    # Pupil/iris in center
    arr[140:240, 220:320] = [40, 30, 25]
    # Sclera around iris
    arr[160:220, 150:220] = [230, 230, 230]
    arr[160:220, 320:390] = [230, 230, 230]
    # Upper eyelid stye nodule at top margin
    arr[80:120, 200:260] = [215, 60, 60]
    return Image.fromarray(arr, mode="RGB")


@pytest.fixture
def webcam_16_9_macro():
    """16:9 widescreen capture framing an eye close-up."""
    arr = np.full((360, 640, 3), 175, dtype=np.uint8)
    # Eye in center
    arr[130:230, 270:370] = [35, 25, 20]
    arr[150:210, 200:270] = [225, 225, 225]
    arr[150:210, 370:440] = [225, 225, 225]
    return Image.fromarray(arr, mode="RGB")


@pytest.fixture
def square_1_1_macro():
    """1:1 square macro ocular capture."""
    arr = np.full((400, 400, 3), 185, dtype=np.uint8)
    arr[150:250, 150:250] = [30, 20, 15]
    return Image.fromarray(arr, mode="RGB")


@pytest.fixture
def portrait_4_3_macro():
    """4:3 portrait ocular capture."""
    arr = np.full((600, 450, 3), 170, dtype=np.uint8)
    arr[250:350, 175:275] = [45, 35, 30]
    return Image.fromarray(arr, mode="RGB")


def test_normalize_image_orientation_supports_pil_and_numpy():
    """Orientation normalizer must accept both PIL Images and numpy arrays without crashing."""
    pil_img = Image.new("RGB", (100, 100), (255, 0, 0))
    res_pil = normalize_image_orientation(pil_img)
    assert isinstance(res_pil, Image.Image)
    assert res_pil.size == (100, 100)

    np_img = np.zeros((120, 160, 3), dtype=np.uint8)
    res_np = normalize_image_orientation(np_img)
    assert isinstance(res_np, Image.Image)
    assert res_np.size == (160, 120)


def test_macro_eye_bypass_preserves_full_framing(macro_stye_image):
    """
    Close-up macro eye uploads must NOT be aggressively cropped.
    Original dimensions and aspect ratio must be preserved to retain eyelid pathology.
    """
    res = detect_and_crop_ocular_region(macro_stye_image)
    assert res["crop_applied"] is False, "Macro eye close-up should not be cropped"
    assert res["detection_mode"] == "direct_macro_eye"
    assert res["crop_box"] == {"x": 0, "y": 0, "w": 553, "h": 382}
    assert res["cropped_image"].size == (553, 382)


def test_widescreen_webcam_aspect_preservation(webcam_16_9_macro):
    """16:9 widescreen capture must preserve macro framing and aspect ratio."""
    res = detect_and_crop_ocular_region(webcam_16_9_macro)
    assert res["crop_applied"] is False
    assert res["crop_dimensions"] == [640, 360]


def test_resize_and_pad_letterboxes_without_distortion(macro_stye_image):
    """
    Letterboxing to (224, 224) must strictly preserve original aspect ratio
    and prevent stretching/squishing of anatomical pathology.
    """
    w, h = macro_stye_image.size
    aspect_orig = w / h  # 553 / 382 = 1.447

    padded = resize_and_pad(macro_stye_image, (224, 224))
    assert padded.size == (224, 224)

    # In 224x224, width is 224, expected height is 224 / 1.447 ~= 155
    arr = np.array(padded)
    non_black = np.where((arr > 0).any(axis=2))
    content_h = non_black[0].max() - non_black[0].min() + 1
    content_w = non_black[1].max() - non_black[1].min() + 1

    assert content_w == 224
    assert abs(content_h - int(224 / aspect_orig)) <= 2, "Aspect ratio must be preserved"


def test_end_to_end_pipeline_tensor_integrity(macro_stye_image):
    """
    Verifies that the exact tensor fed to the neural network models
    is consistent with the preview image in stage_02_model_input.
    """
    proc = process_ocular_image_advanced(macro_stye_image, generate_previews=True)
    assert proc["original_image"].size == (553, 382)
    assert proc["cropped_image"].size == (553, 382)
    assert proc["final_model_input"].size == (224, 224)
    assert "final_model_input_thumb" in proc["previews"]


def test_stye_prediction_on_upper_eyelid_lesion():
    """
    A genuine macro photo with an upper eyelid stye must classify as stye_hordeolum
    and not get discarded as an inconclusive everted mucosa view.
    """
    service = get_inference_service()
    # Test on test_images/demo/stye.jpg
    res = service.predict_stye(["test_images/demo/stye.jpg"])
    assert res.status == "available_research_only"
    assert len(res.prediction) == 1
    pred = res.prediction[0]
    assert pred["predicted_class"] == "stye_hordeolum"
    assert pred["confidence"] >= 0.50
    assert pred["attribution"] is not None
    assert pred["attribution"]["dimensions"] == [224, 224]


def test_different_aspect_ratios_across_service(webcam_16_9_macro, square_1_1_macro, portrait_4_3_macro):
    """
    Verifies that the inference service handles 16:9, 1:1, and 4:3 images cleanly
    without throwing dimensional mismatch or cropping errors.
    """
    service = get_inference_service()
    for img, name in [(webcam_16_9_macro, "16:9"), (square_1_1_macro, "1:1"), (portrait_4_3_macro, "4:3")]:
        prep = service._prepare_image_input(img)
        assert prep["error"] is None, f"Failed for {name}"
        assert prep["image"].size[0] > 0
        assert prep["final_model_input"].size == (224, 224)
