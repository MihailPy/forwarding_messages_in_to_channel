import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from models.account import AccountConfig

CONFIG_PATH = Path("accounts.json")

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


def load_json_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise RuntimeError(
            "accounts.json not found. Create it with: python cli.py add-account"
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise RuntimeError("accounts.json must contain a JSON object")

    if "accounts" not in data or not isinstance(data["accounts"], list):
        raise RuntimeError("accounts.json must contain an accounts list")

    return data


def parse_account(raw_account: dict[str, Any]) -> AccountConfig:
    name = str(raw_account.get("name", "unknown"))

    api_id_env = str(raw_account.get("api_id_env", ""))
    api_hash_env = str(raw_account.get("api_hash_env", ""))
    string_session_env = str(raw_account.get("string_session_env", ""))

    if not api_id_env:
        raise RuntimeError(f"Missing api_id_env for account: {name}")

    if not api_hash_env:
        raise RuntimeError(f"Missing api_hash_env for account: {name}")

    if not string_session_env:
        raise RuntimeError(f"Missing string_session_env for account: {name}")

    target_channel = raw_account.get("target_channel")
    sources = raw_account.get("sources")

    if not isinstance(target_channel, int):
        raise RuntimeError(f"target_channel must be an integer for account: {name}")

    if not isinstance(sources, list):
        raise RuntimeError(f"sources must be a list for account: {name}")

    parsed_sources: list[int] = []

    for source in sources:
        if not isinstance(source, int):
            raise RuntimeError(
                f"Source channel id must be an integer for account {name}: {source}"
            )

        parsed_sources.append(source)

    if not parsed_sources:
        raise RuntimeError(f"Sources list must not be empty for account: {name}")

    return AccountConfig(
        api_id=get_required_int_env(api_id_env),
        api_hash=get_required_env(api_hash_env),
        string_session=get_required_env(string_session_env),
        target_channel=target_channel,
        sources=parsed_sources,
    )


def load_accounts() -> list[AccountConfig]:
    config = load_json_config()

    return [parse_account(account) for account in config["accounts"]]


accounts = load_accounts()
