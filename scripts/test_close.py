from playwright.sync_api import sync_playwright

def test_close_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))

        page.goto("http://127.0.0.1:8000")
        page.wait_for_selector("#userBadge")

        # Open dropdown
        print("Opening dropdown...")
        page.locator("#userBadge").click()
        page.wait_for_timeout(300)

        dd = page.locator("#profileDropdown")
        print("Is dropdown visible after userBadge click?", dd.is_visible())
        print("Dropdown inline display style:", page.evaluate("() => document.getElementById('profileDropdown').style.display"))

        # Click close button
        print("Clicking #btnDropdownClose...")
        page.locator("#btnDropdownClose").click()
        page.wait_for_timeout(300)

        print("Is dropdown visible after #btnDropdownClose click?", dd.is_visible())
        print("Dropdown inline display style:", page.evaluate("() => document.getElementById('profileDropdown').style.display"))

        browser.close()

if __name__ == '__main__':
    test_close_button()
