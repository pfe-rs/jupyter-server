from discord import Client, Intents
from json import load
from time import sleep
from typing import Optional

autodetection_config: Optional[dict[str, str]] = None
users: Optional[list[dict[str, str]]] = None
client = Client(intents=Intents.all())

@client.event
async def on_ready():
    if autodetection_config is None or users is None:
        raise Exception('Autodetection configuration or users not found!')
    print('Logged in to Discord')
    guild = await client.fetch_guild(autodetection_config['guild_id'])
    for user in users:
        if not 'discord_id' in user or not 'notebooks_url' in user:
            continue
        member = await guild.fetch_member(user['discord_id'])
        print('Sending message to', user['name'])
        # We don't want to be detected as a spambot by Discord
        sleep(10)
        await member.send(autodetection_config['notebook_message'].format(**user))
    await client.close()

with open('users.json', 'r', encoding='utf-8') as users_file:
    users = load(users_file)

with open('autodetection.json', 'r', encoding='utf-8') as autodetection_config_file:
    autodetection_config = load(autodetection_config_file)

if autodetection_config is not None:
    client.run(autodetection_config['token'])
