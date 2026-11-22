with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace updateProfileDropdownContent to not rely on hoisted/TDZ variables
old_fn = """  function updateProfileDropdownContent() {
    console.log('[DEBUG updateProfileDropdownContent] currentUserProfile=', JSON.stringify(currentUserProfile));
    if (!profileDropdown) return;
    const hasProfile = Boolean(currentUserProfile && currentUserProfile.full_name);

    const elName = document.getElementById('dropdownUserName');
    const elRole = document.getElementById('dropdownUserRole');
    const elAge = document.getElementById('dropdownUserAge');
    const elGender = document.getElementById('dropdownUserGender');
    const elId = document.getElementById('dropdownUserId');
    const elLetter = document.getElementById('dropdownAvatarLetter');

    if (!hasProfile) {
      if (elName) elName.textContent = 'NA';
      if (elRole) elRole.textContent = 'NA';
      if (elAge) elAge.textContent = 'NA';
      if (elGender) elGender.textContent = 'NA';
      if (elId) elId.textContent = 'NA';
      if (elLetter) elLetter.textContent = 'NA';
      return;
    }

    const name = currentUserProfile.full_name;
    const age = (currentUserProfile.age_years !== undefined && currentUserProfile.age_years !== null) ? `${currentUserProfile.age_years} yrs` : 'NA';
    const rawSex = currentUserProfile.gender || currentUserProfile.clinical_sex || '';
    const gender = rawSex ? (rawSex.charAt(0).toUpperCase() + rawSex.slice(1)) : 'NA';
    const id = currentUserProfile.id || 'NA';

    if (elName) elName.textContent = name;
    if (elRole) elRole.textContent = 'Verified Participant';
    if (elAge) elAge.textContent = age;
    if (elGender) elGender.textContent = gender;
    if (elId) elId.textContent = id;
    if (elLetter) elLetter.textContent = name.charAt(0).toUpperCase() || 'U';
  }"""

new_fn = """  function updateProfileDropdownContent() {
    const pDrop = document.getElementById('profileDropdown');
    if (!pDrop) return;
    const hasProfile = Boolean(currentUserProfile && currentUserProfile.full_name);

    const elName = document.getElementById('dropdownUserName');
    const elRole = document.getElementById('dropdownUserRole');
    const elAge = document.getElementById('dropdownUserAge');
    const elGender = document.getElementById('dropdownUserGender');
    const elId = document.getElementById('dropdownUserId');
    const elLetter = document.getElementById('dropdownAvatarLetter');

    if (!hasProfile) {
      if (elName) elName.textContent = 'NA';
      if (elRole) elRole.textContent = 'NA';
      if (elAge) elAge.textContent = 'NA';
      if (elGender) elGender.textContent = 'NA';
      if (elId) elId.textContent = 'NA';
      if (elLetter) elLetter.textContent = 'NA';
      return;
    }

    const name = currentUserProfile.full_name;
    const age = (currentUserProfile.age_years !== undefined && currentUserProfile.age_years !== null) ? `${currentUserProfile.age_years} yrs` : 'NA';
    const rawSex = currentUserProfile.gender || currentUserProfile.clinical_sex || '';
    const gender = rawSex ? (rawSex.charAt(0).toUpperCase() + rawSex.slice(1)) : 'NA';
    const id = currentUserProfile.id || 'NA';

    if (elName) elName.textContent = name;
    if (elRole) elRole.textContent = 'Verified Participant';
    if (elAge) elAge.textContent = age;
    if (elGender) elGender.textContent = gender;
    if (elId) elId.textContent = id;
    if (elLetter) elLetter.textContent = name.charAt(0).toUpperCase() || 'U';
  }"""

if old_fn in text:
    text = text.replace(old_fn, new_fn)
    print("Replaced old_fn with safe getElementById version")
else:
    t_norm = text.replace('\r\n', '\n')
    o_norm = old_fn.replace('\r\n', '\n')
    n_norm = new_fn.replace('\r\n', '\n')
    if o_norm in t_norm:
        text = t_norm.replace(o_norm, n_norm)
        print("Replaced (CRLF normalized)")
    else:
        print("ERROR: old_fn not found")

with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(text)
