from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("http://host.docker.internal:8080")
    page.wait_for_timeout(2000)

    page.screenshot(path="output/preview.png", full_page=True)

    browser.close()
