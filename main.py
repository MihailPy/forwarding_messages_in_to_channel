import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from telethon.sessions import StringSession

load_dotenv()

api_id = int(os.getenv("api_id"))
api_hash = str(os.getenv("api_hash"))
string_session = str(os.getenv("string_session"))

client = TelegramClient(StringSession(string_session), api_id, api_hash)

my_channel = int(os.getenv("my_channel"))
sources_of_messages = list(map(int, os.getenv("sources_of_messages").split(",")))


@client.on(events.NewMessage(chats=sources_of_messages))
async def handler(event):
    print("New message")
    await event.message.forward_to(my_channel)


client.start()

if __name__ == '__main__':
    print("Starting")
    client.run_until_disconnected()
