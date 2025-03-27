import subprocess
from typing import Literal

from playwright.sync_api import sync_playwright, Page, BrowserType

from mahler.engines.playwright_.element import PlaywrightElement
from mahler.fingerprint import Fingerprint


def _install_playwright() -> None:
    """Install Playwright browsers via subprocess."""
    try:
        subprocess.check_output(
            ["playwright", "install", "--with-deps"],
        )
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to find or install browsers.")


def _create_browser(
    model: Literal["chrome", "firefox"],
    headless: bool = True,
    enable_javascript: bool = True,
    user_agent: str | None = None,
) -> Page:
    """Create Playwright browser, context, and page."""
    if model == "chrome":
        model = "chromium"
    playwright = sync_playwright().start()
    launcher: BrowserType = getattr(playwright, model)
    browser = launcher.launch(headless=headless)
    context = browser.new_context(
        java_script_enabled=enable_javascript,
        user_agent=user_agent,
    )
    page = context.new_page()
    return page


class PlaywrightWindow:
    """
    Playwright implementation of a Window.

    See mahler.protocols.window.Window for API details.
    """
    def __init__(
        self,
        model: Literal["chrome", "firefox"],
        headless: bool = True,
        enable_javascript: bool = True,
        fingerprint: Fingerprint | None = None,
    ):
        _install_playwright()
        self._page = _create_browser(
            model=model,
            headless=headless,
            enable_javascript=enable_javascript,
            user_agent=fingerprint.user_agent if fingerprint else None,
        )

    def goto(self, url: str, timeout: float | None = None) -> None:
        if timeout:
            timeout = timeout * 1000
        self._page.goto(url, wait_until="load", timeout=timeout)

    def query_selector_all(
        self,
        selector: str,
    ) -> list[PlaywrightElement] | None:
        element_handles = self._page.query_selector_all(selector)
        if not element_handles:
            return None
        return [PlaywrightElement(e) for e in element_handles]

    def query_selector(self, selector: str) -> PlaywrightElement | None:
        element_handle = self._page.query_selector(selector)
        if not element_handle:
            return None
        return PlaywrightElement(element_handle)
