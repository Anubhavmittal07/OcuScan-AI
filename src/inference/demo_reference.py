"""
src/inference/demo_reference.py
--------------------------------
Demo Reference Mode handler for EyeHealthAI.

Enables an explicit, auditable DEMO REFERENCE MODE for pre-vetted presentation controls.
Strictly preserves prediction integrity:
1. When an uploaded image matches a verified demo hash in demo_reference_manifest.json,
   a prominent, unmistakable banner is attached:
   "DEMO REFERENCE RESULT — PREDEFINED LABEL — NOT AN AI PREDICTION".
2. Real model outputs, logits, and gates are NOT overwritten or fabricated.
3. Both the predefined presentation reference and the genuine neural network inference
   are reported transparently side-by-side.
"""

import os
import json
import hashlib
import logging
from typing import Dict, Any, List, Optional, Union
from PIL import Image

logger = logging.getLogger(__name__)

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST_PATH = os.path.join(WORKSPACE_ROOT, "test_images", "demo", "demo_reference_manifest.json")

_CACHED_MANIFEST: Optional[Dict[str, Any]] = None


def get_demo_manifest() -> Dict[str, Any]:
    """Loads and caches the demo reference manifest."""
    global _CACHED_MANIFEST
    if _CACHED_MANIFEST is not None:
        return _CACHED_MANIFEST

    if not os.path.exists(MANIFEST_PATH):
        logger.warning(f"Demo reference manifest not found at: {MANIFEST_PATH}")
        return {"references": {}, "banner_text": "DEMO REFERENCE RESULT — PREDEFINED LABEL — NOT AN AI PREDICTION"}

    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            _CACHED_MANIFEST = json.load(f)
            return _CACHED_MANIFEST
    except Exception as e:
        logger.error(f"Failed to load demo reference manifest: {e}")
        return {"references": {}, "banner_text": "DEMO REFERENCE RESULT — PREDEFINED LABEL — NOT AN AI PREDICTION"}


def reload_demo_manifest() -> Dict[str, Any]:
    """Force reloads the demo reference manifest."""
    global _CACHED_MANIFEST
    _CACHED_MANIFEST = None
    return get_demo_manifest()


def compute_sha256(item: Union[str, bytes, Image.Image]) -> Optional[str]:
    """Computes SHA-256 for a file path, raw bytes, or PIL Image with path or attributes."""
    if isinstance(item, bytes):
        return hashlib.sha256(item).hexdigest()
    if isinstance(item, str):
        if os.path.isfile(item):
            with open(item, "rb") as fp:
                return hashlib.sha256(fp.read()).hexdigest()
        demo_candidate = os.path.join(WORKSPACE_ROOT, "test_images", "demo", os.path.basename(item))
        if os.path.isfile(demo_candidate):
            with open(demo_candidate, "rb") as fp:
                return hashlib.sha256(fp.read()).hexdigest()
        return None
    if isinstance(item, Image.Image):
        h = getattr(item, "sha256", None)
        if h:
            return str(h).lower().strip()
        raw_b = getattr(item, "raw_bytes", None)
        if raw_b and isinstance(raw_b, bytes):
            return hashlib.sha256(raw_b).hexdigest()
        fn = getattr(item, "filename", None)
        if fn:
            if os.path.isfile(fn):
                with open(fn, "rb") as fp:
                    return hashlib.sha256(fp.read()).hexdigest()
            demo_candidate = os.path.join(WORKSPACE_ROOT, "test_images", "demo", os.path.basename(fn))
            if os.path.isfile(demo_candidate):
                with open(demo_candidate, "rb") as fp:
                    return hashlib.sha256(fp.read()).hexdigest()
    return None


def match_demo_reference(
    image_hashes: Optional[List[str]] = None,
    images: Optional[List[Union[str, bytes, Image.Image]]] = None
) -> Dict[str, Any]:
    """
    Checks if any provided SHA-256 hash or image matches a verified demo case.
    Returns a standardized dictionary indicating demo mode status and reference metadata.
    """
    manifest = get_demo_manifest()
    references = manifest.get("references", {})
    banner_text = manifest.get("banner_text", "DEMO REFERENCE RESULT — PREDEFINED LABEL — NOT AN AI PREDICTION")

    candidate_hashes: List[str] = []
    if image_hashes:
        candidate_hashes.extend([h.lower().strip() for h in image_hashes if isinstance(h, str)])

    if images:
        for img in images:
            h = compute_sha256(img)
            if h:
                candidate_hashes.append(h.lower().strip())

    for h in candidate_hashes:
        if h in references:
            ref = references[h]
            return {
                "is_demo_reference": True,
                "banner_text": banner_text,
                "sha256": h,
                "filename": ref.get("filename", "unknown"),
                "intended_category": ref.get("intended_category", "Demo Reference Category"),
                "target_module": ref.get("target_module", "unified"),
                "reference_finding": ref.get("reference_finding", "Verified Clinical Presentation Control"),
                "anatomical_suitability": ref.get("anatomical_suitability", "Standard clinical documentation"),
                "ground_truth_status": ref.get("ground_truth_status", "Visual presentation reference control. Independent of AI inference."),
                "presentation_notes": ref.get("presentation_notes", "")
            }

    return {
        "is_demo_reference": False,
        "banner_text": None,
        "sha256": None,
        "filename": None,
        "intended_category": None,
        "target_module": None,
        "reference_finding": None,
        "anatomical_suitability": None,
        "ground_truth_status": None,
        "presentation_notes": None
    }
