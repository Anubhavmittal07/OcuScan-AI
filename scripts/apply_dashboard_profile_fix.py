import re

def update_dashboard_js():
    with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update initial load profile logic:
    # On hard refresh / initial load: start fresh with header "User" and dropdown "NA"
    old_init = """  // Profile Persistence & Initial State Setup
  try {
    const savedProfile = localStorage.getItem('ocuscan_user_profile');
    if (savedProfile) {
      currentUserProfile = JSON.parse(savedProfile);
    }
  } catch (e) {
    console.warn('Could not parse cached user profile from localStorage:', e);
  }

  if (!currentUserProfile) {
    currentUserProfile = {
      id: "usr_sarthak_default",
      full_name: "Sarthak Sharma",
      phone: "9876543210",
      email: "sarthak.sharma@example.com",
      age_years: 28,
      gender: "male",
      clinical_sex: "male",
      research_consent: true,
      data_storage_consent: true,
      external_ai_consent: true
    };
    try {
      localStorage.setItem('ocuscan_user_profile', JSON.stringify(currentUserProfile));
    } catch (e) {}
  }
  // On initial load / hard refresh, hide username from header as requested (profile data safely preserved)
  if (userNameBadge) {
    userNameBadge.style.display = 'none';
    userNameBadge.textContent = '';
  }
  if (userBadge) userBadge.style.display = 'inline-flex';
  goToStep(1);"""

    new_init = """  // Profile Initial State Setup
  // On initial load / hard refresh: header displays "User" and dropdown displays "NA" everywhere
  currentUserProfile = null;
  try {
    localStorage.removeItem('ocuscan_user_profile');
  } catch (e) {}

  if (userNameBadge) {
    userNameBadge.textContent = 'User';
    userNameBadge.style.display = 'inline-block';
  }
  if (userBadge) userBadge.style.display = 'inline-flex';
  if (typeof updateProfileDropdownContent === 'function') {
    updateProfileDropdownContent();
  }
  goToStep(1);"""

    if old_init in content:
        content = content.replace(old_init, new_init)
        print("Updated initial load logic in dashboard.js")
    else:
        # Normalize line endings
        c_norm = content.replace('\r\n', '\n')
        o_norm = old_init.replace('\r\n', '\n')
        n_norm = new_init.replace('\r\n', '\n')
        if o_norm in c_norm:
            content = c_norm.replace(o_norm, n_norm)
            print("Updated initial load logic (CRLF normalized)")
        else:
            print("ERROR: old_init not found in dashboard.js")

    # 2. Update resetSession()
    old_reset = """  function resetSession() {
    // Hide username from header on New Screening (stored profile data is safely preserved)
    if (userNameBadge) {
      userNameBadge.style.display = 'none';
      userNameBadge.textContent = '';
    }
    const pDrop = document.getElementById('profileDropdown');
    if (pDrop) pDrop.style.display = 'none';"""

    new_reset = """  function resetSession() {
    // On New Screening: revert header to 'User' and dropdown to 'NA' everywhere
    if (userNameBadge) {
      userNameBadge.textContent = 'User';
      userNameBadge.style.display = 'inline-block';
    }
    currentUserProfile = null;
    try {
      localStorage.removeItem('ocuscan_user_profile');
    } catch (e) {}
    if (typeof updateProfileDropdownContent === 'function') {
      updateProfileDropdownContent();
    }
    if (formRegistration) {
      formRegistration.reset();
    }
    const pDrop = document.getElementById('profileDropdown');
    if (pDrop) pDrop.style.display = 'none';"""

    if old_reset in content:
        content = content.replace(old_reset, new_reset)
        print("Updated resetSession() in dashboard.js")
    else:
        c_norm = content.replace('\r\n', '\n')
        o_norm = old_reset.replace('\r\n', '\n')
        n_norm = new_reset.replace('\r\n', '\n')
        if o_norm in c_norm:
            content = c_norm.replace(o_norm, n_norm)
            print("Updated resetSession() (CRLF normalized)")
        else:
            print("ERROR: old_reset not found in dashboard.js")

    # 3. Update updateProfileDropdownContent and btnDropdownEditProfile
    old_dropdown_fn = """  function updateProfileDropdownContent() {
    if (!profileDropdown) return;
    const name = currentUserProfile?.full_name || 'Participant';
    const age = (currentUserProfile?.age_years !== undefined && currentUserProfile?.age_years !== null) ? currentUserProfile.age_years : 28;
    const gender = currentUserProfile?.clinical_sex ? (currentUserProfile.clinical_sex.charAt(0).toUpperCase() + currentUserProfile.clinical_sex.slice(1)) : 'Male';
    const id = currentUserProfile?.id || 'usr_sarthak_default';

    const elName = document.getElementById('dropdownUserName');
    if (elName) elName.textContent = name;
    const elAge = document.getElementById('dropdownUserAge');
    if (elAge) elAge.textContent = age;
    const elGender = document.getElementById('dropdownUserGender');
    if (elGender) elGender.textContent = gender;
    const elId = document.getElementById('dropdownUserId');
    if (elId) elId.textContent = id;
    const elLetter = document.getElementById('dropdownAvatarLetter');
    if (elLetter) elLetter.textContent = name.charAt(0).toUpperCase() || 'S';
  }"""

    new_dropdown_fn = """  function updateProfileDropdownContent() {
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

    if old_dropdown_fn in content:
        content = content.replace(old_dropdown_fn, new_dropdown_fn)
        print("Updated updateProfileDropdownContent in dashboard.js")
    else:
        c_norm = content.replace('\r\n', '\n')
        o_norm = old_dropdown_fn.replace('\r\n', '\n')
        n_norm = new_dropdown_fn.replace('\r\n', '\n')
        if o_norm in c_norm:
            content = c_norm.replace(o_norm, n_norm)
            print("Updated updateProfileDropdownContent (CRLF normalized)")
        else:
            print("ERROR: old_dropdown_fn not found in dashboard.js")

    # 4. Update btnDropdownEditProfile to go to step 2 directly
    old_edit_click = """  if (btnDropdownEditProfile) {
    btnDropdownEditProfile.addEventListener('click', (e) => {
      e.stopPropagation();
      if (profileDropdown) profileDropdown.style.display = 'none';
      goToStep(1);
    });
  }"""

    new_edit_click = """  if (btnDropdownEditProfile) {
    btnDropdownEditProfile.addEventListener('click', (e) => {
      e.stopPropagation();
      if (profileDropdown) profileDropdown.style.display = 'none';
      goToStep(2);
    });
  }"""

    if old_edit_click in content:
        content = content.replace(old_edit_click, new_edit_click)
        print("Updated btnDropdownEditProfile in dashboard.js")
    else:
        c_norm = content.replace('\r\n', '\n')
        o_norm = old_edit_click.replace('\r\n', '\n')
        n_norm = new_edit_click.replace('\r\n', '\n')
        if o_norm in c_norm:
            content = c_norm.replace(o_norm, n_norm)
            print("Updated btnDropdownEditProfile (CRLF normalized)")
        else:
            print("ERROR: old_edit_click not found in dashboard.js")

    # 5. Ensure registration submission updates header and dropdown
    old_reg_submit = """        if (userBadge && userNameBadge) {
          userNameBadge.textContent = currentUserProfile.full_name;
          userBadge.style.display = 'inline-flex';
        }"""

    new_reg_submit = """        if (userBadge && userNameBadge) {
          userNameBadge.textContent = currentUserProfile.full_name;
          userNameBadge.style.display = 'inline-block';
          userBadge.style.display = 'inline-flex';
        }
        updateProfileDropdownContent();"""

    if old_reg_submit in content:
        content = content.replace(old_reg_submit, new_reg_submit)
        print("Updated registration submit handler in dashboard.js")
    else:
        c_norm = content.replace('\r\n', '\n')
        o_norm = old_reg_submit.replace('\r\n', '\n')
        n_norm = new_reg_submit.replace('\r\n', '\n')
        if o_norm in c_norm:
            content = c_norm.replace(o_norm, n_norm)
            print("Updated registration submit handler (CRLF normalized)")
        else:
            print("ERROR: old_reg_submit not found in dashboard.js")

    with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully written changes to static/js/dashboard.js")

if __name__ == '__main__':
    update_dashboard_js()
