import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
from src.inference.unified_service import get_inference_service

service = get_inference_service()

test_files = [
    ("Image 1 (Stye)", "test_images/manual/17_jpg.rf.612b22b7e707fc3dbe5e13b6cca5dadf.jpg"),
    ("Image 2 (Conjunctiva macro)", "test_images/manual/20200118_164733.jpg"),
    ("Image 3 (Palpebral everted)", "test_images/manual/2.png"),
    ("Image 4 (Conjunctival injection)", "test_images/manual/25.jpg")
]

for label, fpath in test_files:
    im = Image.open(fpath)
    res = service.predict_unified([im], view_types=["unspecified"])
    print(f"\n==================== {label} : {fpath} ====================")
    for k in ["anemia", "slid", "jaundice", "cataract", "stye"]:
        v = res.get(k) or {}
        status = v.get("status")
        conf = v.get("confidence")
        val = v.get("value")
        pred = v.get("prediction")
        # Simplify pred if it's a list
        if isinstance(pred, list) and len(pred) > 0:
            p0 = pred[0]
            if isinstance(p0, dict):
                p_clean = {pk: pv for pk, pv in p0.items() if pk not in ("attribution", "quality", "chromatic")}
            else:
                p_clean = p0
        else:
            p_clean = pred
        print(f"  [{k.upper()}]: status={status} | val={val} | conf={conf} | pred={p_clean}")
