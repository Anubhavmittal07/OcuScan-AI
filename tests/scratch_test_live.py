import requests
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

imgs = [f for f in glob.glob("C:/Users/sarth/.gemini/antigravity/brain/70fdcf38-6d56-4d81-939c-67094dd39db0/.user_uploaded/*.*") if f.endswith(('.jpg', '.jpeg', '.png'))]
test_img = imgs[0] if imgs else "data/processed/anemia/IND_001_20200118_164733.jpg"
print("Testing analyze with:", os.path.basename(test_img))

with open(test_img, "rb") as f:
    r = requests.post(
        "http://127.0.0.1:8000/api/analyze",
        data={"module": "unified", "capture_source": "upload", "age_years": "25", "clinical_sex": "male"},
        files=[("images", (os.path.basename(test_img), f, "image/jpeg"))]
    )

print("Analyze status:", r.status_code)
if r.status_code == 200:
    res = r.json()
    sid = res.get("session_id")
    print("Session ID:", sid)
    print("Overall Status:", res.get("status"))
    mr = res.get("model_results", {})
    for k in sorted(mr.keys()):
        v = mr[k]
        print(f"  {k}: status={v.get('status')}, pred={str(v.get('prediction'))[:30]}, val={v.get('value')}")

    # Dual PDF downloads
    p1 = requests.get(f"http://127.0.0.1:8000/api/download-pdf/{sid}?report_type=screening")
    p2 = requests.get(f"http://127.0.0.1:8000/api/download-pdf/{sid}?report_type=scorecard")
    print("Screening PDF status:", p1.status_code, "length:", len(p1.content))
    print("Scorecard PDF status:", p2.status_code, "length:", len(p2.content))
else:
    print("Failed:", r.text)
