import json
import hashlib
import os

FILE = "users.json"

def load_users():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):

    if not username or not password:
        return False

    users = load_users()

    if username in users:
        return False

    users[username] = hash_password(password)
    save_users(users)
    return True

def login(username, password):

    if not username or not password:
        return False

    users = load_users()

    return username in users and users[username] == hash_password(password)