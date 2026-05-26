import json
from pathlib import Path
from typing import Any

CONFIG_PATH = Path("accounts.json")


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {"accounts": []}

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config: dict[str, Any]) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)


def find_account(config: dict[str, Any], name: str) -> dict[str, Any]:
    for account in config["accounts"]:
        if account["name"] == name:
            return account

    raise ValueError(f"Account not found: {name}")


def parse_channel_input(value: str) -> int | str:
    value = value.strip()

    try:
        return int(value)
    except ValueError:
        return value
