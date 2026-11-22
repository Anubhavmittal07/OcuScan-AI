"""
image_quality.py - Image loading, RGB conversion, and ocular image quality checks.
"""

import os
from typing import Tuple, Dict, Any, Optional
import numpy as np
from PIL import Image, ImageFile, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = True


def safe_load_image(filepath: str) -> Optional[Image.Image]:
    """Safely loads an image, converts to RGB, handling broken headers."""
    if not os.path.exists(filepath):
        return None
    try:
        with Image.open(filepath) as img:
            img.load()
            # If RGBA, blend onto neutral black or white background
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (0, 0, 0))
                rgb_img.paste(img, mask=img.split()[3])
                return rgb_img
            elif img.mode != 'RGB':
                return img.convert('RGB')
            else:
                return img.copy()
    except Exception as e:
        print(f"Error loading image {filepath}: {e}")
        return None


def calculate_image_quality(img: Image.Image) -> Dict[str, float]:
    """
    Computes objective image quality indicators:
      - brightness (mean luminance [0, 255])
      - contrast (standard deviation of luminance)
      - sharpness (variance of Laplacian proxy via numpy 2D gradients)
    """
    gray = np.array(img.convert('L'), dtype=np.float32)
    
    brightness = float(np.mean(gray))
    contrast = float(np.std(gray))
    
    # 2D discrete Laplacian filter approximation for sharpness
    # [ 0,  1,  0]
    # [ 1, -4,  1]
    # [ 0,  1,  0]
    padded = np.pad(gray, 1, mode='edge')
    laplacian = (
        padded[1:-1, :-2] + padded[1:-1, 2:] +
        padded[:-2, 1:-1] + padded[2:, 1:-1] -
        4.0 * gray
    )
    sharpness = float(np.var(laplacian))
    
    return {
        'brightness': round(brightness, 2),
        'contrast': round(contrast, 2),
        'sharpness': round(sharpness, 2),
        'is_too_dark': brightness < 30.0,
        'is_too_bright': brightness > 230.0,
        'is_blurry': sharpness < 20.0
    }


def validate_cataract_imaging_requirements(
    img: Image.Image,
    capture_source: str = "upload",
    modality: Optional[str] = None,
    filename: Optional[str] = None,
    experimental_override: bool = False
) -> Dict[str, Any]:
    """
    Validates optical and anatomical suitability for nuclear cataract evaluation.
    Enforces anterior segment slit-lamp biomicroscopy resolution, sharpness, and modality dependencies.
    Prevents ordinary webcam or external-eye images from receiving false cataract predictions,
    while permitting genuine slit-lamp biomicroscopy images.
    """
    w, h = img.size
    is_resolution_ok = (w >= 180 and h >= 180 and max(w, h) / max(min(w, h), 1) <= 4.0)

    # Scale-invariant sharpness evaluation on max-1024 thumbnail
    thumb_sharp = img.copy()
    if max(w, h) > 1024:
        thumb_sharp.thumbnail((1024, 1024))
    gray_sharp = np.array(thumb_sharp.convert("L"), dtype=np.float32)
    padded = np.pad(gray_sharp, 1, mode="edge")
    laplacian = (
        padded[1:-1, :-2] + padded[1:-1, 2:] +
        padded[:-2, 1:-1] + padded[2:, 1:-1] -
        4.0 * gray_sharp
    )
    sharpness = float(np.var(laplacian))
    is_sharp = sharpness >= 10.0

    hardware_note = (
        "Slit-lamp biomicroscopy or high-magnification anterior macro adapter required. "
        "Ordinary wide-angle phone/webcam cameras under ambient lighting cannot inspect crystalline lens internal nuclear densities."
    )

    warnings = []
    if not is_resolution_ok:
        warnings.append(f"Image dimensions ({w}x{h}) are unsuitable for anterior segment biomicroscopy.")
    if not is_sharp:
        warnings.append("Pupillary aperture is too blurry to resolve LOCS III nuclear opacification.")

    is_webcam = str(capture_source).lower() == "webcam"
    if is_webcam and not experimental_override:
        warnings.append("BLOCKED (CAMERA-DOMAIN VALIDATION GATE): Nuclear cataract evaluation requires focused slit-lamp biomicroscopy illumination.")
        warnings.append("Webcam sensors and ambient room lighting cannot inspect crystalline lens nuclear density.")
        return {
            "is_suitable": False,
            "is_webcam": True,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": False,
            "modality_type": "blocked_webcam",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": "Webcam sensors cannot section crystalline lens nucleus"
        }

    if experimental_override:
        warnings.append("RESEARCHER EXPERIMENTAL OVERRIDE ACTIVE: Slit-lamp domain requirement bypassed for uncalibrated capture.")
        return {
            "is_suitable": is_resolution_ok and is_sharp,
            "is_webcam": is_webcam,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": True,
            "modality_type": "experimental_override",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": None
        }

    # Explicit modality metadata check
    norm_mod = str(modality or "").strip().lower()
    if norm_mod in ("slit_lamp", "slit", "biomicroscopy", "locs_iii", "remidio_psl", "topcon_dc3", "catscreen"):
        return {
            "is_suitable": is_resolution_ok and is_sharp,
            "is_webcam": False,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": True,
            "modality_type": "explicit_slit_lamp_metadata",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": None
        }

    if norm_mod in ("webcam", "ambient", "external_eye", "macro_camera", "smartphone_ambient", "diffuse"):
        warnings.append("External eye capture under diffuse ambient lighting cannot section crystalline lens.")
        return {
            "is_suitable": False,
            "is_webcam": False,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": False,
            "modality_type": "unsupported_external_modality",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": "Declared modality is external diffuse ambient photography"
        }

    # Content-based optical biomicroscopy verification for missing or ambiguous modality metadata
    fname = str(filename or getattr(img, "filename", "") or "").lower()
    has_slit_provenance = any(k in fname for k in ("slit", "locs", "psl", "catscreen", "topcon", "haag", "zeiss", "keeler", "biomicroscop"))

    # Convert thumbnail (256x256) for fast optical feature extraction
    thumb_opt = img.copy()
    thumb_opt.thumbnail((256, 256))
    arr_opt = np.array(thumb_opt.convert("RGB"))
    th_h, th_w, _ = arr_opt.shape

    gray_opt = np.dot(arr_opt[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.float32)

    bw = max(1, int(min(th_h, th_w) * 0.08))
    border = np.concatenate([
        gray_opt[:bw, :].flatten(),
        gray_opt[-bw:, :].flatten(),
        gray_opt[:, :bw].flatten(),
        gray_opt[:, -bw:].flatten()
    ])
    border_dark_pct = float(np.mean(border < 50.0) * 100.0)
    border_mean = float(np.mean(border))

    r_ch, g_ch, b_ch = arr_opt[..., 0], arr_opt[..., 1], arr_opt[..., 2]
    skin_mask = (
        (r_ch > 95) & (g_ch > 40) & (b_ch > 20) &
        ((np.maximum(np.maximum(r_ch, g_ch), b_ch) - np.minimum(np.minimum(r_ch, g_ch), b_ch)) > 15) &
        (np.abs(r_ch.astype(int) - g_ch.astype(int)) > 15) &
        (r_ch > g_ch) & (r_ch > b_ch)
    )
    skin_pct = float(np.mean(skin_mask) * 100.0)

    col_means = np.mean(gray_opt, axis=0)
    col_std = float(np.std(col_means))
    peak_contrast = float((np.max(col_means) - np.min(col_means)) / (np.mean(col_means) + 1e-5))

    is_dark_field = (border_dark_pct >= 40.0 or border_mean <= 55.0)
    is_slit_beam = (col_std >= 25.0 and peak_contrast >= 0.65)
    is_diffuse_external = (skin_pct >= 55.0 and border_mean >= 95.0 and border_dark_pct < 10.0 and not has_slit_provenance)

    if is_diffuse_external:
        warnings.append("External ocular photograph captured under diffuse ambient lighting. Slit-lamp biomicroscopy illumination is required to inspect internal lens nuclear density.")
        return {
            "is_suitable": False,
            "is_webcam": False,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": False,
            "modality_type": "diffuse_ambient_external",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": "Diffuse ambient lighting detected; lack of pupillary optical slit-beam"
        }

    if is_dark_field:
        return {
            "is_suitable": is_resolution_ok and is_sharp,
            "is_webcam": False,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": True,
            "modality_type": "biomicroscopy_dark_field",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": None
        }

    if has_slit_provenance and (is_slit_beam or border_dark_pct >= 15.0 or col_std >= 18.0):
        return {
            "is_suitable": is_resolution_ok and is_sharp,
            "is_webcam": False,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": True,
            "modality_type": "verified_slit_lamp_provenance",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": None
        }

    if is_slit_beam and skin_pct < 55.0:
        return {
            "is_suitable": is_resolution_ok and is_sharp,
            "is_webcam": False,
            "resolution_ok": is_resolution_ok,
            "sharpness_ok": is_sharp,
            "modality_ok": True,
            "modality_type": "optical_slit_beam_verified",
            "optical_dependency": hardware_note,
            "warnings": warnings,
            "gate_reason": None
        }

    warnings.append("Missing or ambiguous slit-lamp modality metadata. Image lacks verifiable biomicroscopic optical slit-beam sectioning.")
    return {
        "is_suitable": False,
        "is_webcam": False,
        "resolution_ok": is_resolution_ok,
        "sharpness_ok": is_sharp,
        "modality_ok": False,
        "modality_type": "ambiguous_or_unsupported_modality",
        "optical_dependency": hardware_note,
        "warnings": warnings,
        "gate_reason": "Missing or ambiguous modality metadata; optical sectioning unverified"
    }


def resize_and_pad(img: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> Image.Image:
    """
    Resizes image maintaining aspect ratio and pads to target_size,
    avoiding geometric distortion of the ocular structure.
    """
    img_copy = img.copy()
    img_copy.thumbnail(target_size, Image.Resampling.BILINEAR)
    new_img = Image.new('RGB', target_size, (0, 0, 0))
    paste_x = (target_size[0] - img_copy.width) // 2
    paste_y = (target_size[1] - img_copy.height) // 2
    new_img.paste(img_copy, (paste_x, paste_y))
    return new_img


def verify_ocular_framing_or_detect_face(
    img: Image.Image,
    view_type: str = "unspecified"
) -> Dict[str, Any]:
    """
    Validates anatomical view compatibility and checks for invalid full-face inputs
    where automated face detection is supported.
    """
    compatible_views = {'palpebral', 'forniceal', 'forniceal_palpebral', 'raw_eye', 'unspecified'}
    clean_view = (view_type or "unspecified").strip().lower()

    # 1. Anatomical view check
    if clean_view not in compatible_views:
        is_face_view = clean_view in {'face', 'full_face', 'portrait', 'selfie'}
        return {
            "supported": True,
            "is_valid": False,
            "is_full_face": is_face_view,
            "reason": (
                f"Unsupported anatomical view '{view_type}'. "
                f"Compatible views are: {sorted(list(compatible_views))}. "
                "A full-face portrait cannot be analyzed for microvascular conjunctival pallor."
                if is_face_view else
                f"Unsupported anatomical view '{view_type}'. Compatible views are: {sorted(list(compatible_views))}."
            )
        }

    # 2. Automated detector check if OpenCV/cascade available
    try:
        import cv2  # type: ignore
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if not face_cascade.empty():
            gray = np.array(img.convert('L'))
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))
            img_w, img_h = img.size
            # A full-face portrait occupies a substantial portion of the frame
            significant_faces = [
                (x, y, w, h) for (x, y, w, h) in faces
                if (w / img_w >= 0.25 or h / img_h >= 0.25 or (w * h) / (img_w * img_h) >= 0.06)
            ]
            if len(significant_faces) > 0:
                return {
                    "supported": True,
                    "is_valid": False,
                    "is_full_face": True,
                    "reason": "Full face detected. Macro eye framing required (10–15 cm close-up of ocular conjunctiva)."
                }
            return {
                "supported": True,
                "is_valid": True,
                "is_full_face": False,
                "reason": "No full face detected in frame."
            }
    except Exception:
        pass

    # Automated face detection unavailable in this environment
    return {
        "supported": False,
        "is_valid": True,
        "is_full_face": False,
        "reason": "Automated face detection not supported in environment; manual macro eye alignment required."
    }

