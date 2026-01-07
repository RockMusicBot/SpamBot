import asyncio
import os
from datetime import datetime
from telethon import events
from config import OWNER_ID, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10

# बॉट के असली लॉग्स आमतौर पर इसी फाइल में सेव होते हैं
LOG_FILE = "log.txt" 

clients = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]

for client in clients:
    @client.on(events.NewMessage(pattern=r"\.logs$"))
    async def logs_handler(event):
        if event.sender_id != OWNER_ID:
            return await event.reply("» ꜱᴏʀʀʏ, ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴄᴄᴇꜱꜱ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")

        start = datetime.now()
        fetch = await event.reply("<code>असली लॉग्स इकट्ठा कर रहा हूँ... 🛠</code>", parse_mode="html")

        # चेक करें कि लॉग फाइल मौजूद है या नहीं
        if not os.path.exists(LOG_FILE):
            # अगर फाइल नहीं है, तो खाली फाइल बना दें ताकि एरर न आए
            with open(LOG_FILE, "w") as f:
                f.write("Log file was not found. Created now.")

        try:
            await event.client.send_file(
                event.chat_id,
                LOG_FILE,
                caption=f"⚡ **𝗧𝗵𝗲 𝗞𝗼𝗺𝗮𝗹 𝗕𝗼𝘁𝘀 𝗟𝗼𝗴𝘀** ⚡\n» **Time Taken:** `{(datetime.now() - start).total_seconds()}s`",
                reply_to=event.id
            )
            await fetch.delete()
        except Exception as e:
            await fetch.edit(f"**Error:** `{str(e)}`")
            
