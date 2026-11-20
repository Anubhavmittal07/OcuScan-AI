with open("static/report.html", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
matches = [f"{i+1}: {l.strip()}" for i, l in enumerate(lines) if "<button" in l or "download" in l.lower() or "print" in l.lower() or "pdf" in l.lower()]
print(f"Total report buttons/action matches: {len(matches)}")
for m in matches[:30]:
    print(m)
