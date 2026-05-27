import pytest

from config import parse_channel_ref, validate_string_session


def test_parse_channel_ref_accepts_int() -> None:
    assert (
        parse_channel_ref(-1001234567890, "target_channel", "account_1")
        == -1001234567890
    )


def test_parse_channel_ref_accepts_username() -> None:
    assert parse_channel_ref("@channel", "target_channel", "account_1") == "@channel"


def test_parse_channel_ref_strips_string() -> None:
    assert (
        parse_channel_ref("  @channel  ", "target_channel", "account_1") == "@channel"
    )


def test_parse_channel_ref_rejects_empty_string() -> None:
    with pytest.raises(RuntimeError):
        parse_channel_ref("", "target_channel", "account_1")


def test_validate_string_session_rejects_placeholder() -> None:
    with pytest.raises(RuntimeError):
        validate_string_session("your_string_session", "ACCOUNT_1_STRING_SESSION")


def test_validate_string_session_rejects_short_value() -> None:
    with pytest.raises(RuntimeError):
        validate_string_session("abc", "ACCOUNT_1_STRING_SESSION")


def test_validate_string_session_accepts_long_value() -> None:
    value = "a" * 120

    assert validate_string_session(value, "ACCOUNT_1_STRING_SESSION") == value
