#!/usr/bin/env python
from discord import Client, Intents
from json import dump, load
from os.path import isfile
from random import choice
from typing import Optional
from string import ascii_lowercase, digits

LATIN_TO_CYRILLIC: dict[str, str] = {
    'dž': 'џ',
    'lj': 'љ',
    'nj': 'њ',
    'a': 'а',
    'b': 'б',
    'c': 'ц',
    'č': 'ч',
    'ć': 'ћ',
    'd': 'д',
    'đ': 'ђ',
    'e': 'е',
    'f': 'ф',
    'g': 'г',
    'h': 'х',
    'i': 'и',
    'j': 'ј',
    'k': 'к',
    'l': 'л',
    'm': 'м',
    'n': 'н',
    'o': 'о',
    'p': 'п',
    'r': 'р',
    's': 'с',
    'š': 'ш',
    't': 'т',
    'u': 'у',
    'v': 'в',
    'z': 'з',
    'ž': 'ж'
}

def remove_accent_marks(name: str):
    name = name.replace('dž', 'dz')
    name = name.replace('ž', 'z')
    name = name.replace('ć', 'c')
    name = name.replace('č', 'c')
    name = name.replace('š', 's')
    name = name.replace('đ', 'dj')
    return name

def get_username(name: str) -> str:
    name = name.lower()
    name = name.replace(' ', '-')
    name = remove_accent_marks(name)
    return name

def invert_name(name: str) -> str:
    return ' '.join(name.split(' ')[::-1])

def cyrillify_name(name: str) -> str:
    for latin_letter, cyrillic_letter in LATIN_TO_CYRILLIC.items():
        name = name.replace(latin_letter, cyrillic_letter)
        uppercase_latin = f'{latin_letter[0].upper()}{latin_letter[1:]}'
        name = name.replace(uppercase_latin, cyrillic_letter.upper())
    return name

def name_variants(name: str) -> list[str]:
    return [
        # Petar Petrović
        name,
        # Petrović Petar
        invert_name(name),
        # Petar Petrovic
        remove_accent_marks(name),
        # Petrovic Petar
        invert_name(remove_accent_marks(name)),
        # Петар Петровић
        cyrillify_name(name),
        # Петровић Петар
        invert_name(cyrillify_name(name))
    ]

users: Optional[list[dict[str, str]]] = None
intents = Intents.default()
intents.members = True
autodetection: Client = Client(intents=intents)
autodetection_config: Optional[dict[str, str]] = None

@autodetection.event
async def on_ready():
    global users
    if autodetection_config is None or users is None:
        return
    print('Logged in to Discord')
    guild = await autodetection.fetch_guild(autodetection_config['guild_id'])
    role = guild.get_role(autodetection_config['role_id'])
    async for member in guild.fetch_members():
        if role not in member.roles:
            continue
        found = False
        for user in users:
            variants = [variant.lower() for variant in name_variants(user['name'])]
            if (member.nick is not None and member.nick.lower() in variants) or member.name.lower() in variants:
                user['discord_id'] = member.id
                found = True
                print(f'Found a match for {member.name} ({member.nick}):', user['name'])
                break
        if not found:
            print(f'Match not found for {member.name} ({member.nick})')
    await autodetection.close()

if isfile('users.json'):
    with open('users.json', 'r', encoding='utf-8') as users_file:
        users = load(users_file)
else:
    users = []

if isfile('autodetection.json'):
    with open('autodetection.json', 'r', encoding='utf-8') as autodetection_config_file:
        autodetection_config = load(autodetection_config_file)

if users is not None:
    while True:
        try:
            name: str = input()
            if len(name) == 0 or any(user['name'] == name for user in users):
                continue
            users.append({
                'name': name,
                'username': get_username(name),
                'password': ''.join(choice(ascii_lowercase + digits) for _ in range(8))
            })
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    if autodetection_config is not None:
        autodetection.run(autodetection_config['token'])
    with open('users.json', 'w', encoding='utf-8') as users_file:
        dump(users, users_file, indent=4)
