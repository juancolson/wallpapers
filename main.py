from dotenv import load_dotenv
import os
from discord import Client, Intents

# Loading Environment Variables
load_dotenv(override=True)

token = os.getenv("DISCORD_TOKEN")

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'We are logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('hello'):
        print(message)
        await message.channel.send(f'Hello {message.author}')

client.run(token)