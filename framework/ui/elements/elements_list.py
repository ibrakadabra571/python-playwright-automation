from typing import List, Type, Union
from playwright.sync_api import Page, Locator
import logging

from framework.ui.decorators.decorators import action
from framework.ui.elements.base_element import BaseElement
from framework.ui.constants.elements import ElementType

logger = logging.getLogger(__name__)


class ElementsList(BaseElement):
    """
    Represents a list of elements of the same type.

    Each found element will be instantiated as `element_class`.
    """

    def __init__(
        self,
        page: Page,
        locator: Union[Locator, str],
        name: str,
        element_class: Type[BaseElement],
        element_type: ElementType = ElementType.ELEMENT,
    ):
        super().__init__(page, locator, name, element_type)
        self._element_class = element_class

    @action("Get list of elements")
    def get_list_of_elements(self) -> List[BaseElement]:
        """
        Finds all elements matching the locator and returns a list of element_class instances.
        """
        logger.info(f'Getting all elements "{self._name}"')

        count = self._locator.count()
        logger.info(f"Found '{count}' elements")

        elements = [
            self._element_class(self._page, self._locator.nth(i), f"{self._name} #{i}")
            for i in range(count)
        ]
        return elements
