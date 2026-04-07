import allure

from configs.settings import TEST_APP_URL
from framework.ui.browser.browser import Browser
from pages.LoginPage import LoginPage

@allure.feature("LogIn")
@allure.story("Invalid credentials")
class TestLoginNegative:

    def test_invalid_login(self, browser: Browser, login_data):
        browser.open_url(TEST_APP_URL)

        login_page = LoginPage(browser.page)

        login_page.write_user_name(login_data["username"])
        login_page.write_password(login_data["password"])
        login_page.clicking_login_button()

        error_text = login_page.get_error_message()

        assert login_data["error"] in error_text

@allure.feature("LogIn")
@allure.story("Blocked users")
class TestLockedUsers:

    def test_locked_user_login(self, browser, locked_user):
        browser.open_url(TEST_APP_URL)

        login_page = LoginPage(browser.page)

        login_page.write_user_name(locked_user["username"])
        login_page.write_password(locked_user["password"])
        login_page.clicking_login_button()

        error = login_page.get_error_message()

        expected_message = "locked out"

        assert expected_message in error