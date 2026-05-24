from telethon import TelegramClient
from telethon.errors import RPCError

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

    logger.info(f"Account authorized: {me.id}")

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
        entity = await client.get_entity(target_channel)
    except (RPCError, ValueError) as exc:
        raise RuntimeError(
            f"Target channel is not available: {target_channel}. "
            "Check that ID is correct, account has access, "
            "and channel ID uses -100 prefix for channels."
        ) from exc

    logger.info(f"Target available: {target_channel} ({entity.__class__.__name__})")
