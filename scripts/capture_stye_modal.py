from playwright.sync_api import sync_playwright

artifact_path = r'C:\Users\sarth\.gemini\antigravity\brain\70fdcf38-6d56-4d81-939c-67094dd39db0\final_stye_modal_audited.png'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 950})
    page.goto('http://127.0.0.1:8000')
    page.wait_for_timeout(1000)
    page.click('#btnNavReliability')
    page.wait_for_timeout(1500)
    
    # Click the last .btn-rel-details
    page.locator('.btn-rel-details').last.click()
    page.wait_for_timeout(600)
    page.screenshot(path=artifact_path)
    print('Modal screenshot successfully saved to', artifact_path)
    browser.close()
