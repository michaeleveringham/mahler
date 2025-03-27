from typing import Literal, Protocol, runtime_checkable

from mahler.protocols.element import Element
from mahler.fingerprint import Fingerprint


@runtime_checkable
class Window(Protocol):
    def __init__(
        self,
        model: Literal["chrome", "firefox"],
        headless: bool = True,
        enable_javascript: bool = True,
        fingerprint: Fingerprint | None = None,
    ):
        """
        Remote browser interactive API.

        Args:
            model (Literal["chrome", "firefox"]): Browser type.
            headless (bool, optional): Run in headless mode. Defaults to True.
            enable_javascript (bool, optional): Enable JavaScript in browser.
                Defaults to True.
            fingerprint (Fingerprint | None, optional): Browser fingerprint
                to apply, if any. Defaults to None.
        """
        ...

    def goto(self, url: str, timeout: float | None = None) -> None:
        """
        Navigate to a URL.

        Args:
            url (str): URL to visit.
            timeout (float | None, optional): Time in seconds to let load.
                Defaults to None.
        """
        ...

    def query_selector_all(self, selector: str) -> list[Element] | None:
        """
        Select all elements on the page that match the given selector.

        Args:
            selector (str): A CSS or XPATH selector string.

        Returns:
            list[Element] | None: A list of elements found, if any.
                Otherwise, None.
        """
        ...

    def query_selector(self, selector: str) -> Element | None:
        """
        Select the first element on the page that matches the given selector.

        Args:
            selector (str): A CSS or XPATH selector string.

        Returns:
            list[Element] | None: Found element, if any. Otherwise, None.
        """
        ...
