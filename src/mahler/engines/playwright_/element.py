from __future__ import annotations

from playwright.sync_api import ElementHandle


class PlaywrightElement:
    """
    Playwright implementation of an Element.

    See mahler.protocols.element.Element for API details.
    """
    def __init__(
        self,
        element_handle: ElementHandle,
        parent: PlaywrightElement | None = None,
    ) -> None:
        self._element_handle = element_handle
        self._parent = parent

    def __repr__(self):
        return f"Element <PlaywrightElement {id(self)}>"

    @property
    def parent(self) -> PlaywrightElement | None:
        return self._parent

    def query_selector_all(
        self,
        selector: str,
    ) -> list[PlaywrightElement] | None:
        element_handles = self._element_handle.query_selector_all(selector)
        if not element_handles:
            return None
        return [PlaywrightElement(e,  self) for e in element_handles]

    def query_selector(self, selector: str) -> PlaywrightElement | None:
        element_handle = self._element_handle.query_selector(selector)
        if not element_handle:
            return None
        return PlaywrightElement(element_handle, self)

    def click(self) -> None:
        self._element_handle.click()

    def content(self) -> str:
        return self._element_handle.text_content()

    def type_on(self, text: str, delay: float = 0) -> None:
        delay = delay * 1000
        self._element_handle.type(text, delay=delay)
