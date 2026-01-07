import os
import sys
import traceback
import subprocess
from io import StringIO
from datetime import datetime

from telethon import events
from config import X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, SUDO_USERS, CMD_HNDLR as hl

clients = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
OWNER_ID = 8450725193

# टर्मिनल मोड ट्रैक करने के लिए
TERM_MODE = {}

async def aexec(code, event):
    exec(
        "async def __aexec(event): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](event)

for client in clients:
    # --- Eval Command (.eval) ---
    @client.on(events.NewMessage(pattern=fr"^[./?{hl}]eval(?:\s+(.+))?", incoming=True))
    async def eval_handler(event):
        if event.sender_id != OWNER_ID: return
        cmd = event.pattern_match.group(1)
        if not cmd: return await event.reply("<b>Code लिखो मालिक!</b>", parse_mode="html")

        start = datetime.now()
        sys.stdout = redirected_output = StringIO()
sys.stderr = redirected_error = StringIO()

        try:
            await aexec(cmd, event)
        except Exception:
            sys.stderr.write(traceback.format_exc())
        
        stdout, stderr = redirected_output.getvalue(), redirected_error.getvalue()
        sys.stdout, sys.stderr = old_stdout, old_stderr
        evaluation = stderr or stdout or "Success"
        ms = (datetime.now() - start).microseconds / 1000

        await event.reply(f"<b>⥤ RESULT:</b>\n<pre>{evaluation[:4000]}</pre>", parse_mode="html")

    # --- Auto Update (.update) ---
    @client.on(events.NewMessage(pattern=fr"^[./?{hl}]update", incoming=True))
    async def update_handler(event):
        if event.sender_id != OWNER_ID: return
        msg = await event.reply("<code>अप्डेट चेक कर रहा हूँ... 🔄</code>", parse_mode="html")
        try:
            out = subprocess.check_output(["git", "pull"]).decode("utf-8")
            if "Already up to date." in out:
                return await msg.edit("<b>बॉट पहले से ही अपडेटेड है! ✅</b>", parse_mode="html")
            await msg.edit(f"<b>अपडेट मिला!</b>\n<pre>{out}</pre>\n\n<code>बॉट रिस्टार्ट हो रहा है... 🛠</code>", parse_mode="html")
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            await msg.edit(f"<b>Error:</b>\n<pre>{str(e)}</pre>", parse_mode="html")

    # --- Terminal Mode (.terminal) ---
    @client.on(events.NewMessage(pattern=fr"^[./?{hl}]terminal", incoming=True))
    async def terminal_toggle(event):
        if event.sender_id != OWNER_ID: return
        chat_id = event.chat_id
        if chat_id in TERM_MODE:
            del TERM_MODE[chat_id]
            await event.reply("❌ <b>Terminal Mode: OFF</b>", parse_mode="html")
        else:
            TERM_MODE[chat_id] = True
            await event.reply("✅ <b>Terminal Mode: ON</b>", parse_mode="html")

    # --- Shell Handler (.sh) ---
    @client.on(events.NewMessage(incoming=True))
    async def shell_and_term(event):
        if event.sender_id != OWNER_ID: return
        msg_text = event.raw_text
        cmd = None

        if msg_text.startswith(('/', '.', hl)) and (msg_text[1:].startswith('sh ')):
            cmd = msg_text.split(None, 1)[1]
        elif event.chat_id in TERM_MODE and not msg_text.startswith(('/', '.', hl)):
            cmd = msg_text

        if not cmd: return
        
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        output = stdout or stderr or "Done."
        await event.reply(f"<b>OUTPUT:</b>\n<pre>{output[:4000]}</pre>", parse_mode="html")
        
