from playwright.sync_api import sync_playwright

def test_debug2():
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

        # Before submit
        print("Before submit, currProfile:", page.evaluate("() => typeof currentUserProfile !== 'undefined' ? currentUserProfile : 'UNDEFINED_VAR'"))

        page.locator("#btnSubmitRegistration").click()
        page.wait_for_timeout(1000)

        print("After submit, currProfile:", page.evaluate("() => typeof currentUserProfile !== 'undefined' ? currentUserProfile : 'UNDEFINED_VAR'"))

        browser.close()

if __name__ == '__main__':
    test_debug2()
