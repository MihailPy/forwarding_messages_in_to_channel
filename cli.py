import asyncio
import json
import os
from pathlib import Path
from typing import Any, cast

import typer
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.table import Table
from telethon import TelegramClient
from telethon.sessions import StringSession

from config import load_accounts
from services.validation import validate_account

app = typer.Typer(help="Manage Telegram forwarding accounts")
console = Console()

CONFIG_PATH = Path("accounts.json")
ENV_PATH = Path(".env")


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

    raise typer.BadParameter(f"Account not found: {name}")


def normalize_env_name(name: str, suffix: str) -> str:
    safe_name = name.upper().replace("-", "_")
    return f"{safe_name}_{suffix}"


def mask_secret(value: str | None) -> str:
    if not value:
        return "[red]missing[/red]"

    if len(value) <= 10:
        return "***"

    return f"{value[:4]}...{value[-4:]}"


def get_env_value(name: str) -> str | None:
    load_dotenv()
    return os.getenv(name)


def parse_channel_input(value: str) -> int | str:
    value = value.strip()

    try:
        return int(value)
    except ValueError:
        return value


@app.command("add-account")
def add_account() -> None:
    config = load_config()

    name = typer.prompt("Account name")

    if any(account["name"] == name for account in config["accounts"]):
        raise typer.BadParameter(f"Account already exists: {name}")

    api_id = typer.prompt("API ID", type=int)
    api_hash = typer.prompt("API Hash", hide_input=True)
    target_channel_raw = typer.prompt("Target channel ID, @username or link")
    target_channel = parse_channel_input(target_channel_raw)

    api_id_env = normalize_env_name(name, "API_ID")
    api_hash_env = normalize_env_name(name, "API_HASH")
    string_session_env = normalize_env_name(name, "STRING_SESSION")

    ENV_PATH.touch(exist_ok=True)
    set_key(str(ENV_PATH), api_id_env, str(api_id))
    set_key(str(ENV_PATH), api_hash_env, api_hash)

    config["accounts"].append(
        {
            "name": name,
            "api_id_env": api_id_env,
            "api_hash_env": api_hash_env,
            "string_session_env": string_session_env,
            "target_channel": target_channel,
            "sources": [],
        }
    )

    save_config(config)

    console.print(f"[green]Added account:[/green] {name}")
    console.print(f"[green]Saved secrets to .env:[/green] {api_id_env}, {api_hash_env}")
    console.print()
    console.print("Now run:")
    console.print(f"[bold]python cli.py login {name} --save[/bold]")


@app.command("login")
def login(
    name: str,
    save: bool = typer.Option(False, "--save", help="Save string session to .env"),
) -> None:
    load_dotenv()

    config = load_config()
    account = find_account(config, name)

    api_id_raw = os.getenv(account["api_id_env"])
    api_hash = os.getenv(account["api_hash_env"])

    if api_id_raw is None:
        raise typer.BadParameter(f"Missing env variable: {account['api_id_env']}")

    if api_hash is None:
        raise typer.BadParameter(f"Missing env variable: {account['api_hash_env']}")

    api_id = int(api_id_raw)

    with TelegramClient(StringSession(), api_id, api_hash) as client:
        string_session = client.session.save()

    if string_session is None:
        raise typer.BadParameter("Failed to create string session")

    if save:
        ENV_PATH.touch(exist_ok=True)
        set_key(str(ENV_PATH), account["string_session_env"], string_session)
        console.print(
            f"[green]Saved string session to .env:[/green] "
            f"{account['string_session_env']}"
        )
    else:
        console.print("[yellow]String session:[/yellow]")
        console.print(string_session)


@app.command("list")
def list_accounts() -> None:
    config = load_config()
    load_dotenv()

    table = Table(title="Forwarding accounts")
    table.add_column("Name")
    table.add_column("API ID")
    table.add_column("API Hash")
    table.add_column("String Session")
    table.add_column("Target")
    table.add_column("Sources")

    for account in config["accounts"]:
        api_id_env = account["api_id_env"]
        api_hash_env = account["api_hash_env"]
        session_env = account["string_session_env"]

        table.add_row(
            account["name"],
            f"{api_id_env}: {mask_secret(get_env_value(api_id_env))}",
            f"{api_hash_env}: {mask_secret(get_env_value(api_hash_env))}",
            f"{session_env}: {mask_secret(get_env_value(session_env))}",
            str(account["target_channel"]),
            "\n".join(str(source) for source in account["sources"]) or "-",
        )

    console.print(table)


@app.command("add-source")
def add_source(name: str, source: str) -> None:
    config = load_config()
    account = find_account(config, name)

    parsed_source = parse_channel_input(source)

    if parsed_source in account["sources"]:
        console.print(f"[yellow]Source already exists:[/yellow] {parsed_source}")
        return

    account["sources"].append(parsed_source)
    save_config(config)

    console.print(
        f"[green]Added source[/green] {parsed_source} [green]to[/green] {name}"
    )


@app.command("remove-source")
def remove_source(name: str, source: str) -> None:
    config = load_config()
    account = find_account(config, name)

    parsed_source = parse_channel_input(source)

    if parsed_source not in account["sources"]:
        console.print(f"[yellow]Source not found:[/yellow] {parsed_source}")
        return

    account["sources"].remove(parsed_source)
    save_config(config)

    console.print(
        f"[green]Removed source[/green] {parsed_source} [green]from[/green] {name}"
    )


@app.command("set-target")
def set_target(name: str, target: str) -> None:
    config = load_config()
    account = find_account(config, name)

    parsed_target = parse_channel_input(target)

    account["target_channel"] = parsed_target
    save_config(config)

    console.print(f"[green]Updated target for[/green] {name}: {parsed_target}")


@app.command("remove-account")
def remove_account(name: str) -> None:
    config = load_config()

    before = len(config["accounts"])
    config["accounts"] = [
        account for account in config["accounts"] if account["name"] != name
    ]

    if len(config["accounts"]) == before:
        raise typer.BadParameter(f"Account not found: {name}")

    save_config(config)

    console.print(f"[green]Removed account from accounts.json:[/green] {name}")
    console.print("[yellow]Note:[/yellow] related values in .env were not removed")


@app.command("check")
def check_config() -> None:
    asyncio.run(run_check())


async def run_check() -> None:
    accounts = load_accounts()

    for account in accounts:
        client = TelegramClient(
            StringSession(account.string_session),
            account.api_id,
            account.api_hash,
        )

        try:
            await cast(Any, client.start())
            await validate_account(client, account)
            console.print("[green]OK[/green]")
        finally:
            await cast(Any, client.disconnect())


if __name__ == "__main__":
    app()
