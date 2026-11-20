from playwright.sync_api import sync_playwright

def verify_all_close_interactions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000")
        page.wait_for_selector("#userBadge")

        dd = page.locator("#profileDropdown")

        # Test 1: Click #btnDropdownClose button
        print("Test 1: Close button...")
        page.locator("#userBadge").click()
        page.wait_for_timeout(200)
        assert dd.is_visible(), "Dropdown should be visible after clicking avatar"
        page.locator("#btnDropdownClose").click()
        page.wait_for_timeout(200)
        assert not dd.is_visible(), "Dropdown MUST be closed after clicking Close button"
        print("Test 1 Passed: Close button closed dropdown successfully.")

        # Test 2: Toggle by clicking #userBadge again
        print("Test 2: Avatar toggle...")
        page.locator("#userBadge").click()
        page.wait_for_timeout(200)
        assert dd.is_visible(), "Dropdown should be visible after clicking avatar"
        page.locator("#userBadge").click()
        page.wait_for_timeout(200)
        assert not dd.is_visible(), "Dropdown MUST be closed after clicking avatar again"
        print("Test 2 Passed: Avatar toggle closed dropdown successfully.")

        # Test 3: Click outside (backdrop / document click)
        print("Test 3: Click outside...")
        page.locator("#userBadge").click()
        page.wait_for_timeout(200)
        assert dd.is_visible(), "Dropdown should be visible after clicking avatar"
        page.locator("#appTitle").click()
        page.wait_for_timeout(200)
        assert not dd.is_visible(), "Dropdown MUST be closed after clicking outside"
        print("Test 3 Passed: Clicking outside closed dropdown successfully.")

        # Test 4: Edit Profile button closes dropdown and navigates to Step 2
        print("Test 4: Edit Profile button...")
        page.locator("#userBadge").click()
        page.wait_for_timeout(200)
        assert dd.is_visible(), "Dropdown should be visible after clicking avatar"
        page.locator("#btnDropdownEditProfile").click()
        page.wait_for_timeout(300)
        assert not dd.is_visible(), "Dropdown MUST be closed after clicking Edit Profile"
        reg_page = page.locator("#page2Registration")
        assert reg_page.is_visible(), "Should navigate to Step 2 registration page"
        print("Test 4 Passed: Edit Profile closed dropdown and navigated to Step 2.")

        browser.close()
        print("\n>>> ALL 4 CLOSE INTERACTIONS VERIFIED AND PASSED 100%! <<<")

if __name__ == '__main__':
    verify_all_close_interactions()
