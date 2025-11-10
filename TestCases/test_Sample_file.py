from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--window-position=0,0",
                "--window-size=1536,864"   # 👈 your exact screen resolution
            ]
        )
        context = browser.new_context(
            viewport={"width": 1536, "height": 864}  # 👈 match viewport to your display
        )
        page = context.new_page()
        page.goto("https://testapp.cflowapps.com/cflow/login")
        print("\n✅ Browser launched full-screen at 1536x864.")
        input("Press Enter to close...")

if __name__ == "__main__":
    run()
