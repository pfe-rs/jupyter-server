#!/usr/bin/env python
from json import dump, load
from os.path import isfile
from random import randint, choice
from typing import Optional
from string import ascii_lowercase, digits


def get_username(name: str) -> str:
    name = name.lower()
    name = name.replace(' ', '-')
    name = name.replace('dž', 'dz')
    name = name.replace('ž', 'z')
    name = name.replace('ć', 'c')
    name = name.replace('č', 'c')
    name = name.replace('š', 's')
    name = name.replace('đ', 'dj')
    return name


users: Optional[list[dict[str, str]]] = None

if isfile('users.json'):
    with open('users.json', 'r', encoding='utf-8') as users_file:
        users = load(users_file)
else:
    users = []

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
    with open('users.json', 'w', encoding='utf-8') as users_file:
        dump(users, users_file, indent=4)
