import pytest
from PageObjects.B_Admin_Add_user import Admin_Add_User
from Utilities.BaseHelpers import BaseHelper

class Test_002_Admin_Add_User_Positive_cases:

    def test_add_user_with_active_status(self, login):
        page = login
        admin = Admin_Add_User(page)
        helper = BaseHelper(page)

        print("\n🚀  Starting Test Case: 'Add User in Admin Module'")

        # Step 1: Navigate to Admin section
        admin.navigate_to_admin()
        page.wait_for_timeout(1000)

        expected_url_fragment = "/user-role-permission"
        helper.verify_page_url(expected_url_fragment, "Admin")


        # Step 2: Click on Add User
        admin.click_add_user()
        page.wait_for_timeout(2000)

        # Step 3: Fill user details
        username = admin.enter_name()       # ✅ Capture the random name
        page.wait_for_timeout(500)

        admin.enter_department("QA")
        page.wait_for_timeout(500)

        admin.enter_email("dinesh123@yopmail.com")
        page.wait_for_timeout(500)

        admin.enter_login_id()
        page.wait_for_timeout(500)

        admin.print_visible_password_validations()
        page.wait_for_timeout(5000)

        admin.enter_password()
        page.wait_for_timeout(500)

        admin.enter_employee_number()
        page.wait_for_timeout(500)

        admin.select_role(["User"])
        page.wait_for_timeout(500)

        admin.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")
        page.wait_for_timeout(500)

        admin.enable_send_welcome_mail()
        page.wait_for_timeout(500)

        # 💾 Step 4: Save User
        admin.click_save()
        page.wait_for_timeout(2000)

        print("✅ User added successfully (random data used)")
        page.wait_for_timeout(2000)

        # 👁 Step 5: Verify user in 'All Users' section
        admin.click_all_users_radio()
        page.wait_for_timeout(500)

        # 🔘 Step 6: Verify user status toggle
        admin.verify_user_in_all_users(username)
        status = admin.verify_user_status_toggle(username)
        print(f"✅ Verified user '{username}' is listed and status is '{status}'")

        print("\n🎯 Test Completed Successfully — 'Add User' flow verified end-to-end.\n")

    def test_add_user_with_disabled_status(self, login):
        page = login
        admin = Admin_Add_User(page)
        helper = BaseHelper(page)

        print("\n🚀  Starting Test Case: 'Add User in Admin Module with Status Disabled'")
        page.reload()
        page.wait_for_timeout(500)

        # Step 1: Navigate to Admin section
        admin.navigate_to_admin()
        page.wait_for_timeout(1000)

        expected_url_fragment = "/user-role-permission"
        helper.verify_page_url(expected_url_fragment, "Admin")

        # Step 2: Click on Add User
        admin.click_add_user()
        page.wait_for_timeout(2000)

        # Step 3: Fill user details
        username = admin.enter_name()  # ✅ Capture the random name
        page.wait_for_timeout(500)

        admin.enter_department("QA")
        page.wait_for_timeout(500)

        admin.enter_email("dinesh123@yopmail.com")
        page.wait_for_timeout(500)

        admin.enter_login_id()
        page.wait_for_timeout(500)

        admin.enter_password("Test@123")
        page.wait_for_timeout(500)

        admin.enter_employee_number()
        page.wait_for_timeout(500)

        admin.select_role(["User"])
        page.wait_for_timeout(500)

        admin.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")
        page.wait_for_timeout(500)

        admin.disable_user_status_toggle()
        page.wait_for_timeout(500)

        admin.enable_send_welcome_mail()
        page.wait_for_timeout(500)

        # 💾 Step 4: Save User
        admin.click_save()
        page.wait_for_timeout(2000)

        print("\n✅ User added successfully (random data used) with status disabled")
        page.wait_for_timeout(2000)

        # 👁 Step 5: Verify user in 'All Users' section
        admin.click_all_users_radio()
        page.wait_for_timeout(500)

        # 🔘 Step 6: Verify user status toggle
        admin.verify_user_in_all_users(username)
        status = admin.verify_user_status_toggle_disabled(username)
        print(f"✅ Verified user '{username}' is listed and status is '{status}'")

        print("\n🎯 Test Completed Successfully — 'Add User without Status' flow verified end-to-end.\n")


