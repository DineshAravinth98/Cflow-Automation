import pytest
from PageObjects.C import (
    AdminNavigationAndAddUser,
    UserVerificationAndDuplicateEmpNOLoginChecks,
    PasswordGenerationAndValidation
)
from Utilities.BaseHelpers import BaseHelper


class Test_001_Admin_Add_User_Positive_Cases:
    """✅ Admin Add User Positive Test Suite"""
    disabled_username = None  # shared username for next test

    def test_add_user_with_active_status(self, login):
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
        password_util = PasswordGenerationAndValidation(page, helper)

        print("\n🚀 Starting Test: Add User with Active Status")

        # Navigate to Admin
        admin_nav.go_to_admin()
        page.wait_for_timeout(1000)
        helper.verify_page_url("/user-role-permission", "Admin")

        # Add user
        admin_nav.click_add_user()
        page.wait_for_timeout(2000)

        username = admin_nav.enter_name()
        admin_nav.enter_department("QA")
        admin_nav.enter_email("dinesh123@yopmail.com")
        admin_nav.enter_login_id()
        old_password = password_util.enter_password()
        admin_nav.enter_employee_number()
        admin_nav.select_role(["User"])
        admin_nav.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")
        admin_nav.enable_send_welcome_mail()
        page.wait_for_timeout(500)

        # Save
        admin_nav.click_save()
        page.wait_for_timeout(2000)
        print(f"✅ User '{username}' added successfully with Active status")

        # Verify in All Users
        admin_nav.click_All_Users_radio()
        page.wait_for_timeout(5000)
        admin_nav.search_user(username, timeout=2000)
        user_verif.verify_user_in_all_users(username)
        status = user_verif.verify_user_status_toggle(username)
        print(f"🎯 Verified '{username}' appears with status: {status}")

        print("\n🚀 Next Scenario is to reset the password of the created user")

        # Reset password
        admin_nav.search_user(username)
        admin_nav.click_user_in_All_Users_page(username)
        page.wait_for_timeout(2000)
        password_util.reset_password_with_policy_check(old_password)


    def test_add_user_with_disabled_status(self, login):
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
        password_util = PasswordGenerationAndValidation(page, helper)

        print("\n🚀 Starting Test: Add User with Disabled Status")
        page.reload()
        page.wait_for_timeout(1000)

        # Navigate and add user
        admin_nav.go_to_admin()
        helper.verify_page_url("/user-role-permission", "Admin")
        admin_nav.click_add_user()
        page.wait_for_timeout(2000)

        username = admin_nav.enter_name()
        admin_nav.enter_department("QA")
        admin_nav.enter_email("dinesh123@yopmail.com")
        admin_nav.enter_login_id()
        password_util.enter_password()
        admin_nav.enter_employee_number()
        admin_nav.select_role(["User"])
        admin_nav.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")

        # Disable status and enable welcome mail
        admin_nav.disable_user_status_toggle()
        admin_nav.enable_send_welcome_mail()

        # Save
        admin_nav.click_save()
        page.wait_for_timeout(2000)
        print(f"✅ User '{username}' added successfully with Disabled status")

        # Verify
        admin_nav.click_All_Users_radio()
        user_verif.verify_user_in_all_users(username)
        user_verif.verify_user_status_toggle_disabled(username)

        # Store for next test
        Test_001_Admin_Add_User_Positive_Cases.disabled_username = username


    def test_enable_and_verify_active_user(self, login):
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)

        username = Test_001_Admin_Add_User_Positive_Cases.disabled_username
        if not username:
            pytest.skip("⚠ No disabled user from previous test — skipping.")

        print(f"\n🚀 Enabling user '{username}' and verifying in Active Users")

        # Ensure toggle is disabled
        user_verif.verify_user_status_toggle_disabled(username)

        # Enable
        user_verif.enable_user_toggle(username)
        print(f"✅ Enabled user '{username}' successfully")

        # Verify in Active Users
        admin_nav.click_Active_Users_radio_()
        user_verif.verify_user_in_Active_List(username)
        print(f"🎯 Verified '{username}' now appears in Active Users\n")
