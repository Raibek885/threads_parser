from playwright.sync_api import sync_playwright

def get_threads_html(keyword: str) -> str:
    """Open Threads search page for the given keyword and return the HTML content."""
    url = f"https://www.threads.net/search?q={keyword}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(4000)  # we are waiting for content to load.You can increase if needed
        html = page.content()
        browser.close()
        return html