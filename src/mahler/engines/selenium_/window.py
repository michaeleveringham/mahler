from typing import Literal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


from mahler.engines.selenium_.element import SeleniumElement, _find_elements
from mahler.fingerprint import Fingerprint


def _create_chromium_browser(
    headless: bool = True,
    enable_javascript: bool = True,
    user_agent: str | None = None,
) -> WebDriver:
    options = ChromeOptions()
    options.headless = headless
    if headless:
        options.add_argument('--headless=new')
    if not enable_javascript:
        prefs = {}
        prefs["webkit.webprefs.javascript_enabled"] = False
        prefs["profile.content_settings.exceptions.javascript.*.setting"] = 2
        prefs["profile.default_content_setting_values.javascript"] = 2
        prefs["profile.managed_default_content_settings.javascript"] = 2
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--disable-javascript')
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
    return webdriver.Chrome(
        options=options,
        service=ChromeService(ChromeDriverManager().install())
    )


def _create_firefox_browser(
    headless: bool = True,
    enable_javascript: bool = True,
    user_agent: str | None = None,
) -> WebDriver:
    options = FirefoxOptions()
    options.headless = headless
    options.set_preference("javascript.enabled", enable_javascript)
    if user_agent:
        options.set_preference("general.useragent.override", user_agent)
    return webdriver.Firefox(
        options=options,
        service=FirefoxService(GeckoDriverManager().install())
    )


def _create_browser(
    model: Literal["chrome", "firefox"],
    headless: bool = True,
    enable_javascript: bool = True,
    user_agent: str | None = None,
) -> WebDriver:
    match model:
        case "chrome":
            return _create_chromium_browser(
                headless=headless,
                enable_javascript=enable_javascript,
                user_agent=user_agent,
            )
        case "firefox":
            return _create_firefox_browser(
                headless=headless,
                enable_javascript=enable_javascript,
                user_agent=user_agent,
            )
    raise RuntimeError("Invalid model given, can't create browser.")


class SeleniumWindow:
    """
    Selenium implementation of a Window.

    See mahler.protocols.window.Window for API details.
    """
    def __init__(
        self,
        model: Literal["chrome", "firefox"],
        headless: bool = True,
        enable_javascript: bool = True,
        fingerprint: Fingerprint | None = None,
    ):
        self._driver = _create_browser(
            model=model,
            headless=headless,
            enable_javascript=enable_javascript,
            user_agent=fingerprint.user_agent if fingerprint else None,
        )

    def goto(self, url: str, timeout: float | None = None) -> None:
        if timeout:
            self._driver.set_page_load_timeout(timeout)
        self._driver.get(url)

    def query_selector_all(self, selector: str) -> list[SeleniumElement] | None:
        web_elements = _find_elements(self._driver, selector, False)
        if not web_elements:
            return None
        return [SeleniumElement(e) for e in web_elements]

    def query_selector(self, selector: str) -> SeleniumElement | None:
        web_element = _find_elements(self._driver, selector, True)
        if not web_element:
            return None
        return SeleniumElement(web_element)
