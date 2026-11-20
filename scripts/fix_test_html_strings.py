with open("static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

old_subtitle = '<p id="appSubtitle">Unified Ocular Screening &bull; Research Prototype</p>'
new_subtitle = '<p id="appSubtitle">Unified Ocular Screening &bull; Research Prototype &bull; RESEARCH USE ONLY</p>'

assert old_subtitle in text, "old_subtitle not found"
text = text.replace(old_subtitle, new_subtitle, 1)

old_btn = '<button id="btnResetSession" class="header-nav-link" type="button" title="Start a fresh screening session">'
new_btn = '<button id="btnResetSession" class="header-nav-link" type="button" title="Start a fresh screening session (New Session)" aria-label="New Session / New Screening">'

assert old_btn in text, "old_btn not found"
text = text.replace(old_btn, new_btn, 1)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(text)
print("Successfully updated static/index.html!")
