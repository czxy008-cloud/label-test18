import bcrypt

password = b"admin123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
print(f"Password: admin123")
print(f"Hash: {hashed.decode('utf-8')}")

verify = bcrypt.checkpw(password, hashed)
print(f"Verify: {verify}")
