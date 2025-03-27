import warnings
from typing import Literal

from mahler.engines import (PlaywrightWindow, SeleniumWindow)
from mahler.fingerprint import Fingerprint
from mahler.protocols import Element, Window


ENGINE_TO_WINDOW_CLS = {
    "playwright": PlaywrightWindow,
    "selenium": SeleniumWindow,
}


class Controller:
    def __init__(
        self,
        engine: Literal["playwright", "selenium"],
        model: Literal["chrome", "firefox"],
        headless: bool = True,
        enable_javascript: bool = True,
        fingerprint: Fingerprint | None = None,
        user_agent: str | None = None,
    ):
        """
        Controller class to interact with a browser window.

        Args:
            engine (Literal["playwright", "selenium"]): Automation suite
                to use.
            model (Literal["chrome", "firefox"]): Browser type.
            headless (bool, optional): Run in headless mode. Defaults to True.
            enable_javascript (bool, optional): Enable JavaScript in browser.
                Defaults to True.
            fingerprint (Fingerprint | None, optional): Browser fingerprint
                to apply, if any. Defaults to None.
            user_agent (str | None, optional): User agent to apply to browser,
                if any. Defaults to None.

        Raises:
            ValueError: Raised if an invalid engine is given.
        """
        self._engine = engine
        self._model = model
        if user_agent:
            if fingerprint:
                warnings.warn("User agent ignored, fingerprint given.")
            else:
                fingerprint = Fingerprint(headers=None, user_agent=user_agent)
        window_cls: Window = ENGINE_TO_WINDOW_CLS.get(engine)
        if not window_cls:
            raise ValueError("Invalid engine given.")
        self._window: Window = window_cls(
            model,
            headless=headless,
            enable_javascript=enable_javascript,
            fingerprint=fingerprint,
        )

    def __repr__(self) -> str:
        kind = f"{self.engine.title()} {self.model.title()}"
        return f"Controller <{kind} at {id(self)}>"

    @property
    def engine(self) -> str:
        """Automation suite being used."""
        return self._engine

    @property
    def model(self) -> str:
        """Browser type."""
        return self._model

    @property
    def window(self) -> Window:
        """Current window object for the controller."""
        return self._window

    def goto(self, url: str, timeout: float | None = None) -> None:
        """
        Navigate to a URL.

        Args:
            url (str): URL to visit.
            timeout (float | None, optional): Time in seconds to let load.
                Defaults to None.
        """
        self._window.goto(url, timeout)

    def query_selector_all(self, selector: str) -> list[Element] | None:
        """
        Select all elements on the page that match the given selector.

        Args:
            selector (str): A CSS or XPATH selector string.

        Returns:
            list[Element] | None: A list of elements found, if any.
                Otherwise, None.
        """
        return self._window.query_selector_all(selector)

    def query_selector(self, selector: str) -> Element | None:
        """
        Select the first element on the page that matches the given selector.

        Args:
            selector (str): A CSS or XPATH selector string.

        Returns:
            list[Element] | None: Found element, if any. Otherwise, None.
        """
        return self._window.query_selector(selector)
