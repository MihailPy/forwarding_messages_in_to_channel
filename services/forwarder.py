from typing import Any, cast

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from models.account import AccountConfig
from services.validation import validate_account
from utils.logger import logger


async def create_forwarding_client(account: AccountConfig) -> TelegramClient:
    client = TelegramClient(
        StringSession(account.string_session),
        account.api_id,
        account.api_hash,
    )

    await cast(Any, client.start())
    await validate_account(client, account)

    register_forwarding_handler(client, account)

    return client


def register_forwarding_handler(
    client: TelegramClient,
    account: AccountConfig,
) -> None:
    target_channel = account.target_channel

    @client.on(events.NewMessage(chats=account.sources))
    async def handler(event: Any) -> None:
        logger.info("New message received")
        await event.message.forward_to(target_channel)
