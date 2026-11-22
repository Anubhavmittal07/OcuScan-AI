import os

with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = """[data-theme="dark"] .header-user-name {
  color: #f8fafc !important;
}"""

replacement = """[data-theme="dark"] .header-user-name {
  color: #f8fafc !important;
}

/* Header Profile Dropdown Card */
.profile-dropdown-menu {
  position: absolute !important;
  top: 48px !important;
  right: 0 !important;
  width: 260px !important;
  background: var(--bg-card, #ffffff) !important;
  border: 1px solid var(--border-subtle, #e2e8f0) !important;
  border-radius: 12px !important;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.16) !important;
  padding: 14px 16px !important;
  z-index: 10005 !important;
  display: flex !important;
  flex-direction: column !important;
  animation: fadeIn 0.15s ease-out !important;
}

[data-theme="dark"] .profile-dropdown-menu {
  background: #1e293b !important;
  border-color: #334155 !important;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45) !important;
}"""

assert target in css, "target not found in style.css!"
css = css.replace(target, replacement, 1)

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Successfully added profile dropdown CSS to style.css!")
