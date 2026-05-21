import json
import os
from pathlib import Path
from typing import Any

import typer
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.table import Table
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

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


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise typer.BadParameter(f"Environment variable is missing: {name}")

    return value


@app.command("list")
def list_accounts() -> None:
    config = load_config()

    table = Table(title="Forwarding accounts")
    table.add_column("Name")
    table.add_column("API ID env")
    table.add_column("API Hash env")
    table.add_column("Session env")
    table.add_column("Target")
    table.add_column("Sources")

    for account in config["accounts"]:
        table.add_row(
            account["name"],
            account["api_id_env"],
            account["api_hash_env"],
            account["string_session_env"],
            str(account["target_channel"]),
            "\n".join(str(source) for source in account["sources"]) or "-",
        )

    console.print(table)


@app.command("add-account")
def add_account(
    name: str,
    api_id_env: str = typer.Option(..., help="Env variable name for API ID"),
    api_hash_env: str = typer.Option(..., help="Env variable name for API hash"),
    string_session_env: str = typer.Option(
        ..., help="Env variable name for StringSession"
    ),
    target: int = typer.Option(..., help="Target channel ID"),
) -> None:
    config = load_config()

    if any(account["name"] == name for account in config["accounts"]):
        raise typer.BadParameter(f"Account already exists: {name}")

    config["accounts"].append(
        {
            "name": name,
            "api_id_env": api_id_env,
            "api_hash_env": api_hash_env,
            "string_session_env": string_session_env,
            "target_channel": target,
            "sources": [],
        }
    )

    save_config(config)
    console.print(f"[green]Added account:[/green] {name}")


@app.command("remove-account")
def remove_account(name: str) -> None:
    config = load_config()

    accounts = config["accounts"]
    config["accounts"] = [account for account in accounts if account["name"] != name]

    if len(config["accounts"]) == len(accounts):
        raise typer.BadParameter(f"Account not found: {name}")

    save_config(config)
    console.print(f"[green]Removed account:[/green] {name}")


@app.command("add-source")
def add_source(name: str, source: int) -> None:
    config = load_config()
    account = find_account(config, name)

    if source in account["sources"]:
        console.print(f"[yellow]Source already exists:[/yellow] {source}")
        return

    account["sources"].append(source)
    save_config(config)

    console.print(f"[green]Added source[/green] {source} [green]to[/green] {name}")


@app.command("remove-source")
def remove_source(name: str, source: int) -> None:
    config = load_config()
    account = find_account(config, name)

    if source not in account["sources"]:
        console.print(f"[yellow]Source not found:[/yellow] {source}")
        return

    account["sources"].remove(source)
    save_config(config)

    console.print(f"[green]Removed source[/green] {source} [green]from[/green] {name}")


@app.command("set-target")
def set_target(name: str, target: int) -> None:
    config = load_config()
    account = find_account(config, name)

    account["target_channel"] = target
    save_config(config)

    console.print(f"[green]Updated target for[/green] {name}: {target}")


@app.command("login")
def login(
    name: str,
    save: bool = typer.Option(False, "--save", help="Save string session to .env"),
) -> None:
    load_dotenv()

    config = load_config()
    account = find_account(config, name)

    api_id = int(get_required_env(account["api_id_env"]))
    api_hash = get_required_env(account["api_hash_env"])
    session_env = account["string_session_env"]

    with TelegramClient(StringSession(), api_id, api_hash) as client:
        string_session = client.session.save()

    if string_session is None:
        raise typer.BadParameter("Failed to create string session")

    if save:
        ENV_PATH.touch(exist_ok=True)
        set_key(str(ENV_PATH), session_env, string_session)
        console.print(f"[green]Saved string session to .env:[/green] {session_env}")
    else:
        console.print("[yellow]String session:[/yellow]")
        console.print(string_session)
        console.print()
        console.print("Add it to .env as:")
        console.print(f"{session_env}={string_session}")


if __name__ == "__main__":
    app()
