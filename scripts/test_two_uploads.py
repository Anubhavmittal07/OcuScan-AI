import time
import requests

def test_upload(img_path):
    url = "http://127.0.0.1:8000/api/analyze"
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    print(f"\n--- Testing {img_path} ({len(img_bytes)} bytes) ---")
    t0 = time.time()
    files = {"images": (img_path.split("/")[-1].split("\\")[-1], img_bytes, "image/jpeg")}
    data = {
        "module": "unified",
        "capture_source": "upload",
        "language": "en"
    }
    resp = requests.post(url, files=files, data=data)
    t1 = time.time()
    print(f"Status: {resp.status_code}, Elapsed: {t1 - t0:.3f} s")
    if resp.status_code == 200:
        res = resp.json()
        print("Selected module:", res.get("selected_module"))
        print("Demo reference:", res.get("demo_reference"))

if __name__ == "__main__":
    test_upload("test_images/demo/normal.jpeg")
    test_upload("test_images/manual/25.jpg")
