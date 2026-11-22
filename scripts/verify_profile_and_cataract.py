from playwright.sync_api import sync_playwright
import os

artifact_dir = r'C:\Users\sarth\.gemini\antigravity\brain\70fdcf38-6d56-4d81-939c-67094dd39db0'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # 1. Test Hard Refresh / Initial Load
    page.goto('http://127.0.0.1:8000')
    page.wait_for_timeout(1000)
    
    # Check that username in header is hidden on hard refresh
    user_name_visible = page.is_visible('#userNameBadge')
    user_name_text = page.inner_text('#userNameBadge')
    avatar_visible = page.is_visible('#navUserAvatar')
    print(f'[Hard Refresh] userNameBadge visible: {user_name_visible}, text: "{user_name_text}", avatar visible: {avatar_visible}')
    assert not user_name_visible or user_name_text.strip() == "", "Username must be hidden on hard refresh!"
    assert avatar_visible, "Avatar icon must be visible on hard refresh!"
    
    # Take screenshot of header on hard refresh (username hidden, avatar icon visible)
    page.screenshot(path=os.path.join(artifact_dir, 'profile_header_hard_refresh.png'), clip={'x': 800, 'y': 0, 'width': 480, 'height': 85})
    
    # 2. Test Clicking Profile Icon (Must NOT open modalUpdateAge, must open profileDropdown)
    page.click('#userBadge')
    page.wait_for_timeout(500)
    
    age_modal_visible = page.is_visible('#modalUpdateAge')
    dropdown_visible = page.is_visible('#profileDropdown')
    dropdown_name = page.inner_text('#dropdownUserName')
    print(f'[Profile Click] modalUpdateAge visible: {age_modal_visible}, profileDropdown visible: {dropdown_visible}, name: "{dropdown_name}"')
    assert not age_modal_visible, "Clicking profile icon must NOT open modalUpdateAge!"
    assert dropdown_visible, "Clicking profile icon must open profileDropdown!"
    assert "Sarthak" in dropdown_name, "Dropdown must display user profile name!"
    
    # Take screenshot of open profile dropdown
    page.screenshot(path=os.path.join(artifact_dir, 'profile_dropdown_opened.png'), clip={'x': 900, 'y': 0, 'width': 380, 'height': 260})
    
    # 3. Test New Screening Button
    page.click('#btnResetSession')
    page.wait_for_timeout(800)
    
    user_name_after_new = page.is_visible('#userNameBadge')
    user_name_after_text = page.inner_text('#userNameBadge')
    stored_profile = page.evaluate("localStorage.getItem('ocuscan_user_profile')")
    print(f'[New Screening] userNameBadge visible: {user_name_after_new}, text: "{user_name_after_text}", localStorage preserved: {bool(stored_profile)}')
    assert not user_name_after_new or user_name_after_text.strip() == "", "Username must remain hidden after New Screening!"
    assert stored_profile is not None, "Stored profile must NOT be deleted!"
    
    # Take screenshot after New Screening
    page.screenshot(path=os.path.join(artifact_dir, 'header_after_new_screening.png'), clip={'x': 800, 'y': 0, 'width': 480, 'height': 85})
    
    # 4. Test Model Reliability Cataract Values
    page.click('#btnNavReliability')
    page.wait_for_timeout(1500)
    
    cat_acc = page.inner_text('#valCataractAcc')
    cat_prec = page.inner_text('#valCataractPrec')
    cat_rec = page.inner_text('#valCataractRec')
    cat_spec = page.inner_text('#valCataractSpec')
    cat_f1 = page.inner_text('#valCataractF1')
    
    print(f'[Cataract Metrics] Acc: {cat_acc}, Prec: {cat_prec}, Rec: {cat_rec}, Spec: {cat_spec}, F1: {cat_f1}')
    assert cat_acc == '89.8%', f"Expected 89.8%, got {cat_acc}"
    assert cat_prec == '91.3%', f"Expected 91.3%, got {cat_prec}"
    assert cat_rec == '87.5%', f"Expected 87.5%, got {cat_rec}"
    assert cat_spec == '93.1%', f"Expected 93.1%, got {cat_spec}"
    assert cat_f1 == '90.2%', f"Expected 90.2%, got {cat_f1}"
    
    # Take screenshot of Cataract card with exact requested metrics
    page.screenshot(path=os.path.join(artifact_dir, 'cataract_exact_values_verified.png'), clip={'x': 750, 'y': 240, 'width': 260, 'height': 600})
    
    browser.close()

print('ALL PROFILE & CATARACT VERIFICATIONS PASSED!')
