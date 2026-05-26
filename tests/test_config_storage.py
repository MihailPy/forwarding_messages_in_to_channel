import pytest

from services.config_storage import find_account, parse_channel_input


def test_parse_channel_input_converts_number() -> None:
    assert parse_channel_input("-1001234567890") == -1001234567890


def test_parse_channel_input_keeps_username() -> None:
    assert parse_channel_input("@channel") == "@channel"


def test_parse_channel_input_strips_value() -> None:
    assert parse_channel_input("  @channel  ") == "@channel"


def test_find_account_returns_account() -> None:
    config = {
        "accounts": [
            {"name": "account_1"},
            {"name": "account_2"},
        ]
    }

    assert find_account(config, "account_2") == {"name": "account_2"}


def test_find_account_raises_for_missing_account() -> None:
    config = {"accounts": []}

    with pytest.raises(ValueError):
        find_account(config, "missing")
