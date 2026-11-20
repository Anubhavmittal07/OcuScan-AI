import time
import requests

def profile_api():
    url = "http://127.0.0.1:8000/api/analyze"
    img_path = r"test_images\demo\normal.jpeg"

    with open(img_path, "rb") as f:
        img_bytes = f.read()

    print(f"Profiling /api/analyze with {img_path} ({len(img_bytes)} bytes)...")
    
    t0 = time.time()
    files = {"images": ("normal.jpeg", img_bytes, "image/jpeg")}
    data = {
        "module": "unified",
        "capture_source": "upload",
        "language": "en"
    }

    resp = requests.post(url, files=files, data=data)
    t1 = time.time()

    print(f"Status: {resp.status_code}")
    print(f"Total time elapsed: {t1 - t0:.3f} seconds")

    if resp.status_code == 200:
        res_json = resp.json()
        print("Session ID:", res_json.get("session_id"))
        print("Selected module:", res_json.get("selected_module"))
        print("Audit keys:", list(res_json.get("module_execution_audit", {}).keys()))

if __name__ == '__main__':
    profile_api()
