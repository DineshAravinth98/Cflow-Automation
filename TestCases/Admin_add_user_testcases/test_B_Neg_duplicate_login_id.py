import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from PageObjects.B_Admin_Add_user import Admin_Add_User
from Utilities.BaseHelpers import BaseHelper


class Test_003_Admin_Add_User_Negative:

    def test_duplicate_login_id(self, login):
        """
        ✅ Negative Test:
        Verify system shows 'Username Already Exist' toast when duplicate Login ID is entered.
        """
        page = login
        admin = Admin_Add_User(page)
        helper = BaseHelper(page)

        print("🚨 Starting Negative Test: Duplicate Login ID")

        # Step 1: Navigate to Admin
        admin.navigate_to_admin()
        page.wait_for_timeout(1000)

        # Step 2: Click Add User
        admin.click_add_user()
        page.wait_for_timeout(2000)

        # Step 3: Fill all mandatory fields but use a known duplicate Login ID
        admin.enter_name("Existing_User")
        admin.enter_department("QA")
        admin.enter_email("existinguser@yopmail.com")

        duplicate_login_id = "dinesh01"  # 🔁 Known duplicate
        admin.enter_login_id(duplicate_login_id)
        admin.enter_password("Test@123")
        admin.enter_employee_number("123466")
        admin.select_role(["User"])
        admin.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")


        admin.verify_duplicate_login_toast("Username Already Exist")



    def test_duplicate_employee_number(self, login):
        """
        ✅ Negative Test:
        Verify system shows 'Employee No Already Exist' toast when duplicate Employee No is entered.
        """
        page = login
        admin = Admin_Add_User(page)
        helper = BaseHelper(page)

        print("🚨 Starting Negative Test: Duplicate Employee Number")

        page.reload()

        # Step 1: Navigate to Admin
        admin.navigate_to_admin()
        page.wait_for_timeout(1000)

        # Step 2: Click Add User
        admin.click_add_user()
        page.wait_for_timeout(2000)

        # Step 3: Fill all mandatory fields but use a known duplicate Employee No
        admin.enter_name("Existing_Employee")
        admin.enter_department("QA")
        admin.enter_email("existingemp@yopmail.com")
        admin.enter_login_id("unique_login_id_0021")
        admin.enter_password("Test@123")

        duplicate_emp_no = "E01"  # 🔁 Known duplicate
        admin.enter_employee_number(duplicate_emp_no)
        admin.select_role(["User"])
        admin.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")

        # Step 4: Try savin

        admin.verify_duplicate_emp_toast()


