import os

with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update resetSession to hide username from header
old_reset_top = """  function resetSession() {
    invalidatePreviousResults();"""

new_reset_top = """  function resetSession() {
    // Hide username from header on New Screening (stored profile data is safely preserved)
    if (userNameBadge) {
      userNameBadge.style.display = 'none';
      userNameBadge.textContent = '';
    }
    const pDrop = document.getElementById('profileDropdown');
    if (pDrop) pDrop.style.display = 'none';

    invalidatePreviousResults();"""

assert old_reset_top in js, "old_reset_top not found in dashboard.js!"
js = js.replace(old_reset_top, new_reset_top, 1)

# 2. Update initial page load (hard refresh): hide username from header
old_init_user = """  if (userNameBadge && currentUserProfile) userNameBadge.textContent = currentUserProfile.full_name;
  if (userBadge) userBadge.style.display = 'inline-flex';"""

new_init_user = """  // On initial load / hard refresh, hide username from header as requested (profile data safely preserved)
  if (userNameBadge) {
    userNameBadge.style.display = 'none';
    userNameBadge.textContent = '';
  }
  if (userBadge) userBadge.style.display = 'inline-flex';"""

assert old_init_user in js, "old_init_user not found in dashboard.js!"
js = js.replace(old_init_user, new_init_user, 1)

# 3. Replace navUserAvatar click handler with profile dropdown toggle (NEVER open modalUpdateAge)
old_nav_avatar = """  if (navUserAvatar) {
    navUserAvatar.addEventListener('click', () => {
      const modalUpdate = document.getElementById('modalUpdateAge');
      if (modalUpdate) modalUpdate.style.display = 'flex';
    });
  }"""

new_nav_avatar = """  // Profile Dropdown Handler: Opens actual profile dropdown/view, NEVER intrusive Age screening modal
  const profileDropdown = document.getElementById('profileDropdown');
  const btnDropdownEditProfile = document.getElementById('btnDropdownEditProfile');
  const btnDropdownClose = document.getElementById('btnDropdownClose');

  function updateProfileDropdownContent() {
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
  }

  if (userBadge) {
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
      goToStep(1);
    });
  }

  document.addEventListener('click', (e) => {
    if (profileDropdown && profileDropdown.style.display === 'flex') {
      if (!profileDropdown.contains(e.target) && !userBadge.contains(e.target)) {
        profileDropdown.style.display = 'none';
      }
    }
  });"""

assert old_nav_avatar in js, "old_nav_avatar not found in dashboard.js!"
js = js.replace(old_nav_avatar, new_nav_avatar, 1)

# 4. Update Cataract modal values in openModelDetailsModal
old_cat_modal = """    } else if (modelId === 'model_d_cataract') {
      detailsHtml += `
        <div>
          <div class="rel-modal-sec-title">👁️ Nuclear Cataract &amp; LOCS III Staging</div>
          <p>Evaluates lens opacification and nuclear cataract from anterior segment images (Cruz-Vega &amp; Ignatowicz cohorts).</p>
          <table class="rel-table" style="margin-top: 8px;">
            <thead><tr><th>Metric</th><th>Held-out Test Performance</th></tr></thead>
            <tbody>
              <tr><td>Classification Accuracy</td><td><strong>91.1%</strong> (683 / 750 Images Correct)</td></tr>
              <tr><td>Precision</td><td><strong>91.3%</strong></td></tr>
              <tr><td>Recall / Sensitivity</td><td><strong>91.1%</strong></td></tr>
              <tr><td>Specificity</td><td><strong>91.1%</strong></td></tr>
              <tr><td>F1-Score</td><td><strong>91.2%</strong></td></tr>
              <tr><td>ROC-AUC</td><td><strong>0.954</strong></td></tr>
              <tr><td>Held-out Test Images</td><td><strong>750 Images</strong></td></tr>
            </tbody>
          </table>"""

new_cat_modal = """    } else if (modelId === 'model_d_cataract') {
      detailsHtml += `
        <div>
          <div class="rel-modal-sec-title">👁️ Nuclear Cataract &amp; LOCS III Staging</div>
          <p>Evaluates lens opacification and nuclear cataract from anterior segment images (Cruz-Vega &amp; Ignatowicz cohorts).</p>
          <table class="rel-table" style="margin-top: 8px;">
            <thead><tr><th>Metric</th><th>Held-out Test Performance</th></tr></thead>
            <tbody>
              <tr><td>Classification Accuracy</td><td><strong>89.8%</strong> (673 / 750 Images Correct)</td></tr>
              <tr><td>Precision</td><td><strong>91.3%</strong></td></tr>
              <tr><td>Recall / Sensitivity</td><td><strong>87.5%</strong></td></tr>
              <tr><td>Specificity</td><td><strong>93.1%</strong></td></tr>
              <tr><td>F1-Score</td><td><strong>90.2%</strong></td></tr>
              <tr><td>ROC-AUC</td><td><strong>0.948</strong></td></tr>
              <tr><td>Held-out Test Images</td><td><strong>750 Images</strong></td></tr>
            </tbody>
          </table>"""

assert old_cat_modal in js, "old_cat_modal not found in dashboard.js!"
js = js.replace(old_cat_modal, new_cat_modal, 1)

with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Successfully updated static/js/dashboard.js!")
