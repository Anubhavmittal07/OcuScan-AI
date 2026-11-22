import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
from src.inference.unified_service import get_inference_service

service = get_inference_service()

test_files = [
    ("17_jpg.rf.612b22b7e707fc3dbe5e13b6cca5dadf.jpg", "test_images/manual/17_jpg.rf.612b22b7e707fc3dbe5e13b6cca5dadf.jpg"),
    ("20200118_164733.jpg", "test_images/manual/20200118_164733.jpg"),
    ("2.png", "test_images/manual/2.png"),
    ("25.jpg", "test_images/manual/25.jpg")
]

print("\n" + "="*120)
print(f"{'Image':<45} | {'Module':<12} | {'Suitable?':<10} | {'Status':<22} | {'Prediction / Finding':<40}")
print("="*120)

for name, fpath in test_files:
    im = Image.open(fpath)
    # preserve filename on image object for view checking
    im.filename = name
    res = service.predict_unified([im], view_types=["unspecified"])
    
    for mod in ["anemia", "slid", "jaundice", "cataract", "stye"]:
        v = res.get(mod) or {}
        status = v.get("status")
        pred = v.get("prediction")
        p0 = pred[0] if isinstance(pred, list) and len(pred) > 0 else (pred or {})
        cd = p0.get("clinical_decision", {}) if isinstance(p0, dict) else {}
        finding = cd.get("finding_en") or p0.get("predicted_class") or str(p0.get("hb_pred_g_dl")) or "N/A"
        
        suitable = "No" if status in ("unsupported_image", "blocked_domain_validation", "unavailable") else "Yes"
        print(f"{name:<45} | {mod:<12} | {suitable:<10} | {status:<22} | {finding:<40}")
    print("-" * 120)
