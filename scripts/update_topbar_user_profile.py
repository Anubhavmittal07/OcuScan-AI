import re

def update_index_html():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Hide Dashboard button from top bar
    content = re.sub(
        r'<button id="btnNavDashboard" class="header-nav-link" type="button"[^>]*>Dashboard</button>',
        '<button id="btnNavDashboard" class="header-nav-link" type="button" style="display: none !important;">Dashboard</button>',
        content
    )

    # 2. Update userNameBadge to show "User"
    content = re.sub(
        r'<span id="userNameBadge" class="header-user-name"[^>]*>.*?</span>',
        '<span id="userNameBadge" class="header-user-name">User</span>',
        content
    )

    # 3. Update profileDropdown inner fields to "NA"
    content = re.sub(
        r'<div[^>]*id="dropdownAvatarLetter"[^>]*>.*?</div>',
        '<div style="width: 36px; height: 36px; border-radius: 50%; background: #0284c7; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700; font-size: 14px;" id="dropdownAvatarLetter">NA</div>',
        content
    )
    content = re.sub(
        r'<div id="dropdownUserName"[^>]*>.*?</div>',
        '<div id="dropdownUserName" style="font-size: 13.5px; font-weight: 700; color: var(--text-primary); white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">NA</div>',
        content
    )
    content = re.sub(
        r'<div id="dropdownUserRole"[^>]*>.*?</div>',
        '<div id="dropdownUserRole" style="font-size: 11px; color: var(--text-muted);">NA</div>',
        content
    )
    content = re.sub(
        r'<span id="dropdownUserAge"[^>]*>.*?</span>\s*yrs',
        '<span id="dropdownUserAge">NA</span>',
        content
    )
    content = re.sub(
        r'<span id="dropdownUserGender"[^>]*>.*?</span>',
        '<span id="dropdownUserGender">NA</span>',
        content
    )
    content = re.sub(
        r'<span id="dropdownUserId"[^>]*>.*?</span>',
        '<span id="dropdownUserId">NA</span>',
        content
    )

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated static/index.html")

if __name__ == '__main__':
    update_index_html()
