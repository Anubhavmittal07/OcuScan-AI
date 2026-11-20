import sys
import os
import re
import requests

FILE_ID = "1bxO0PZcE4B_k58Vce5N7-xOTVr5q6x8p"
DEST_ZIP = os.path.abspath("data/raw/catscreen/Data2025-main.zip")

print(f"Target destination: {DEST_ZIP}")
session = requests.Session()
URL = "https://drive.google.com/uc?export=download"

print("Contacting Google Drive...")
response = session.get(URL, params={'id': FILE_ID}, stream=True, timeout=30)

confirm_token = None
uuid_val = None

for key, value in response.cookies.items():
    if key.startswith('download_warning'):
        confirm_token = value

html = response.text
confirm_match = re.search(r'name=["\']confirm["\']\s+value=["\']([^"\']+)["\']', html)
if confirm_match:
    confirm_token = confirm_match.group(1)

uuid_match = re.search(r'name=["\']uuid["\']\s+value=["\']([^"\']+)["\']', html)
if uuid_match:
    uuid_val = uuid_match.group(1)

action_match = re.search(r'action=["\']([^"\']+)["\']', html)
download_url = action_match.group(1) if action_match else "https://drive.usercontent.google.com/download"

params = {'id': FILE_ID, 'export': 'download'}
if confirm_token:
    params['confirm'] = confirm_token
if uuid_val:
    params['uuid'] = uuid_val

print(f"Confirm token: {confirm_token}, UUID: {uuid_val}, URL: {download_url}")
print("Starting download stream...")

res2 = session.get(download_url, params=params, stream=True, timeout=60)
print(f"HTTP Status: {res2.status_code}, Content-Type: {res2.headers.get('Content-Type')}")

total_size = int(res2.headers.get('content-length', 0))
print(f"Expected Size: {total_size / (1024*1024):.2f} MB")

downloaded = 0
last_print = 0
with open(DEST_ZIP, "wb") as f:
    for chunk in res2.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)
            downloaded += len(chunk)
            mb = downloaded / (1024 * 1024)
            if mb - last_print >= 50:
                print(f"Downloaded: {mb:.1f} MB ...")
                last_print = mb

print(f"Download complete: {downloaded / (1024*1024):.2f} MB written to {DEST_ZIP}")
