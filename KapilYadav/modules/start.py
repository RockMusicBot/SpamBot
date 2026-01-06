from telethon import events, Button, __version__  # Import __version__ directly
from config import X1, X2, X3, X4, X5, X6, X7, X8, X9, X10

START_BUTTON = [
    [
        Button.inline("• ᴄᴏᴍᴍᴀɴᴅs •", data="help_back")
    ],
    [
        Button.url("• ᴄʜᴀɴɴᴇʟ •", "https://t.me/TheKomalBots"),
        Button.url("• sᴜᴘᴘᴏʀᴛ •", "https://t.me/KomalBotSupport")
    ],
    [
        Button.url("• ʀᴇᴘᴏ •", "https://files.catbox.moe/2d32oj.mp4")
    ]
]

@X1.on(events.NewMessage(pattern="/start"))
@X2.on(events.NewMessage(pattern="/start"))
@X3.on(events.NewMessage(pattern="/start"))
@X4.on(events.NewMessage(pattern="/start"))
@X5.on(events.NewMessage(pattern="/start"))
@X6.on(events.NewMessage(pattern="/start"))
@X7.on(events.NewMessage(pattern="/start"))
@X8.on(events.NewMessage(pattern="/start"))
@X9.on(events.NewMessage(pattern="/start"))
@X10.on(events.NewMessage(pattern="/start"))
async def start(event):              
    if event.is_private:
        AltBot = await event.client.get_me()
        bot_name = AltBot.first_name
        bot_id = AltBot.id
        TEXT = f"ʜᴇʏ [{event.sender.first_name}](tg://user?id={event.sender.id}),\n\nɪ ᴀᴍ [{bot_name}](tg://user?id={bot_id})\n━━━━━━━━━━━━━━━━━━━\n\n"
        TEXT += f"» ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [𝗧𝗵𝗲 𝗞𝗼𝗺𝗮𝗹 𝗕𝗼𝘁𝘀](https://t.me/TheKomalBots)\n\n"
        TEXT += f"» Spam ʙᴏᴛꜱ ᴠᴇʀsɪᴏɴ : K3.3\n"
        TEXT += f"» ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : 3.11.3\n"
        TEXT += f"» ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : {__version__}\n━━━━━━━━━━━━━━━━━"
        await event.client.send_file(
            event.chat_id,
            "https://files.catbox.moe/lg4old.jpg",
            caption=TEXT, 
            buttons=START_BUTTON
        )
