with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for tid in ['dropdownUserName', 'dropdownUserAge', 'dropdownUserGender', 'dropdownUserId', 'dropdownAvatarLetter', 'profileDropdown', 'userBadge', 'userNameBadge']:
    count = text.count(f'id="{tid}"')
    print(f"{tid}: {count}")
