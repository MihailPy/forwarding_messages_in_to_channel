import asyncio
from typing import Any, cast

from config import accounts
from services.forwarder import create_forwarding_client
from utils.logger import logger


async def main() -> None:
    clients = [await create_forwarding_client(account) for account in accounts]

    logger.info("Forwarding started")

    await asyncio.gather(
        *(cast(Any, client.run_until_disconnected()) for client in clients)
    )


if __name__ == "__main__":
    asyncio.run(main())
