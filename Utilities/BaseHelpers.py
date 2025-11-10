import os
from datetime import datetime
from playwright.sync_api import Page, TimeoutError


class BaseHelper:
    def __init__(self, page: Page):
        self.page = page
        self.screenshot_dir = r"D:\CFLOW PLAYWRIGHT\Screenshots"

    # ---------------------------------------------------------------
    # Utility: Screenshot
    # ---------------------------------------------------------------
    def take_screenshot(self, prefix="Error"):
        os.makedirs(self.screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(self.screenshot_dir, f"{prefix}_{timestamp}.png")
        self.page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot saved at: {screenshot_path}")
        return screenshot_path

    # ---------------------------------------------------------------
    # Common Actions
    # ---------------------------------------------------------------
    def click(self, locator, description: str = "element", timeout: int = 5000):
        """Click an element and stop test on failure."""
        try:
            element = self.page.locator(locator) if isinstance(locator, str) else locator
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.click(timeout=timeout)
            print(f"✅ Clicked: {description}")

        except Exception as e:
            self.take_screenshot(f"ClickFailed_{description.replace(' ', '_')}")
            error_msg = f"❌ Test failed — Unable to click {description}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    def enter_text(self, locator, text: str, description: str = "textbox", timeout: int = 5000):
        """Enter text into a field and stop test on failure."""
        try:
            element = self.page.locator(locator) if isinstance(locator, str) else locator
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.fill("")  # Clear any existing text
            element.fill(text)
            print(f"✅ Entered '{text}' into {description}")

        except Exception as e:
            self.take_screenshot(f"EnterTextFailed_{description.replace(' ', '_')}")
            error_msg = f"❌ Test failed — Unable to enter text in {description}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    def scroll_to_label(self, locator, friendly_name: str = None, timeout: int = 5000):
        """Scroll to a label element and confirm visibility."""
        try:
            element = self.page.locator(locator) if isinstance(locator, str) else locator
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            label_text = friendly_name or element.inner_text().strip()
            print(f"✅ Label visible — {label_text}")
            return element

        except Exception as e:
            self.take_screenshot(f"LabelNotVisible_{friendly_name or 'Unknown'}")
            error_msg = f"❌ Test failed — Label not visible: {friendly_name or locator}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # ---------------------------------------------------------------
    # Page Verification
    # ---------------------------------------------------------------
    def verify_page_url(self, expected_url_fragment: str, description: str = "page", timeout: int = 10000):
        """Verify the page URL contains the expected fragment."""
        try:
            print(f"🌍  Verifying {description} URL ...")
            self.page.wait_for_url(f"**{expected_url_fragment}**", timeout=timeout)
            actual_url = self.page.url

            if expected_url_fragment in actual_url:
                print(f"🏆  {description} URL verification passed! ✅")
                print(f"Actual URL: '{actual_url}'")
            else:
                raise AssertionError(
                    f"❌ {description} URL verification failed.\n"
                    f"Expected fragment: '{expected_url_fragment}'\n"
                    f"Actual URL: '{actual_url}'"
                )

        except Exception as e:
            self.take_screenshot(f"URL_Verification_Failed_{description.replace(' ', '_')}")
            error_msg = f"❌ Test failed — {description} URL verification failed: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # ---------------------------------------------------------------
    # User Verification
    # ---------------------------------------------------------------
    def verify_user_in_all_users(self, username: str, description: str = "'All Users list'", timeout: int = 10000):
        """Verify that a specific user appears in the 'All Users' list."""
        print(f"🔍  Verifying if user '{username}' is listed under {description}...")
        try:
            user_locator = self.page.locator(
                f'//div[contains(@class,"admin-grid-item")]//p[normalize-space(text())="{username}"]'
            )
            user_locator.wait_for(state="visible", timeout=timeout)
            print(f"✅ User '{username}' is visible in {description}.")

        except Exception as e:
            self.take_screenshot(f"UserNotFound_{username}")
            error_msg = f"❌ Test failed — User '{username}' not found in {description}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    def verify_user_status_toggle(self, username: str, description: str = "'User Status Toggle'", timeout: int = 10000):
        """
        Verify whether the given user's status toggle is enabled (Active) or disabled (Inactive).
        """
        print(f"🔍  Verifying user status toggle for '{username}' under {description}...")
        try:
            toggle_locator = self.page.locator(
                f'//p[normalize-space()="{username}"]/ancestor::div[contains(@class,"admin-grid-item")]//input[@aria-label="User Status"]'
            )

            toggle_locator.wait_for(state="attached", timeout=timeout)
            is_checked = toggle_locator.is_checked()

            if is_checked:
                print(f"🔴 User '{username}' status is Active (toggle ON).")
                return "Active"
            else:
                print(f"🔴 User '{username}' status is Disabled (toggle OFF).")
                return "Disabled"

        except Exception as e:
            self.take_screenshot(f"ToggleCheckFailed_{username}")
            error_msg = f"❌ Test failed — Unable to verify toggle for '{username}': {e}"
            print(error_msg)
            raise AssertionError(error_msg)
