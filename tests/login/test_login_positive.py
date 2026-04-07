import time

from configs.settings import TEST_APP_URL
from framework.ui.browser.browser import Browser
from pages.LoginPage import LoginPage
from pages.main_page import MainPage
import allure


@allure.feature("LogIn")
@allure.story("Valid credentials")
class TestLoginPositive:

    def test_log_in(self,browser:Browser,credentials):

        browser.open_url(TEST_APP_URL)

        login_page=LoginPage(browser.page)

        login_page.write_user_name(credentials["username"])
        login_page.write_password(credentials["password"])
        login_page.clicking_login_button()

        main_page=MainPage(browser.page)

        assert main_page.is_page_open()


