import os
import sys
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\sarth\.gemini\antigravity\brain\70fdcf38-6d56-4d81-939c-67094dd39db0"

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print("Navigating to http://127.0.0.1:8000 ...")
        page.goto("http://127.0.0.1:8000")
        page.wait_for_selector("#userBadge", timeout=10000)
        page.wait_for_timeout(1000)

        # 1. VERIFY TOP BAR ON FRESH LOAD
        # Dashboard button should NOT be visible
        btn_dash = page.locator("#btnNavDashboard")
        is_dash_visible = btn_dash.is_visible()
        print(f"1. [Fresh Load] Dashboard button visible: {is_dash_visible}")
        assert not is_dash_visible, "Dashboard button must NOT be visible in the top bar!"

        # Header username badge should show "User"
        name_badge = page.locator("#userNameBadge")
        assert name_badge.is_visible(), "userNameBadge should be visible in header!"
        badge_text = name_badge.text_content().strip()
        print(f"1. [Fresh Load] Header badge text: '{badge_text}'")
        assert badge_text == "User", f"Expected header badge to say 'User', got '{badge_text}'"

        # Capture top bar screenshot on initial load
        top_bar_path = os.path.join(ARTIFACT_DIR, "topbar_initial_user.png")
        page.locator("header.header").screenshot(path=top_bar_path)
        print(f"Saved initial top bar screenshot to {top_bar_path}")

        # 2. VERIFY CLICKING PROFILE OPENS DROPDOWN WITH 'NA' EVERYWHERE
        page.locator("#userBadge").click()
        page.wait_for_timeout(300)

        # Ensure intrusive age modal did not open
        assert not page.locator("#modalUpdateAge").is_visible(), "Modal update age should not open on profile click"

        dropdown = page.locator("#profileDropdown")
        assert dropdown.is_visible(), "Profile dropdown should be visible after clicking profile icon"

        dd_name = page.locator("#dropdownUserName").text_content().strip()
        dd_age = page.locator("#dropdownUserAge").text_content().strip()
        dd_gender = page.locator("#dropdownUserGender").text_content().strip()
        dd_id = page.locator("#dropdownUserId").text_content().strip()
        dd_role = page.locator("#dropdownUserRole").text_content().strip()
        dd_letter = page.locator("#dropdownAvatarLetter").text_content().strip()

        print(f"2. [Profile Dropdown Defaults] Name: '{dd_name}', Age: '{dd_age}', Gender: '{dd_gender}', ID: '{dd_id}', Role: '{dd_role}', Letter: '{dd_letter}'")
        assert dd_name == "NA", f"Expected Name to be 'NA', got '{dd_name}'"
        assert dd_age == "NA", f"Expected Age to be 'NA', got '{dd_age}'"
        assert dd_gender == "NA", f"Expected Gender to be 'NA', got '{dd_gender}'"
        assert dd_id == "NA", f"Expected ID to be 'NA', got '{dd_id}'"
        assert dd_role == "NA", f"Expected Role to be 'NA', got '{dd_role}'"
        assert dd_letter == "NA", f"Expected Letter to be 'NA', got '{dd_letter}'"

        # Capture dropdown with NA
        dd_na_path = os.path.join(ARTIFACT_DIR, "profile_dropdown_na.png")
        dropdown.screenshot(path=dd_na_path)
        print(f"Saved dropdown NA screenshot to {dd_na_path}")

        # Close dropdown
        page.locator("#btnDropdownClose").click()
        page.wait_for_timeout(200)

        # 3. FILL DETAILS IN PROFILE PAGE (STEP 2)
        print("3. Navigating to Step 2 (Profile Registration)...")
        page.evaluate("goToStep(2)")
        page.wait_for_timeout(500)

        # Fill in participant profile form
        page.fill("#inputRegName", "Vikram Seth")
        page.fill("#inputRegEmail", "vikram.seth@example.com")
        page.select_option("#selectRegGender", "male")
        page.fill("#inputRegPhone", "9876543210")
        page.fill("#inputRegAge", "42")
        page.check("#chkConsentResearch")
        page.check("#chkConsentStorage")
        page.wait_for_timeout(300)

        # Click Agree & Continue
        btn_submit = page.locator("#btnSubmitRegistration")
        assert btn_submit.is_enabled(), "Submit button should be enabled after filling form"
        btn_submit.click()
        page.wait_for_timeout(1000)

        # 4. VERIFY HEADER SHOWS ENTERED USERNAME
        header_name_after = page.locator("#userNameBadge").text_content().strip()
        print(f"4. [After Profile Submitted] Header name: '{header_name_after}'")
        assert header_name_after == "Vikram Seth", f"Expected header to show 'Vikram Seth', got '{header_name_after}'"

        # Capture top bar after registration
        top_bar_filled_path = os.path.join(ARTIFACT_DIR, "topbar_with_user_name.png")
        page.locator("header.header").screenshot(path=top_bar_filled_path)
        print(f"Saved filled top bar screenshot to {top_bar_filled_path}")

        # 5. VERIFY DROPDOWN NOW SHOWS FILLED USER DETAILS
        page.locator("#userBadge").click()
        page.wait_for_timeout(300)
        assert dropdown.is_visible()

        dd_name_filled = page.locator("#dropdownUserName").text_content().strip()
        dd_age_filled = page.locator("#dropdownUserAge").text_content().strip()
        dd_gender_filled = page.locator("#dropdownUserGender").text_content().strip()
        dd_letter_filled = page.locator("#dropdownAvatarLetter").text_content().strip()

        print(f"5. [Dropdown Filled Details] Name: '{dd_name_filled}', Age: '{dd_age_filled}', Gender: '{dd_gender_filled}', Letter: '{dd_letter_filled}'")
        assert dd_name_filled == "Vikram Seth", f"Expected dropdown name 'Vikram Seth', got '{dd_name_filled}'"
        assert "42" in dd_age_filled, f"Expected 42 in age, got '{dd_age_filled}'"
        assert dd_gender_filled.lower() == "male", f"Expected Male gender, got '{dd_gender_filled}'"
        assert dd_letter_filled == "V", f"Expected avatar letter 'V', got '{dd_letter_filled}'"

        dd_filled_path = os.path.join(ARTIFACT_DIR, "profile_dropdown_filled.png")
        dropdown.screenshot(path=dd_filled_path)
        print(f"Saved filled dropdown screenshot to {dd_filled_path}")

        page.locator("#btnDropdownClose").click()
        page.wait_for_timeout(200)

        # 6. CLICK "NEW SCREENING" -> MUST REVERT TO "User" AND "NA"
        print("6. Clicking 'New Screening'...")
        page.locator("#btnResetSession").click()
        page.wait_for_timeout(500)

        header_reset_text = page.locator("#userNameBadge").text_content().strip()
        print(f"6. [After New Screening] Header badge text: '{header_reset_text}'")
        assert header_reset_text == "User", f"Expected header to revert to 'User', got '{header_reset_text}'"

        # Check dropdown after New Screening
        page.locator("#userBadge").click()
        page.wait_for_timeout(300)
        dd_name_reset = page.locator("#dropdownUserName").text_content().strip()
        dd_age_reset = page.locator("#dropdownUserAge").text_content().strip()
        print(f"6. [Dropdown After New Screening] Name: '{dd_name_reset}', Age: '{dd_age_reset}'")
        assert dd_name_reset == "NA", f"Expected Name to reset to 'NA', got '{dd_name_reset}'"
        assert dd_age_reset == "NA", f"Expected Age to reset to 'NA', got '{dd_age_reset}'"

        page.locator("#btnDropdownClose").click()
        page.wait_for_timeout(200)

        # 7. HARD REFRESH -> MUST STILL BE "User" AND "NA"
        print("7. Performing page reload (Hard Refresh)...")
        page.reload()
        page.wait_for_timeout(1000)

        hr_dash_visible = page.locator("#btnNavDashboard").is_visible()
        hr_header_text = page.locator("#userNameBadge").text_content().strip()
        print(f"7. [After Hard Refresh] Dashboard visible: {hr_dash_visible}, Header badge: '{hr_header_text}'")
        assert not hr_dash_visible, "Dashboard button must NOT be visible after hard refresh!"
        assert hr_header_text == "User", f"Expected 'User' after hard refresh, got '{hr_header_text}'"

        page.locator("#userBadge").click()
        page.wait_for_timeout(300)
        hr_dd_name = page.locator("#dropdownUserName").text_content().strip()
        hr_dd_age = page.locator("#dropdownUserAge").text_content().strip()
        print(f"7. [Dropdown After Hard Refresh] Name: '{hr_dd_name}', Age: '{hr_dd_age}'")
        assert hr_dd_name == "NA", f"Expected Name 'NA' after hard refresh, got '{hr_dd_name}'"
        assert hr_dd_age == "NA", f"Expected Age 'NA' after hard refresh, got '{hr_dd_age}'"

        hr_path = os.path.join(ARTIFACT_DIR, "after_hard_refresh_verified.png")
        page.screenshot(path=hr_path)
        print(f"Saved full page screenshot to {hr_path}")

        browser.close()
        print("\n>>> ALL CHECKS PASSED PERFECTLY 100% END-TO-END! <<<")

if __name__ == "__main__":
    run_verification()
