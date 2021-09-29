import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from telethon.sessions import StringSession

load_dotenv()

api_id1 = int(os.getenv("api_id1"))
api_hash1 = str(os.getenv("api_hash1"))
string_session1 = str(os.getenv("string_session1"))
client1 = TelegramClient(StringSession(string_session1), api_id1, api_hash1)
my_channel1 = int(os.getenv("my_channel1"))
sources_of_messages1 = list(map(int, os.getenv("sources_of_messages1").split(",")))

api_id2 = int(os.getenv("api_id2"))
api_hash2 = str(os.getenv("api_hash2"))
string_session2 = str(os.getenv("string_session2"))
client2 = TelegramClient(StringSession(string_session2), api_id2, api_hash2)
my_channel2 = int(os.getenv("my_channel2"))
sources_of_messages2 = list(map(int, os.getenv("sources_of_messages2").split(",")))


@client1.on(events.NewMessage(chats=sources_of_messages1))
async def handler1(event):
    print("New message")
    await event.message.forward_to(my_channel1)
    await client1.send_read_acknowledge(event.message.peer_id, event.message)


@client2.on(events.NewMessage(chats=sources_of_messages2))
async def handler2(event):
    print("New message")
    await event.message.forward_to(my_channel2)
    await client2.send_read_acknowledge(event.message.peer_id, event.message)


client1.start()
client2.start()

if __name__ == '__main__':
    print("Starting")
    client1.run_until_disconnected()
    client2.run_until_disconnected()
