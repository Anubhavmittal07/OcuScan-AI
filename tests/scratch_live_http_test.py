import requests

test_files = [
    ("17_jpg.rf.612b22b7e707fc3dbe5e13b6cca5dadf.jpg", "test_images/manual/17_jpg.rf.612b22b7e707fc3dbe5e13b6cca5dadf.jpg"),
    ("20200118_164733.jpg", "test_images/manual/20200118_164733.jpg"),
    ("2.png", "test_images/manual/2.png"),
    ("25.jpg", "test_images/manual/25.jpg")
]

for fname, fpath in test_files:
    with open(fpath, "rb") as f:
        r = requests.post(
            "http://127.0.0.1:8000/api/analyze",
            data={"module": "unified", "capture_source": "upload", "age_years": "25", "clinical_sex": "male"},
            files=[("images", (fname, f, "image/jpeg" if fname.endswith(".jpg") else "image/png"))]
        )
    print(f"\n{fname}: HTTP {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        sid = data["session_id"]
        mr = data.get("model_results", {})
        stye_obj = mr.get("stye", {})
        cat_obj = mr.get("cataract", {})
        stye_pred = stye_obj.get("prediction", [{}])
        cat_pred = cat_obj.get("prediction", [{}])
        stye_finding = (stye_pred[0].get("clinical_decision") or {}).get("finding_en") if isinstance(stye_pred, list) and stye_pred else "N/A"
        cat_finding = (cat_pred[0].get("clinical_decision") or {}).get("finding_en") if isinstance(cat_pred, list) and cat_pred else "N/A"
        print(f"   Session ID : {sid}")
        print(f"   Stye       : {stye_finding} [Status: {stye_obj.get('status')}]")
        print(f"   Cataract   : {cat_finding} [Status: {cat_obj.get('status')}]")
        
        # Test PDF downloads
        p1 = requests.get(f"http://127.0.0.1:8000/api/reports/{sid}/screening-pdf")
        p2 = requests.get(f"http://127.0.0.1:8000/api/reports/{sid}/scorecard-pdf")
        print(f"   Screening PDF: HTTP {p1.status_code} ({len(p1.content)} bytes)")
        print(f"   Scorecard PDF: HTTP {p2.status_code} ({len(p2.content)} bytes)")
