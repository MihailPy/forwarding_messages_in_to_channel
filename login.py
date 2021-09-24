import os
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from dotenv import load_dotenv

load_dotenv()

api_id1 = int(os.getenv("api_id1"))
api_hash1 = str(os.getenv("api_hash1"))
with TelegramClient(StringSession(), api_id1, api_hash1) as client:
    print("Скопируйте код 1 сессии")
    print(client.session.save())

api_id2 = int(os.getenv("api_id2"))
api_hash2 = str(os.getenv("api_hash2"))
with TelegramClient(StringSession(), api_id2, api_hash2) as client:
    print("Скопируйте код 2 сессии")
    print(client.session.save())
