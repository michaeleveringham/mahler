import unittest
from unittest.mock import patch, MagicMock, PropertyMock

import pytest
from selenium.common.exceptions import (
    InvalidSelectorException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By

from mahler.engines.selenium_.element import _find_elements, SeleniumElement
from mahler.engines.selenium_.window import (
    _create_chromium_browser,
    _create_browser,
    _create_firefox_browser,
    SeleniumWindow,
)


@pytest.fixture
def user_agent() -> str:
    return "user_agent"


@pytest.mark.parametrize("headless", [True, False])
def test_chromium_browser_new_headless_if_headless(headless):
    with (
        patch("mahler.engines.selenium_.window.webdriver.Chrome") as mock_call,
        patch("mahler.engines.selenium_.window.ChromeService"),
        patch("mahler.engines.selenium_.window.ChromeDriverManager"),
    ):
        _create_chromium_browser(headless=headless)
    truth = "--headless=new" in mock_call.call_args.kwargs["options"].arguments
    assert truth == headless


def test_chromium_browser_user_agent_applied(user_agent):
    with (
        patch("mahler.engines.selenium_.window.webdriver.Chrome") as mock_call,
        patch("mahler.engines.selenium_.window.ChromeService"),
        patch("mahler.engines.selenium_.window.ChromeDriverManager"),
    ):
        _create_chromium_browser(user_agent=user_agent)
    assert f"user-agent={user_agent}" in mock_call.call_args.kwargs["options"].arguments


@pytest.mark.parametrize("enable_javascript", [True, False])
def test_chromium_browser_disable_javascript_applied(enable_javascript):
    with (
        patch("mahler.engines.selenium_.window.webdriver.Chrome") as mock_call,
        patch("mahler.engines.selenium_.window.ChromeService"),
        patch("mahler.engines.selenium_.window.ChromeDriverManager"),
    ):
        _create_chromium_browser(enable_javascript=enable_javascript)
    options = mock_call.call_args.kwargs["options"]
    # Testing inverse enable_javascript to test both ways
    assert (f"--disable-javascript" in options.arguments) is not enable_javascript
    assert ("prefs" in options.experimental_options) is not enable_javascript
    prefs = options.experimental_options.get("prefs", {})
    assert (prefs.get("webkit.webprefs.javascript_enabled") == False) is not enable_javascript
    assert (prefs.get("profile.content_settings.exceptions.javascript.*.setting") == 2) is not enable_javascript
    assert (prefs.get("profile.default_content_setting_values.javascript") == 2) is not enable_javascript
    assert (prefs.get("profile.managed_default_content_settings.javascript") == 2) is not enable_javascript


def test_firefox_browser_user_agent_applied(user_agent):
    with (
        patch("mahler.engines.selenium_.window.webdriver.Firefox") as mock_call,
        patch("mahler.engines.selenium_.window.FirefoxService"),
        patch("mahler.engines.selenium_.window.GeckoDriverManager"),
    ):
        _create_firefox_browser(user_agent=user_agent)
    assert mock_call.call_args.kwargs["options"].preferences.get("general.useragent.override") == user_agent


def test_create_browser_calls_correct_method():
    with(
        patch("mahler.engines.selenium_.window._create_chromium_browser") as mock_create_cr,
        patch("mahler.engines.selenium_.window._create_firefox_browser") as mock_create_ff,
    ):
        cr_call_count = mock_create_cr.call_count
        ff_call_count = mock_create_ff.call_count
        _create_browser("chrome")
        assert mock_create_cr.call_count > cr_call_count
        assert mock_create_ff.call_count == ff_call_count
        cr_call_count = mock_create_cr.call_count
        _create_browser("firefox")
        assert mock_create_cr.call_count == cr_call_count
        assert mock_create_ff.call_count > ff_call_count


class TestSeleniumWindow(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        with (
            patch("mahler.engines.selenium_.window._create_browser", return_value=self.mock_driver),
        ):
            self.window = SeleniumWindow("chrome")

    def test_timeout_set_before_goto(self):
        timeout = 30
        self.window.goto("url", timeout)
        assert self.mock_driver.set_page_load_timeout.call_args.args[0] == timeout

    def test_query_selectors_returns_none_not_empty_type(self):
        for target in ["query_selector_all", "query_selector"]:
            with patch("mahler.engines.selenium_.window._find_elements", return_value=None):
                method = getattr(self.window, target)
                assert method("selector") is None

    def test_query_selector_all_return_type(self):
        mock_web_elements = [MagicMock(), MagicMock()]
        with patch("mahler.engines.selenium_.window._find_elements", return_value=mock_web_elements):
            elements = self.window.query_selector_all("selector")
        assert isinstance(elements, list)
        for index, element in enumerate(elements):
            assert isinstance(element, SeleniumElement)
            assert element._web_element == mock_web_elements[index]

    def test_query_selector_return_type(self):
        web_element = MagicMock()
        with patch("mahler.engines.selenium_.window._find_elements", return_value=web_element):
            element = self.window.query_selector("selector")
        assert isinstance(element, SeleniumElement)
        assert element._web_element == web_element


@pytest.mark.parametrize("exception", [InvalidSelectorException, NoSuchElementException])
def test_find_elements_returns_none_on_selenium_exceptions(exception):
    finder = MagicMock()
    with (
        patch.object(finder, "find_element", side_effect=exception),
        patch.object(finder, "find_elements", side_effect=exception),
    ):
        try:
            assert _find_elements(finder, "selector", True) == None
            assert _find_elements(finder, "selector", False) == None
        except exception:
            raise AssertionError


def raise_on_xpath_side_effect(*args, **__):
    if args[0] == By.XPATH:
        raise InvalidSelectorException


@pytest.mark.parametrize("choice", [True, False])
def test_find_elements_fallback_to_css(choice):
    finder = MagicMock()
    method = "find_element" if choice else "find_elements"
    with (
        patch.object(finder, method, side_effect=raise_on_xpath_side_effect) as mock_call,
    ):
        _find_elements(finder, "selector", choice)
    assert mock_call.call_count == 2
    assert mock_call.call_args_list[0].args[0] == By.XPATH
    assert mock_call.call_args_list[1].args[0] == By.CSS_SELECTOR


class TestPlaywrightElement(unittest.TestCase):
    def setUp(self):
        self.mock_web_element = MagicMock()
        self.element = SeleniumElement(self.mock_web_element)

    def test_no_parent_at_top_level(self):
        assert self.element.parent == None

    def test_query_selector_all_returns(self):
        mock_web_elements = [MagicMock(), MagicMock()]
        with patch("mahler.engines.selenium_.element._find_elements", return_value=mock_web_elements):
            elements = self.element.query_selector_all("selector")
        for index, element in enumerate(elements):
            assert element._web_element == mock_web_elements[index]
            assert element.parent == self.element

    def test_query_selector_returns(self):
        mock_web_element = MagicMock()
        with patch("mahler.engines.selenium_.element._find_elements", return_value=mock_web_element):
            element = self.element.query_selector("selector")
        assert element._web_element == mock_web_element
        assert element.parent == self.element
    
    def test_click(self):
        self.element.click()
        self.mock_web_element.click.assert_called_once()
    
    def test_content(self):
        mock_text_property = PropertyMock()
        type(self.mock_web_element).text = mock_text_property
        self.element.content()
        mock_text_property.assert_called_once()
    
    def test_type_on(self):
        text = "text"
        self.element.type_on(text)
        assert self.mock_web_element.send_keys.call_args.args[0] == text
    
    def test_type_on_delay(self):
        text = "text"
        delay = 0.05
        with patch("mahler.engines.selenium_.element.time.sleep") as mock_sleep:
            self.element.type_on(text, delay=delay)
        assert mock_sleep.call_count == len(text)
        assert all(i.args[0] == delay for i in mock_sleep.mock_calls)
        assert "".join(i.args[0] for i in self.mock_web_element.send_keys.mock_calls) == text
    