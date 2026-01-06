import logging
import os
from telethon import TelegramClient
from os import getenv
from dotenv import load_dotenv
from KapilYadav.data import ALTRON

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

# VALUES REQUIRED FOR BOTS
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

CMD_HNDLR = getenv("CMD_HNDLR", default=".")
hl = CMD_HNDLR  # This fixes the import issue in bot.py

# 🔄 Git & Update Settings

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/XYZ/XYZ")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = os.getenv("GIT_TOKEN", None)
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

# Bot Tokens
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_TOKEN2 = getenv("BOT_TOKEN2")
BOT_TOKEN3 = getenv("BOT_TOKEN3")
BOT_TOKEN4 = getenv("BOT_TOKEN4")
BOT_TOKEN5 = getenv("BOT_TOKEN5")
BOT_TOKEN6 = getenv("BOT_TOKEN6")
BOT_TOKEN7 = getenv("BOT_TOKEN7")
BOT_TOKEN8 = getenv("BOT_TOKEN8")
BOT_TOKEN9 = getenv("BOT_TOKEN9")
BOT_TOKEN10 = getenv("BOT_TOKEN10")

SUDO_USERS = list(map(int, getenv("SUDO_USERS", default="7574330905").split()))
for x in ALTRON:
    SUDO_USERS.append(x)

OWNER_ID = int(getenv("OWNER_ID", default="8450725193"))
SUDO_USERS.append(OWNER_ID)

# ------------- CLIENTS -------------
X1 = TelegramClient('X1', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
X2 = TelegramClient('X2', API_ID, API_HASH).start(bot_token=BOT_TOKEN2)
X3 = TelegramClient('X3', API_ID, API_HASH).start(bot_token=BOT_TOKEN3)
X4 = TelegramClient('X4', API_ID, API_HASH).start(bot_token=BOT_TOKEN4)
X5 = TelegramClient('X5', API_ID, API_HASH).start(bot_token=BOT_TOKEN5)
X6 = TelegramClient('X6', API_ID, API_HASH).start(bot_token=BOT_TOKEN6)
X7 = TelegramClient('X7', API_ID, API_HASH).start(bot_token=BOT_TOKEN7)
X8 = TelegramClient('X8', API_ID, API_HASH).start(bot_token=BOT_TOKEN8)
X9 = TelegramClient('X9', API_ID, API_HASH).start(bot_token=BOT_TOKEN9)
X10 = TelegramClient('X10', API_ID, API_HASH).start(bot_token=BOT_TOKEN10)
