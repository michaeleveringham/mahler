import unittest
from unittest.mock import patch, MagicMock

import pytest

from mahler.engines.playwright_.element import PlaywrightElement
from mahler.engines.playwright_.window import (
    _create_browser,
    _install_playwright,
    PlaywrightWindow,
)


def test_install_called_with_deps():
    with patch("mahler.engines.playwright_.window.subprocess.check_output") as mock_call:
        _install_playwright()
    assert "--with-deps" in mock_call.call_args.args[0]


@pytest.mark.parametrize(
    "browser_name, truth",
    [
        ("chrome", True),
        ("firefox", False),  # Sanity check.
    ]
)
def test_chrome_maps_to_chromium(browser_name, truth):
    mock_playwright = MagicMock()
    mock_playwright.start = lambda *_, **__: mock_playwright
    with patch("mahler.engines.playwright_.window.sync_playwright", return_value=mock_playwright):
        _create_browser(browser_name)
    assert mock_playwright.chromium.launch.called == truth


class TestPlaywrightWindow(unittest.TestCase):
    def setUp(self):
        self.mock_page = MagicMock()
        with (
            patch("mahler.engines.playwright_.window._install_playwright") as mock_install,
            patch("mahler.engines.playwright_.window._create_browser", return_value=self.mock_page),
        ):
            self.window = PlaywrightWindow("chrome")
        self.mock_install = mock_install

    def test_install_called_on_instantiation(self):
        self.mock_install.assert_any_call()

    def test_goto_timeout_in_milliseconds(self):
        timeout = 30
        self.window.goto("url", timeout)
        assert self.mock_page.goto.call_args.kwargs["timeout"] == timeout * 1000

    def test_query_selectors_returns_none_not_empty_type(self):
        for target in ["query_selector_all", "query_selector"]:
            with patch.object(self.mock_page, target, return_value=None):
                method = getattr(self.window, target)
                assert method("selector") is None

    def test_query_selector_all_return_type(self):
        mock_element_handles = [MagicMock(), MagicMock()]
        with patch.object(self.mock_page, "query_selector_all", return_value=mock_element_handles):
            elements = self.window.query_selector_all("selector")
        assert isinstance(elements, list)
        for index, element in enumerate(elements):
            assert isinstance(element, PlaywrightElement)
            assert element._element_handle == mock_element_handles[index]

    def test_query_selector_return_type(self):
        element_handle = MagicMock()
        with patch.object(self.mock_page, "query_selector", return_value=element_handle):
            element = self.window.query_selector("selector")
        assert isinstance(element, PlaywrightElement)
        assert element._element_handle == element_handle


class TestPlaywrightElement(unittest.TestCase):
    def setUp(self):
        self.mock_element_handle = MagicMock()
        self.element = PlaywrightElement(self.mock_element_handle)

    def test_no_parent_at_top_level(self):
        assert self.element.parent == None

    def test_query_selector_all_returns(self):
        mock_element_handles = [MagicMock(), MagicMock()]
        with patch.object(self.mock_element_handle, "query_selector_all", return_value=mock_element_handles):
            elements = self.element.query_selector_all("selector")
        for index, element in enumerate(elements):
            assert element._element_handle == mock_element_handles[index]
            assert element.parent == self.element

    def test_query_selector_returns(self):
        mock_element_handle = MagicMock()
        with patch.object(self.mock_element_handle, "query_selector", return_value=mock_element_handle):
            element = self.element.query_selector("selector")
        assert element._element_handle == mock_element_handle
        assert element.parent == self.element
    
    def test_click(self):
        self.element.click()
        self.mock_element_handle.click.assert_called_once()
    
    def test_content(self):
        self.element.content()
        self.mock_element_handle.text_content.assert_called_once()
    
    def test_type_on(self):
        text = "text"
        self.element.type_on(text)
        assert self.mock_element_handle.type.call_args.args[0] == text
    
    def test_type_on_delay_in_milliseconds(self):
        delay = 0.05
        self.element.type_on("text", delay=delay)
        assert self.mock_element_handle.type.call_args.kwargs["delay"] == delay * 1000
    