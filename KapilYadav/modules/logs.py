import os
from telethon import events
from config import OWNER_ID, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10

clients = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]

@X1.on(events.NewMessage(pattern=r"^[./!]logs$"))
async def logs_fetch(event):
    if event.sender_id != OWNER_ID:
        return
    
    # चेक करें कि क्या कोई log फाइल मौजूद है
    log_file = "log.txt" 
    if not os.path.exists(log_file):
        # अगर log.txt नहीं है, तो चेक करें क्या Logs.txt है
        if os.path.exists("Logs.txt"):
            log_file = "Logs.txt"
        else:
            return await event.reply("❌ कोई लॉग फाइल (log.txt) नहीं मिली।")

    await event.client.send_file(event.chat_id, log_file, caption="⚡ **Komal Bot Logs**")
            
