from playwright.sync_api import sync_playwright

def test_debug():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))

        page.goto("http://127.0.0.1:8000")
        page.wait_for_selector("#userBadge")

        page.evaluate("goToStep(2)")
        page.fill("#inputRegName", "Vikram Seth")
        page.fill("#inputRegEmail", "vikram.seth@example.com")
        page.select_option("#selectRegGender", "male")
        page.fill("#inputRegPhone", "9876543210")
        page.fill("#inputRegAge", "42")
        page.check("#chkConsentResearch")
        page.check("#chkConsentStorage")
        page.wait_for_timeout(200)

        page.locator("#btnSubmitRegistration").click()
        page.wait_for_timeout(1000)

        badge_txt = page.locator("#userNameBadge").text_content()
        print("userNameBadge text:", badge_txt)

        prof = page.evaluate("() => localStorage.getItem('ocuscan_user_profile')")
        print("localStorage profile:", prof)

        page.locator("#userBadge").click()
        page.wait_for_timeout(300)

        dd_name = page.locator("#dropdownUserName").text_content()
        print("dropdownUserName text:", dd_name)

        browser.close()

if __name__ == '__main__':
    test_debug()
