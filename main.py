from telethon import TelegramClient, events
from telethon.sessions import StringSession

from config import accounts

clients = []


for account in accounts:
    client = TelegramClient(
        StringSession(account.string_session),
        account.api_id,
        account.api_hash,
    )

    @client.on(events.NewMessage(chats=account.sources))
    async def handler(event, target=account.target_channel):
        print("New message")
        await event.message.forward_to(target)

    clients.append(client)


for client in clients:
    client.start()

for client in clients:
    client.run_until_disconnected()
