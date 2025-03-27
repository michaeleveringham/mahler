from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Element(Protocol):
    def __init__(
        self,
        native_element: Any,
        parent: Element | None = None,
    ) -> None:
        """
        Remote browser object API.

        Args:
            native_element (Any): The native element API for the underlying
                automation suite.
            parent (Element | None, optional): The parent. Defaults to None.
        """
        ...

    @property
    def parent(self) -> Element | None:
        """The parent element this was selected from, if any."""
        ...

    def query_selector_all(self, selector: str) -> list[Element] | None:
        """
        Select all child elements of this node that match the given selector.

        Args:
            selector (str): A CSS or XPATH selector string.

        Returns:
            list[Element] | None: A list of elements found, if any.
                Otherwise, None.
        """
        ...

    def query_selector(self, selector: str) -> Element | None:
        """
        Select the first child element of this node that matches the given
        selector.

        Args:
            selector (str): A CSS or XPATH selector string.

        Returns:
            list[Element] | None: Found element, if any. Otherwise, None.
        """
        ...

    def click(self) -> None:
        """Click on this element."""
        ...

    def content(self) -> str:
        """Return the text content of this element."""
        ...

    def type_on(self, text: str, delay: float = 0) -> None:
        """
        Emulate typing on this element.

        Args:
            text (str): Text to type.
            delay (float, optional): Time in seconds to wait between keys.
                Defaults to 0.
        """
        ...
