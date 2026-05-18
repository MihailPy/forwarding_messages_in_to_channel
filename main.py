import asyncio
from typing import Any

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from config import accounts
from services.validation import validate_account


async def main() -> None:
    clients: list[TelegramClient] = []

    for account in accounts:
        client = TelegramClient(
            StringSession(account.string_session),
            account.api_id,
            account.api_hash,
        )

        await client.start()
        await validate_account(client, account)

        @client.on(events.NewMessage(chats=account.sources))
        async def handler(event: Any, target: int = account.target_channel) -> None:
            print("New message")
            await event.message.forward_to(target)

        clients.append(client)

    print("Starting")

    await asyncio.gather(*(client.run_until_disconnected() for client in clients))


if __name__ == "__main__":
    asyncio.run(main())
