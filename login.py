import os

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.getenv("api_id"))
api_hash = str(os.getenv("api_hash"))
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
