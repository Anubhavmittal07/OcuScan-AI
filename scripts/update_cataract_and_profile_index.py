import os

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Cataract card metrics
old_cat_metrics = """            <div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valCataractAcc">91.1%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valCataractPrec">91.3%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valCataractRec">91.1%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valCataractSpec">91.1%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valCataractF1">91.2%</span></div>"""

new_cat_metrics = """            <div class="rel-metric-row"><span class="rel-metric-label">Accuracy</span><span class="rel-metric-value" id="valCataractAcc">89.8%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Precision</span><span class="rel-metric-value" id="valCataractPrec">91.3%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Recall (Sensitivity)</span><span class="rel-metric-value" id="valCataractRec">87.5%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">Specificity</span><span class="rel-metric-value" id="valCataractSpec">93.1%</span></div>
            <div class="rel-metric-row"><span class="rel-metric-label">F1-Score</span><span class="rel-metric-value" id="valCataractF1">90.2%</span></div>"""

old_cat_cm = """                  <div class="cm-grid-cells">
                    <div class="cm-cell cell-deep">337</div>
                    <div class="cm-cell cell-light">33</div>
                    <div class="cm-cell cell-light">34</div>
                    <div class="cm-cell cell-deep">346</div>
                  </div>"""

new_cat_cm = """                  <div class="cm-grid-cells">
                    <div class="cm-cell cell-deep">345</div>
                    <div class="cm-cell cell-light">26</div>
                    <div class="cm-cell cell-light">47</div>
                    <div class="cm-cell cell-deep">332</div>
                  </div>"""

assert old_cat_metrics in html, "old_cat_metrics not found in index.html!"
assert old_cat_cm in html, "old_cat_cm not found in index.html!"

html = html.replace(old_cat_metrics, new_cat_metrics, 1)
html = html.replace(old_cat_cm, new_cat_cm, 1)

# 2. Update Header Profile Element & Dropdown
old_header_profile = """        <!-- 7. User Profile Avatar & Name -->
        <div id="userBadge" class="header-user-profile" role="button" tabindex="0" title="User Profile">
          <div class="header-user-avatar" id="navUserAvatar">
            <svg viewBox="0 0 24 24" fill="#ffffff" width="16" height="16">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <span id="userNameBadge" class="header-user-name">Sarthak Sharma</span>
        </div>"""

new_header_profile = """        <!-- 7. User Profile Avatar & Dropdown -->
        <div style="position: relative;">
          <div id="userBadge" class="header-user-profile" role="button" tabindex="0" title="User Profile">
            <div class="header-user-avatar" id="navUserAvatar">
              <svg viewBox="0 0 24 24" fill="#ffffff" width="16" height="16">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
            </div>
            <span id="userNameBadge" class="header-user-name" style="display: none;"></span>
          </div>

          <!-- Profile Dropdown Menu (Opened on avatar click, NOT age modal) -->
          <div id="profileDropdown" class="profile-dropdown-menu" style="display: none;">
            <div style="display: flex; align-items: center; gap: 10px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 10px;">
              <div style="width: 36px; height: 36px; border-radius: 50%; background: #0284c7; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700; font-size: 14px;" id="dropdownAvatarLetter">S</div>
              <div style="overflow: hidden;">
                <div id="dropdownUserName" style="font-size: 13.5px; font-weight: 700; color: var(--text-primary); white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">Sarthak Sharma</div>
                <div id="dropdownUserRole" style="font-size: 11px; color: var(--text-muted);">Verified Participant</div>
              </div>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.6; padding-top: 6px;">
              <div><strong>Age:</strong> <span id="dropdownUserAge">28</span> yrs</div>
              <div><strong>Gender:</strong> <span id="dropdownUserGender">Male</span></div>
              <div style="font-size: 11px; color: var(--text-muted); margin-top: 3px;">ID: <span id="dropdownUserId">usr_sarthak_default</span></div>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 10px;">
              <button id="btnDropdownEditProfile" class="btn-secondary" style="flex: 1; padding: 6px 8px; font-size: 11.5px; border-radius: 6px;" type="button">Edit Profile</button>
              <button id="btnDropdownClose" class="btn-secondary" style="padding: 6px 10px; font-size: 11.5px; border-radius: 6px;" type="button">Close</button>
            </div>
          </div>
        </div>"""

assert old_header_profile in html, "old_header_profile not found in index.html!"
html = html.replace(old_header_profile, new_header_profile, 1)

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated static/index.html!")
