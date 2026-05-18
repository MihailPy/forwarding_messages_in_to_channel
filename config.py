import os

from dotenv import load_dotenv

from models.account import AccountConfig

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise RuntimeError(f"Required environment variable {name} is not set")

    return value


def get_required_int_env(name: str) -> int:
    value = get_required_env(name)

    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer") from exc


def parse_sources(value: str) -> list[int]:
    sources: list[int] = []

    for item in value.split(","):
        item = item.strip()

        if not item:
            continue

        try:
            sources.append(int(item))
        except ValueError as exc:
            raise RuntimeError(f"Source channel id must be an integer: {item}") from exc

    if not sources:
        raise RuntimeError("Sources list must not be empty")

    return sources


def load_account_config(index: int) -> AccountConfig:
    return AccountConfig(
        api_id=get_required_int_env(f"API_ID_{index}"),
        api_hash=get_required_env(f"API_HASH_{index}"),
        string_session=get_required_env(f"STRING_SESSION_{index}"),
        target_channel=get_required_int_env(f"TARGET_CHANNEL_{index}"),
        sources=parse_sources(get_required_env(f"SOURCES_{index}")),
    )


accounts = [
    load_account_config(1),
    load_account_config(2),
]
