from __future__ import annotations

import time

from selenium.common.exceptions import (
    InvalidSelectorException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def _find_elements(
    finder: WebDriver | WebElement,
    selector: str,
    first: bool,
) -> None | WebElement | list[WebElement]:
    """Find elements on a given Selenium driver or element."""
    method = finder.find_element if first else finder.find_elements
    try:
        web_elements = method(By.XPATH, selector)
        # Always try with CSS if xpath fails.
        if not web_elements:
            raise NoSuchElementException
    except (NoSuchElementException, InvalidSelectorException):
        try:
            web_elements = method(By.CSS_SELECTOR, selector)
        except (NoSuchElementException, InvalidSelectorException):
            return None
    return web_elements


class SeleniumElement:
    """
    Selenium implementation of an Element.

    See mahler.protocols.element.Element for API details.
    """
    def __init__(
        self,
        web_element: WebElement,
        parent: SeleniumElement | None = None,
    ) -> None:
        self._web_element = web_element
        self._parent = parent

    def __repr__(self):
        return f"Element <SeleniumElement {id(self)}>"

    @property
    def parent(self) -> SeleniumElement | None:
        return self._parent

    def query_selector_all(self, selector: str) -> list[SeleniumElement] | None:
        web_elements = _find_elements(self._web_element, selector, False)
        if not web_elements:
            return None
        return [SeleniumElement(e,  self) for e in web_elements]

    def query_selector(self, selector: str) -> SeleniumElement | None:
        web_element = _find_elements(self._web_element, selector, True)
        if not web_element:
            return None
        return SeleniumElement(web_element, self)

    def click(self) -> None:
        self._web_element.click()

    def content(self) -> str:
        return self._web_element.text

    def type_on(self, text: str, delay: float = 0) -> None:
        if not delay:
            self._web_element.send_keys(text)
        else:
            for char in text:
                self._web_element.send_keys(char)
                time.sleep(delay)
