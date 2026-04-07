
from playwright.sync_api import Page

from framework.ui.elements.button import Button
from framework.ui.elements.input import Input
from framework.ui.elements.label import Label
from framework.ui.pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        header_locator = page.locator('.login-box')
        super().__init__(page, header_locator, "Log in Page")

        self._username_field=Input(page,'#user-name',"Username Field")

        self._password_field=Input(page,"#password","Password Field")

        self._login_button=Button(page,"#login-button","LOGIN Button")

        self._error_message=Label(page,"[data-test='error']","Error message")

    def write_user_name(self,user_name):
        self._username_field.type_text(user_name)


    def write_password(self,user_password):
        self._password_field.type_text(user_password)


    def clicking_login_button(self):
        self._login_button.click()

    def get_error_message(self):
        return self._error_message.get_text()






