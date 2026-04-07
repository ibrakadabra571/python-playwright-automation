from playwright.sync_api import Page

from framework.ui.pages.base_page import BasePage


class MainPage(BasePage):

    def __init__(self,page:Page):

        header_locator=page.locator("[data-test='title']")
        super().__init__(page,header_locator,"Main Page")

