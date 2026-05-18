import os

from dotenv import load_dotenv
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from utils import logger

load_dotenv()

api_id1 = int(os.getenv("api_id1"))
api_hash1 = str(os.getenv("api_hash1"))
with TelegramClient(StringSession(), api_id1, api_hash1) as client:
    logger.info("Скопируйте код 1 сессии")
    logger.info(client.session.save())

api_id2 = int(os.getenv("api_id2"))
api_hash2 = str(os.getenv("api_hash2"))
with TelegramClient(StringSession(), api_id2, api_hash2) as client:
    logger.info("Скопируйте код 2 сессии")
    logger.info(client.session.save())
