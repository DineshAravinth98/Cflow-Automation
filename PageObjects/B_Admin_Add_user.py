from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError  # ✅ correct import
import random
import string
import re
import pytest
from Utilities.BaseHelpers import BaseHelper


class Admin_Add_User:
    def __init__(self, page: Page, timeout: int = 30):
        self.page = page
        self.timeout = timeout
        self.helper = BaseHelper(page)

        # ---------------- Locators ----------------
        self.side_nav_admin = page.get_by_role("link", name="Admin")
        self.btn_add_user = page.get_by_role("button", name="Add User")
        self.txt_name = page.locator('input[formcontrolname="name"]')
        self.txt_department = page.locator('input[formcontrolname="department"]')
        self.txt_email = page.locator('input[formcontrolname="email"]')
        self.txt_login_id = page.locator('input[formcontrolname="loginId"]')
        self.txt_password = page.locator('input[formcontrolname="password"]')
        self.txt_employee_number = page.locator('input[formcontrolname="empNo"]')
        self.dropdown_role = page.locator('ng-select[formcontrolname="role"]')
        self.label_locator = page.locator('//label[normalize-space(text())="Send welcome mail to the user?"]')
        self.toggle_send_mail = page.locator(
            "(//label[@id='flexCheckDefault' and contains(@class,'switch')]/span[@class='slider'])[2]"
        )
        self.btn_save = page.locator('//button[normalize-space(text())="Save"]')
        self.country_code_input = page.locator('//div[contains(@class, "d-flex")]/input[@placeholder="+91"]')
        self.whatsapp_input = page.locator('//div[contains(@class, "d-flex")]/input[@formcontrolname="whatsappNo"]')
        self.radio_btn_all_users = page.locator('//label[.//span[normalize-space()="All Users"]]')
        self.user_status_toggle = page.locator('//input[@type="checkbox" and @aria-label="User Status"]')
        self.toast_message = page.locator("//div[contains(@id,'toast-container')]")

    # ---------------- Random helpers ----------------
    @staticmethod
    def random_string(length=6):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    @staticmethod
    def random_email():
        return f"{Admin_Add_User.random_string(6)}@yopmail.com"

    @staticmethod
    def random_login_id():
        return f"user_{Admin_Add_User.random_string(5)}"

    @staticmethod
    def random_employee_number():
        return str(random.randint(1000, 9999))

    # ---------------- Actions ----------------
    def navigate_to_admin(self):
        print("➡ Navigating to Admin page")
        self.helper.click(self.side_nav_admin, "Admin side navigation link")

    def click_add_user(self):
        self.helper.click(self.btn_add_user, "Add User button in the Admin page")

    def enter_name(self, name=None):
        if not name:
            name = f"User_{self.random_string(5)}"
        self.helper.enter_text(self.txt_name, name, "Name textbox")
        return name

    def enter_department(self, dept):
        self.helper.enter_text(self.txt_department, dept, "Department textbox")

    def enter_email(self, email=None):
        if not email:
            email = self.random_email()

        # ✅ Validate email format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            print(f"❌ Invalid email format: '{email}'")
            pytest.fail(f"Invalid Email Format: {email}", pytrace=False)

        self.helper.enter_text(self.txt_email, email, "Email textbox")

    def enter_login_id(self, login_id=None):
        if not login_id:
            login_id = self.random_login_id()

        print(f"🔑 Entering Login ID: {login_id}")
        self.helper.enter_text(self.txt_login_id, login_id, "Login ID textbox")
        print(f"✅ Login ID entered successfully: {login_id}")
        return login_id

    def enter_password(self, password):
        self.helper.enter_text(self.txt_password, password, "Password textbox")

    def enter_employee_number(self, emp_no=None):
        if not emp_no:
            emp_no = self.random_employee_number()
        self.helper.enter_text(self.txt_employee_number, emp_no, "Employee Number textbox")

    def select_role(self, roles):
        if isinstance(roles, str):
            roles = [roles]

        print(f"🎯 Selecting roles: {roles}")
        self.helper.click(self.dropdown_role, "Roles dropdown")
        self.page.wait_for_timeout(1000)

        for role in roles:
            print(f"➡ Selecting role: '{role}'")
            role_option = self.page.get_by_text(role, exact=True)
            try:
                if role_option.count() > 0:
                    self.helper.click(role_option, f"Role option: {role}")
                    print(f"✅ Selected role: '{role}'")
                else:
                    print(f"⚠️ Role '{role}' not found.")
            except Exception as e:
                print(f"❌ Error selecting role '{role}': {e}")
            self.page.wait_for_timeout(500)

    def enter_whatsapp_number(self, country_code="91", whatsapp_no="9876543210"):
        self.helper.enter_text(self.country_code_input, country_code, "Country code input")
        self.helper.enter_text(self.whatsapp_input, whatsapp_no, "WhatsApp number input")

    def enable_send_welcome_mail(self):
        container = self.page.locator(
            '//div[@class="item" and .//label[contains(text(),"Send welcome mail to the user?")]]'
        )
        checkbox = container.locator('input[formcontrolname="sendMail"]')
        slider = container.locator('span.slider')

        container.wait_for(state="visible", timeout=5000)
        self.helper.scroll_to_label(container, "'Send welcome mail to the user?' toggle")

        is_checked = checkbox.evaluate("el => el.checked")
        if not is_checked:
            slider.click(force=True)
            self.page.wait_for_timeout(300)

        is_checked = checkbox.evaluate("el => el.checked")
        if is_checked:
            print("✔ 'Send welcome mail to the user?' toggle enabled")
        else:
            print("❌ Failed to enable 'Send welcome mail to the user?' toggle")

    def click_save(self):
        """
        Clicks the Save button and validates if a toast appears.
        Stops test execution immediately if duplicate login ID or Employee No found.
        """
        print("💾 Clicking the Save button...")
        self.helper.click(self.btn_save, "Save button")

        # Toast locator: supports both div/span structures
        toast_locator = self.page.locator("#toast-container div, #toast-container span")

        try:
            # Wait for toast to appear (max 5 seconds)
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()
            print(f"⚠️ Toast message detected after Save: {message}")

            # --- Duplicate validations ---
            if re.search(r"username\s*already\s*exist", message, re.IGNORECASE):
                print(f"❌ Duplicate Login ID detected — {message}")
                pytest.fail(f"Duplicate Login ID: {message}", pytrace=False)

            elif re.search(r"employee\s*no\s*already\s*exist", message, re.IGNORECASE):
                print(f"❌ Duplicate Employee No detected — {message}")
                pytest.fail(f"Duplicate Employee No: {message}", pytrace=False)

            # --- Generic error message handling ---
            elif re.search(r"(error|invalid|failed)", message, re.IGNORECASE):
                print(f"❌ Error message detected — {message}")
                pytest.fail(f"Form submission failed: {message}", pytrace=False)

            else:
                print(f"✅ Success message: {message}")

        except PlaywrightTimeoutError:
            # No toast appeared within timeout — assume success
            print("✅ No toast message detected — Save action successful.")
        except Exception as e:  # noqa: E722 — intentionally broad for unforeseen runtime issues
            print(f"⚠️ Unexpected error while handling toast message: {e}")

    def click_all_users_radio(self):
        """Clicks the 'All Users' radio button."""
        print("🎯 Selecting 'All Users' radio option")
        self.radio_btn_all_users.click(force=True)

    def verify_duplicate_login_toast(self, expected_message: str):
        """
        Click Save and check if expected duplicate toast appears.
        Takes screenshot if toast does not appear or message mismatch.
        """

        self.helper.click(self.btn_save, "Save button")

        toast_locator = self.page.locator("#toast-container div, #toast-container span")
        try:
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()
            print(f"⚠️ Toast message detected: {message}")

            if expected_message.lower() not in message.lower():
                # Take screenshot if message is not as expected
                self.helper.take_screenshot(prefix="DuplicateToastMismatch")
                pytest.fail(f"Expected message '{expected_message}', but got: '{message}'")

            print("✅ Negative test passed: Toast message displayed correctly")
            return True

        except PlaywrightTimeoutError:
            # Take screenshot if toast did not appear
            self.helper.take_screenshot(prefix="ToastNotFound")
            pytest.fail(f"❌ Expected toast message '{expected_message}' did not appear")

    def verify_duplicate_emp_toast(self):
        """
        Click Save and verify 'Employee No Already Exist' toast appears.
        Takes screenshot if toast does not appear or message mismatch.
        """
        self.helper.click(self.btn_save, "Save button")

        toast_locator = self.page.locator("#toast-container div, #toast-container span")
        try:
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()
            print(f"⚠️ Toast message detected: {message}")

            if "Employee No Already Exist" not in message:
                self.helper.take_screenshot(prefix="DuplicateEmpToastMismatch")
                pytest.fail(f"Expected duplicate employee number message, but got: '{message}'")

            print("✅ Negative test passed: Duplicate Employee Number message displayed correctly")

        except PlaywrightTimeoutError:
            self.helper.take_screenshot(prefix="DuplicateEmpToastNotFound")
            pytest.fail("❌ Expected duplicate Employee Number toast did not appear")