#!/usr/bin/env python3

import bcrypt

# Test password hashing and verification
password = "admin123"
print(f"Testing password: {password}")

# Generate hash
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(f"Generated hash: {hashed.decode('utf-8')}")

# Test verification
result = bcrypt.checkpw(password.encode('utf-8'), hashed)
print(f"Verification result: {result}")

# Test with database hash
db_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
print(f"Database hash: {db_hash}")

result2 = bcrypt.checkpw(password.encode('utf-8'), db_hash.encode('utf-8'))
print(f"Database verification result: {result2}")