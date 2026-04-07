from typing import Union

from playwright.sync_api import Locator

from framework.ui.constants.elements import ElementType
from framework.ui.decorators.decorators import action
from framework.ui.elements.base_element import BaseElement


class Dropdown(BaseElement):

    def __init__(self, page, locator: Union[Locator, str], name: str):
        super().__init__(page, locator, name, ElementType.DROPDOWN)

    @action("Select option from dropdown")
    def select_option(self, option=None):
        self.locator.select_option(option)
