import json
import os

# ---------------- FILES ----------------
FEEDBACK_FILE = "feedback.json"
MENU_FILE = "menu.json"
USER_FILE = "users.json"

# ---------------- SAFE FILE INITIALIZATION ----------------
def ensure_files():
    """Creates files if they don't exist (IMPORTANT for Streamlit Cloud)"""

    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(MENU_FILE):
        with open(MENU_FILE, "w") as f:
            json.dump({"breakfast": "", "lunch": "", "dinner": ""}, f)

    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)

# Call once at import
ensure_files()

# ---------------- FEEDBACK FUNCTIONS ----------------
def load_data():
    try:
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_feedback(entry):
    data = load_data()
    data.append(entry)
    save_data(data)

# ---------------- MENU FUNCTIONS ----------------
def load_menu():
    try:
        with open(MENU_FILE, "r") as f:
            return json.load(f)
    except:
        return {"breakfast": "", "lunch": "", "dinner": ""}

def save_menu(menu_data):
    with open(MENU_FILE, "w") as f:
        json.dump(menu_data, f, indent=4)

# ---------------- USER FUNCTIONS (optional safety) ----------------
def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)