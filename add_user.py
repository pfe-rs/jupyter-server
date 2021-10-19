#!/usr/bin/env python
from json import dump, load
from random import randint
from typing import Optional

users: Optional[dict[str, str]] = None

with open('users.json', 'r', encoding='utf-8') as users_file:
    users = load(users_file)

if users is not None:
    while True:
        try:
            username: str = input()
            password: int = randint(1000000000, 9999999999)
            users[username] = str(password)
            with open('users.json', 'w', encoding='utf-8') as users_file:
                dump(users, users_file, indent=4)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
