with open("static/js/dashboard.js", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
matches = [f"{i+1}: {l.strip()}" for i, l in enumerate(lines) if any(k in l.lower() for k in ["getusermedia", "cameramodal", "btnstartcamera", "btncapturecamera", "closecameramodal"])]
print(f"Total camera matches: {len(matches)}")
for m in matches[:25]:
    print(m)
