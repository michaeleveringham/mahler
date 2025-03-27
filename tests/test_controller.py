from unittest.mock import patch, MagicMock

import pytest

from mahler import Controller, Fingerprint


@pytest.fixture
def user_agent() -> str:
    return "user_agent"


def test_invalid_engine_raises_error():
    with pytest.raises(ValueError):
        Controller("notanengine", "firefox")


def test_user_agent_ignored_and_warned_if_fingerprint(user_agent):
    mock_window_cls = MagicMock()
    mock_engine_dict = MagicMock()
    mock_engine_dict.get = lambda *_, **__: mock_window_cls
    fingerprint = Fingerprint(headers=None, user_agent=user_agent)
    with (
        patch("mahler.controller.ENGINE_TO_WINDOW_CLS", mock_engine_dict),
        pytest.warns(UserWarning),
    ):
        Controller("playwright", "firefox", fingerprint=fingerprint, user_agent="wrong")
    assert mock_window_cls.call_args.kwargs["fingerprint"].user_agent == fingerprint.user_agent


def test_user_agent_used_if_no_fingerprint(user_agent):
    mock_window_cls = MagicMock()
    mock_engine_dict = MagicMock()
    mock_engine_dict.get = lambda *_, **__: mock_window_cls
    with patch("mahler.controller.ENGINE_TO_WINDOW_CLS", mock_engine_dict):
        Controller("playwright", "firefox", user_agent=user_agent)
    assert mock_window_cls.call_args.kwargs["fingerprint"].user_agent == user_agent
