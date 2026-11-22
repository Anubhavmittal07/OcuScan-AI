with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "function updateProfileDropdownContent() {",
    "function updateProfileDropdownContent() {\n    console.log('[DEBUG updateProfileDropdownContent] currentUserProfile=', JSON.stringify(currentUserProfile));"
)

with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added console log to updateProfileDropdownContent")
