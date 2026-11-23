# Quick API Usage Snippets

### Check Operational Health
```bash
curl -X GET http://127.0.0.1:8000/api/health
```

### Analyze Eye Photograph via Python
```python
import requests

url = "http://127.0.0.1:8000/api/analyze"
files = {"image": open("test_eye.jpg", "rb")}
data = {"age": 34, "sex": "male", "notes": "Routine community health check"}

response = requests.post(url, files=files, data=data)
print(response.json())
```
