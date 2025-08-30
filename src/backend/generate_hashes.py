#!/usr/bin/env python3

import bcrypt

passwords = {
    "admin123": "admin",
    "manager123": "manager", 
    "staff123": "staff"
}

for password, user in passwords.items():
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(f"{user}: {hashed.decode('utf-8')}")