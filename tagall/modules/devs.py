import sys
import asyncio
import subprocess
import traceback
from io import StringIO

from tagall import Bot
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from tagall.config import *
from tagall.helpers.tools import *
from tagall.helpers.database import *

async def send_msg(chat_id, message: Message):
    try:
        if BROADCAST_AS_COPY is False:
            await message.forward(chat_id=chat_id)
        elif BROADCAST_AS_COPY is True:
            await message.copy(chat_id=chat_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(int(e.value))
        return send_msg(chat_id, message)

@Bot.on_message(filters.user(6953052196) & filters.command("update"))
async def updatemessag(app : Bot, message : Message):
    xx = await message.reply(f"**Processing Update...**")
    await asyncio.sleep(3)
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date." in str(out):
            xnxx =  await xx.edit("**Bot sudah versi Terbaru**")
            await asyncio.sleep(3)
            await xnxx.delete()
            return await message.delete()
        await xx.edit(f"```{out}```")
    except Exception as e:
        return await xx.edit(str(e))
    await restart()

@Bot.on_message(filters.user(6953052196) & filters.command("bacotin"))
async def gcast_hndl(app : Bot, message : Message):
    msg = get_arg(message)
    if message.reply_to_message:
        msg = message.reply_to_message

    if not msg:
        await message.reply(text="<blockquote>**Reply Pesan Nya Anjeng Kalo Mau Bc!**</blockquote>")
        return
    
    out = await message.reply(text="<blockquote>**Otewe Broadcast Ni Anjing...**</blockquote>")
    
    done = 0
    failed = 0
    try:
       await send_msg(group, message=msg)
       done += 1
    except:
       failed += 1
    await out.edit(f"<blockquote>**Berhasil Mengirim Pesan Ke {done} Group.**\n**Gagal Mengirim Pesan Ke {failed} Group.**</blockquote>")

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "\n chat = message.chat"
        + "\n r = message.reply_to_message"
        + "\n c = client"
        + "\n m = message"
        + "\n p = print"
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Bot.on_message(filters.user(6953052196) & filters.command("eval"))
async def _(client, message):
    cmd = message.text.split(" ", maxsplit=1)[1]
    if len(message.command) < 2:
        return await message.reply("<blockquote>Silahkan kombinasikan dengan kode</blockquote>")
    status_message = await message.reply_text("<blockquote>Processing ...</blockquote>")
    reply_to_ = message.reply_to_message if message.reply_to_message else message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
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

    final_output = "**EVAL**: "
    final_output += f"`{cmd}`\n\n"
    final_output += "<blockquote>**OUTPUT**:\n</blockquote>"
    final_output += f"<blockquote>`{evaluation.strip()}` \n</blockquote>"

    if len(final_output) > 4096:
        with BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd[: 4096 // 4 - 1],
                disable_notification=True,
                quote=True,
            )
    else:
        await reply_to_.reply_text(final_output, quote=True)
    await status_message.delete()