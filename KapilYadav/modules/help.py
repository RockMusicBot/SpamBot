from telethon import events, Button
import asyncio
import time
from config import X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, SUDO_USERS, CMD_HNDLR as hl

clients = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]

# User data storage with thread-safe approach
user_data = {}  # Format: {user_id: {'theme': 'dark/light', 'last_interaction': timestamp}}

# === Themes ===
def get_help_string(theme="dark"):
    if theme == "light":
        return (
            "<b>╭──『 ⚙️ BOT COMMAND PANEL 』──╮</b>\n"
            "<b>│</b> 🧑‍💻 Owner: <a href='https://t.me/TheKomalBots'>@TheKomalBots</a>\n"
            "<b>│</b> 🛰 Status: <code>Online</code>\n"
            "<b>│</b> 📁 Modules: Admin | Spam | Raid | Dev\n"
            "<b>╰──────────────────────────────╯</b>\n\n"
            "<b>🌐 Select a category below:</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>"
        )
    else:
        return (
            "<b>╔═『 📡 HACKER CONSOLE PANEL 📡 』═╗</b>\n"
            "<b>║</b> 👤 Owner: <a href='https://t.me/TheKomalBots'>@TheKomalBots</a>\n"
            "<b>║</b> 🖥 Status: <code>Active</code>\n"
            "<b>║</b> 🔗 Modules: Admin | 🕶 | 🔒 | 📡\n"
            "<b>╚═════════════════════════════╝</b>\n\n"
            "<b><code>[Select a signal below to continue]</code></b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>"
        )

def get_help_buttons(theme="dark"):
    return [
        [Button.inline("🕶 SPAM", data="spam"), Button.inline("🔒 RAID", data="raid")],
        [Button.inline("👥 ADMIN", data="group"), Button.inline("📡 TOOLS", data="extra")],
        [Button.inline("🌗 Toggle Theme", data="toggle_theme")],
        [Button.url("📢 Updates", "https://t.me/TheKomalBots"),
         Button.url("💬 Support", "https://t.me/KomalBotsupport")]
    ]

# === Modules ===
spam_msg = (
    "<b>╭──『 🕶 SPAM MODULE 』──╮</b>\n"
    f"<b>│ • <code>{hl}spam</code> – Message spam</b>\n"
    f"<b>│ • <code>{hl}pspam</code> – Adult spam</b>\n"
    f"<b>│ • <code>{hl}hang</code> – Freeze spam</b>\n"
    "<b>╰────────────────────────╯</b>"
)

raid_msg = (
    "<b>╭──『 🔒 RAID MODULE 』──╮</b>\n"
    f"<b>│ • <code>{hl}raid</code> – Start raid</b>\n"
    f"<b>│ • <code>{hl}rraid</code> – Reply raid</b>\n"
    f"<b>│ • <code>{hl}drraid</code> – Direct reply</b>\n"
    f"<b>│ • <code>{hl}mraid</code> – Multi-target</b>\n"
    f"<b>│ • <code>{hl}sraid</code> – Super raid</b>\n"
    f"<b>│ • <code>{hl}craid</code> – Combo</b>\n"
    "<b>╰────────────────────────╯</b>"
)

group_msg = (
    "<b>╭──『 👥 ADMIN PANEL 』──╮</b>\n"
    f"<b>│ • <code>{hl}sh update</code> / <code>{hl}update the bot</code></b>\n"
    f"<b>│ • <code>{hl}sh git pull</code> / <code>{hl}update the bot</code></b>\n"
    f"<b>│ • <code>{hl}sh uptime</code> / <code>{hl}uptime of bot</code></b>\n"
    f"<b>│ • <code>{hl}sh speedtest</code> / <code>{hl}speed of bot</code></b>\n"
    f"<b>│ • <code>{hl}🌝</code> / <code>{hl}🌝</code></b>\n"
    f"<b>│ • <code>{hl}❤️</code> / <code>{hl}❤️</code></b>\n"
    "<b>╰────────────────────────╯</b>"
)

extra_msg = (
    "<b>╭──『 📡 DEV & EXTRA 』──╮</b>\n"
    f"<b>│ • <code>{hl}ping</code> – Test latency</b>\n"
    f"<b>│ • <code>{hl}reboot</code> – Restart</b>\n"
    f"<b>│ • <code>{hl}sudo</code> – Add sudo</b>\n"
    f"<b>│ • <code>{hl}logs</code> – Logs dump</b>\n"
    f"<b>│ • <code>{hl}alive</code> – Check alive</b>\n"
    f"<b>│ • <code>{hl}echo</code> / <code>{hl}rmecho</code></b>\n"
    f"<b>│ • <code>{hl}leave</code> – Exit group</b>\n"
    "<b>╰────────────────────────╯</b>"
)

async def help_handler(event):
    uid = event.sender_id
    if uid not in SUDO_USERS:
        return await event.delete()

    # Initialize user data if not exists
    if uid not in user_data:
        user_data[uid] = {'theme': 'dark', 'last_interaction': time.time()}
    else:
        user_data[uid]['last_interaction'] = time.time()
    
    theme = user_data[uid]['theme']
    
    try:
        loading_msg = await event.reply("<b>🔌 Connecting to Bot Kernel...</b>", parse_mode="html")
        
        # Efficient loading animation
        for i in range(1, 11):
            progress = "█" * i + "░" * (10 - i)
            await loading_msg.edit(
                f"<b>🔌 Connecting to Bot Kernel...</b>\n<b>Loading [{progress}] {i*10}%</b>",
                parse_mode="html"
            )
            await asyncio.sleep(0.1)
        
        await loading_msg.edit(
            get_help_string(theme),
            buttons=get_help_buttons(theme),
            parse_mode="html"
        )
    except Exception as e:
        print(f"Error in help handler: {e}")
        await event.respond("⚠️ An error occurred. Please try again.")

async def button_callback(event):
    uid = event.query.user_id
    if uid not in SUDO_USERS:
        return await event.answer("⛔ Access Denied", alert=True)
    
    # Update last interaction time using current timestamp
    if uid not in user_data:
        user_data[uid] = {'theme': 'dark'}
    user_data[uid]['last_interaction'] = time.time()
    
    data = event.data.decode('utf-8')
    theme = user_data[uid]['theme']
    
    try:
        if data == "toggle_theme":
            # Toggle theme
            new_theme = 'light' if theme == 'dark' else 'dark'
            user_data[uid]['theme'] = new_theme
            await event.edit(
                get_help_string(new_theme),
                buttons=get_help_buttons(new_theme),
                parse_mode="html"
            )
        elif data == "help_back":
            await event.edit(
                get_help_string(theme),
                buttons=get_help_buttons(theme),
                parse_mode="html"
            )
        elif data == "spam":
            await event.edit(spam_msg, buttons=[[Button.inline("🔙 Return", data="help_back")]], parse_mode="html")
        elif data == "raid":
            await event.edit(raid_msg, buttons=[[Button.inline("🔙 Return", data="help_back")]], parse_mode="html")
        elif data == "group":
            await event.edit(group_msg, buttons=[[Button.inline("🔙 Return", data="help_back")]], parse_mode="html")
        elif data == "extra":
            await event.edit(extra_msg, buttons=[[Button.inline("🔙 Return", data="help_back")]], parse_mode="html")
    except Exception as e:
        print(f"Error in button callback: {e}")
        await event.answer("⚠️ An error occurred. Please try again.", alert=True)

# === Register Handlers ===
def register_handlers(client):
    client.add_event_handler(
        help_handler,
        events.NewMessage(pattern=fr"\{hl}help(?: |$)(.*)", forwards=False)
    )
    client.add_event_handler(
        button_callback,
        events.CallbackQuery()
    )

# Register for all clients
for client in clients:
    register_handlers(client)

# Cleanup old user data periodically
async def cleanup_user_data():
    while True:
        await asyncio.sleep(3600)  # Cleanup every hour
        current_time = time.time()
        stale_users = [uid for uid, data in user_data.items() 
                      if current_time - data.get('last_interaction', 0) > 86400]  # 24 hours
        for uid in stale_users:
            del user_data[uid]

# Start cleanup task
for client in clients:
    client.loop.create_task(cleanup_user_data())
