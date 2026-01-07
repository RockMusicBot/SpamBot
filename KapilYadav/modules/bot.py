import asyncio
import logging
import sys
import json
import subprocess
from datetime import datetime
from os import execl, _exit

from telethon import events
from config import X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, SUDO_USERS, CMD_HNDLR as hl

logging.basicConfig(level=logging.INFO)
clients = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
CONFIG_FILE = "config_store.json"

try:
    with open(CONFIG_FILE) as f:
        STORED_CONFIG = json.load(f)
except:
    STORED_CONFIG = {}

async def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(STORED_CONFIG, f)

ALIVE_MESSAGE = """💫 **I'm Alive!** 💫

✨ **Bot Status:** Working Fine
⚡ **Powered By:** [𝗧𝗵𝗲 𝗞𝗼𝗺𝗮𝗹 𝗕𝗼𝘁𝘀](https://t.me/TheKomalBots)"""

# --- Command Handlers ---

async def ping_handler(event):
    if event.sender_id in SUDO_USERS:
        start = datetime.now()
        msg = await event.reply("•[ 🍹𝗧𝗵𝗲 𝗞𝗼𝗺𝗮𝗹 𝗕𝗼𝘁𝘀 🍹 ]•")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await msg.edit(f"""[🍹] ᴛʜᴇ ᴋᴏᴍᴀʟ ʙᴏᴛs ᴘαᴘα ɪѕ нєʀє
[🏓] αвє αв тєʀα куα нσgα
[⚡] кιѕкι ᴄнυ∂αι кαʀиι нαι

➜ {ms} ms""")

async def alive_handler(event):
    if event.sender_id in SUDO_USERS:
        await event.reply(ALIVE_MESSAGE)

async def set_alive_handler(event):
    if event.sender_id in SUDO_USERS:
        global ALIVE_MESSAGE
        text = event.raw_text.split(None, 1)
        if len(text) > 1:
            ALIVE_MESSAGE = text[1]
            await event.reply("Alive message updated successfully!")
        else:
            await event.reply("Please provide the new alive message after the command.")

async def reboot_handler(event):
    if event.sender_id in SUDO_USERS:
        await event.reply("""ʀᴇʙᴏᴏᴛ ᴅᴏɴᴇ
[🍷] 2 міιτ ωαιτ ṗℓєαѕє
[🪧] fιʀ ααʏєɢα тєʀɪ мᴀᴀ ᴄнσᴅиє ᴛʜᴇᴋᴏᴍᴀʟʙᴏᴛs ʙᴀʙʏ""")
        for x in clients:
            try:
                await x.disconnect()
            except:
                pass
        execl(sys.executable, sys.executable, *sys.argv)

async def sudo_handler(event):
    if event.sender_id in SUDO_USERS:
        try:
            reply = await event.get_reply_message()
            args = event.pattern_match.group(1)
            if reply:
                target = reply.sender_id
            elif args:
                try:
                    if args.isdigit():
                        target = int(args)
                    else:
                        user = await event.client.get_entity(args)
                        target = user.id
                except ValueError:
                    return await event.reply("Invalid user ID.")
                except Exception as e:
                    return await event.reply(f"Error getting user: {str(e)}")
            else:
                return await event.reply("Reply to a user or provide username/ID.")
            
            if target not in SUDO_USERS:
                SUDO_USERS.append(target)
                await event.reply(f"User {target} added to sudo list.")
            else:
                await event.reply("User is already a sudo user.")
        except Exception as e:
            await event.reply(f"Failed to add sudo: {str(e)}")

async def unsudo_handler(event):
    if event.sender_id in SUDO_USERS:
        try:
            reply = await event.get_reply_message()
            args = event.pattern_match.group(1)
            if reply:
                target = reply.sender_id
            elif args:
                try:
                    if args.isdigit():
                        target = int(args)
                    else:
                        user = await event.client.get_entity(args)
                        target = user.id
                except ValueError:
                    return await event.reply("Invalid user ID.")
                except Exception as e:
                    return await event.reply(f"Error getting user: {str(e)}")
            else:
                return await event.reply("Reply to a user or provide username/ID.")
            
            if target in SUDO_USERS:
                SUDO_USERS.remove(target)
                await event.reply(f"User {target} removed from sudo list.")
            else:
                await event.reply("User is not a sudo user.")
        except Exception as e:
            await event.reply(f"Failed to remove sudo: {str(e)}")

async def sudolist_handler(event):
    if event.sender_id in SUDO_USERS:
        if not SUDO_USERS:
            return await event.reply("No sudo users configured.")
        message = "**🍷 Sudo Users List 🍷**\n\n"
        for user_id in SUDO_USERS:
            try:
                user = await event.client.get_entity(user_id)
                name = f"{user.first_name} {user.last_name or ''}".strip()
                username = f"@{user.username}" if user.username else "No username"
                message += f"• {name} ({username}) - `{user_id}`\n"
            except:
                message += f"• Unknown user - `{user_id}`\n"
        await event.reply(message)

async def logs_handler(event):
    if event.sender_id in SUDO_USERS:
        await event.reply("Sending logs...")
        await event.client.send_file(event.chat_id, "log.txt")

async def set_text_handler(event):
    if event.sender_id in SUDO_USERS:
        cmd = event.pattern_match.group(1)
        text = event.raw_text.split(None, 1)[1] if len(event.raw_text.split(None, 1)) > 1 else None
        if not text:
            return await event.reply("Provide text.")
        STORED_CONFIG[f"{cmd}_{event.chat_id}"] = text
        await save_config()
        await event.reply(f"{cmd} message saved!")

async def echo_handler(event):
    if event.sender_id in SUDO_USERS:
        reply = await event.get_reply_message()
        if reply:
            await event.reply(reply.text)

async def rmecho_handler(event):
    if event.sender_id in SUDO_USERS:
        await event.delete()

async def stopall_handler(event):
    if event.sender_id in SUDO_USERS:
        await event.reply("Stopping all bot processes now.")
        await asyncio.sleep(1)
        _exit(0)

async def speedtest_handler(event):
    if event.sender_id in SUDO_USERS:
        try:
            import speedtest
        except ImportError:
            return await event.reply("Speedtest module not installed. `pip install speedtest-cli`")
        st = speedtest.Speedtest()
        st.get_best_server()
        msg = f"Download: {st.download() / 1024 / 1024:.2f} Mbit/s\nUpload: {st.upload() / 1024 / 1024:.2f} Mbit/s\nPing: {st.results.ping} ms"
        await event.reply(f"**Speedtest Results:**\n{msg}")

# --- Register Commands ---

for client in clients:
    client.add_event_handler(ping_handler, events.NewMessage(pattern=fr"{hl}ping", incoming=True))
    client.add_event_handler(alive_handler, events.NewMessage(pattern=fr"{hl}alive", incoming=True))
    client.add_event_handler(set_alive_handler, events.NewMessage(pattern=fr"{hl}setalive", incoming=True))
    client.add_event_handler(reboot_handler, events.NewMessage(pattern=fr"{hl}reboot", incoming=True))
    client.add_event_handler(sudo_handler, events.NewMessage(pattern=fr"{hl}sudo(?:\s+(.+))?", incoming=True))
    client.add_event_handler(unsudo_handler, events.NewMessage(pattern=fr"{hl}unsudo(?:\s+(.+))?", incoming=True))
    client.add_event_handler(sudolist_handler, events.NewMessage(pattern=fr"{hl}sudolist", incoming=True))
    client.add_event_handler(logs_handler, events.NewMessage(pattern=fr"{hl}logs", incoming=True))
    client.add_event_handler(set_text_handler, events.NewMessage(pattern=fr"{hl}(setleave)(.+)?", incoming=True))
    client.add_event_handler(echo_handler, events.NewMessage(pattern=fr"{hl}echo", incoming=True))
    client.add_event_handler(rmecho_handler, events.NewMessage(pattern=fr"{hl}rmecho", incoming=True))
    client.add_event_handler(stopall_handler, events.NewMessage(pattern=fr"{hl}stopall", incoming=True))
    client.add_event_handler(speedtest_handler, events.NewMessage(pattern=fr"{hl}speedtest", incoming=True))
    
