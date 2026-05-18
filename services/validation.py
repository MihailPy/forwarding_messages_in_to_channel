from telethon import TelegramClient
from telethon.errors import RPCError

from models.account import AccountConfig


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

    print(f"Account authorized: {me.id}")

    await validate_sources(client, account.sources)
    await validate_target_channel(client, account.target_channel)


async def validate_sources(
    client: TelegramClient,
    sources: list[int],
) -> None:
    for source in sources:
        try:
            entity = await client.get_entity(source)
        except RPCError as exc:
            raise RuntimeError(
                f"Source chat/channel is not available: {source}"
            ) from exc

        print(f"Source available: {source} ({entity.__class__.__name__})")


async def validate_target_channel(
    client: TelegramClient,
    target_channel: int,
) -> None:
    try:
        entity = await client.get_entity(target_channel)
    except RPCError as exc:
        raise RuntimeError(
            f"Target channel is not available: {target_channel}"
        ) from exc

    print(f"Target available: {target_channel} ({entity.__class__.__name__})")
