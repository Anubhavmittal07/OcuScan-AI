import re

def fix_profile_dropdown():
    # 1. Update style.css
    with open('static/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    old_css = """.profile-dropdown-menu {
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
}"""

    new_css = """.profile-dropdown-menu {
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
  display: none !important;
  flex-direction: column !important;
  animation: fadeIn 0.15s ease-out !important;
}

.profile-dropdown-menu.active {
  display: flex !important;
}"""

    if old_css in css:
        css = css.replace(old_css, new_css)
        print("Replaced CSS in style.css directly")
    else:
        c_norm = css.replace('\r\n', '\n')
        o_norm = old_css.replace('\r\n', '\n')
        n_norm = new_css.replace('\r\n', '\n')
        if o_norm in c_norm:
            css = c_norm.replace(o_norm, n_norm)
            print("Replaced CSS in style.css (normalized)")
        else:
            print("ERROR: old_css not found in style.css")

    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)

    # 2. Update dashboard.js with robust openProfileDropdown and closeProfileDropdown
    with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
        js = f.read()

    old_js_section = """  if (userBadge) {
    userBadge.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!profileDropdown) return;
      const isHidden = profileDropdown.style.display === 'none' || !profileDropdown.style.display;
      if (isHidden) {
        updateProfileDropdownContent();
        profileDropdown.style.display = 'flex';
      } else {
        profileDropdown.style.display = 'none';
      }
    });
  }

  if (btnDropdownClose) {
    btnDropdownClose.addEventListener('click', (e) => {
      e.stopPropagation();
      if (profileDropdown) profileDropdown.style.display = 'none';
    });
  }

  if (btnDropdownEditProfile) {
    btnDropdownEditProfile.addEventListener('click', (e) => {
      e.stopPropagation();
      if (profileDropdown) profileDropdown.style.display = 'none';
      goToStep(2);
    });
  }

  document.addEventListener('click', (e) => {
    if (profileDropdown && profileDropdown.style.display === 'flex') {
      if (!profileDropdown.contains(e.target) && !userBadge.contains(e.target)) {
        profileDropdown.style.display = 'none';
      }
    }
  });"""

    new_js_section = """  function closeProfileDropdown() {
    const p = document.getElementById('profileDropdown');
    if (p) {
      p.classList.remove('active');
      p.style.setProperty('display', 'none', 'important');
    }
  }

  function openProfileDropdown() {
    const p = document.getElementById('profileDropdown');
    if (p) {
      updateProfileDropdownContent();
      p.classList.add('active');
      p.style.setProperty('display', 'flex', 'important');
    }
  }

  if (userBadge) {
    userBadge.addEventListener('click', (e) => {
      e.stopPropagation();
      const p = document.getElementById('profileDropdown');
      if (!p) return;
      const isOpen = p.classList.contains('active') || (p.style.display !== 'none' && p.style.display !== '');
      if (isOpen) {
        closeProfileDropdown();
      } else {
        openProfileDropdown();
      }
    });
  }

  if (btnDropdownClose) {
    btnDropdownClose.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeProfileDropdown();
    });
  }

  if (btnDropdownEditProfile) {
    btnDropdownEditProfile.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeProfileDropdown();
      goToStep(2);
    });
  }

  document.addEventListener('click', (e) => {
    const p = document.getElementById('profileDropdown');
    if (p && (p.classList.contains('active') || p.style.display === 'flex')) {
      if (!p.contains(e.target) && !userBadge.contains(e.target)) {
        closeProfileDropdown();
      }
    }
  });"""

    if old_js_section in js:
        js = js.replace(old_js_section, new_js_section)
        print("Replaced JS section in dashboard.js directly")
    else:
        j_norm = js.replace('\r\n', '\n')
        o_norm = old_js_section.replace('\r\n', '\n')
        n_norm = new_js_section.replace('\r\n', '\n')
        if o_norm in j_norm:
            js = j_norm.replace(o_norm, n_norm)
            print("Replaced JS section in dashboard.js (normalized)")
        else:
            print("ERROR: old_js_section not found in dashboard.js")

    # Also update resetSession in dashboard.js to call closeProfileDropdown()
    js = js.replace(
        "const pDrop = document.getElementById('profileDropdown');\n    if (pDrop) pDrop.style.display = 'none';",
        "closeProfileDropdown();"
    )

    with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
        f.write(js)

    # 3. Update index.html inline style
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html = re.sub(
        r'<div id="profileDropdown" class="profile-dropdown-menu"[^>]*>',
        '<div id="profileDropdown" class="profile-dropdown-menu" style="display: none !important;">',
        html
    )

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html profileDropdown inline style")

if __name__ == '__main__':
    fix_profile_dropdown()
