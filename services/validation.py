from typing import cast

from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.tl.types import TypeInputPeer

from models.account import AccountConfig, ChannelRef
from utils.logger import logger


async def validate_account(
    client: TelegramClient,
    account: AccountConfig,
) -> None:
    try:
        me = await client.get_me()
    except RPCError as exc:
        raise RuntimeError("Failed to authorize Telegram account") from exc

    if me is None:
        raise RuntimeError("Telegram account is not authorized")

    user_id = getattr(me, "id", "unknown")
    logger.info(f"Account authorized: {user_id}")

    await validate_sources(client, account.sources)
    await validate_target_channel(client, account.target_channel)


async def validate_sources(
    client: TelegramClient,
    sources: list[ChannelRef],
) -> None:
    for source in sources:
        try:
            entity = await client.get_entity(source)

        except (RPCError, ValueError) as exc:
            raise RuntimeError(
                f"Source chat/channel is not available: {source}"
            ) from exc

        logger.info(f"Source available: {source} ({entity.__class__.__name__})")


async def validate_target_channel(
    client: TelegramClient,
    target_channel: ChannelRef,
) -> None:
    try:
        entity = await client.get_input_entity(target_channel)
        permissions = await client.get_permissions(
            cast(TypeInputPeer, entity),
            "me",
        )
    except (RPCError, ValueError) as exc:
        raise RuntimeError(
            f"Target channel is not available: {target_channel}"
        ) from exc

    if getattr(permissions, "send_messages", None) is False:
        raise RuntimeError(
            f"Account has no permission to send messages to target: {target_channel}"
        )

    logger.info(f"Target available: {target_channel}")
