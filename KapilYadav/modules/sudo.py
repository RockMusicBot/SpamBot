
import json
from telethon import events
from config import CMD_HNDLR
from pathlib import Path

SUDO_FILE = Path("KapilYadav/data/sudo_users.json")

def load_sudo_users():
    if SUDO_FILE.exists():
        with open(SUDO_FILE, "r") as f:
            return json.load(f)
    return []

def save_sudo_users(user_ids):
    with open(SUDO_FILE, "w") as f:
        json.dump(user_ids, f)

SUDO_USERS = load_sudo_users()

def is_sudo(user_id):
    return user_id in SUDO_USERS

@events.register(events.NewMessage(pattern=f"\{CMD_HNDLR}sudo(?:\s+(\d+))?$"))
async def add_sudo(event):
    if not event.sender_id in SUDO_USERS:
        return await event.reply("Only sudo users can add others.")
    user_id = event.pattern_match.group(1)
    if not user_id and event.is_reply:
        user_id = (await event.get_reply_message()).sender_id
    elif user_id:
        user_id = int(user_id)
    else:
        return await event.reply("Reply to a user or provide a user ID.")

    if user_id in SUDO_USERS:
        return await event.reply("User is already a sudo.")
    SUDO_USERS.append(user_id)
    save_sudo_users(SUDO_USERS)
    await event.reply(f"Added {user_id} to sudo users.")

@events.register(events.NewMessage(pattern=f"\{CMD_HNDLR}unsudo(?:\s+(\d+))?$"))
async def remove_sudo(event):
    if not event.sender_id in SUDO_USERS:
        return await event.reply("Only sudo users can remove others.")
    user_id = event.pattern_match.group(1)
    if not user_id and event.is_reply:
        user_id = (await event.get_reply_message()).sender_id
    elif user_id:
        user_id = int(user_id)
    else:
        return await event.reply("Reply to a user or provide a user ID.")

    if user_id not in SUDO_USERS:
        return await event.reply("User is not a sudo.")
    SUDO_USERS.remove(user_id)
    save_sudo_users(SUDO_USERS)
    await event.reply(f"Removed {user_id} from sudo users.")
