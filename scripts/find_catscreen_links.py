import urllib.request
import re

url = 'https://www.iab-rubric.org/resources/healthcare-datasets/catscreen'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')

    matches = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.I | re.S)
    print(f"Total links found: {len(matches)}")
    for href, text in matches:
        clean_text = re.sub('<[^<]+?>', '', text).strip()
        if any(k in href.lower() or k in clean_text.lower() for k in ['sample', 'snapshot', 'catscreen', 'drive', 'download', 'license', 'github', 'dropbox', 'pdf', 'zip']):
            print(f"LINK: {clean_text} -> {href}")
except Exception as e:
    print("Error:", e)
