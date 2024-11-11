import asyncio
from platform import python_version
from pyrogram import __version__
from tagall import Bot, app
from tagall.config import LOGGER, LOGGER_ID
from pyrogram import idle
from tagall.helpers.tools import checkExpired


loop = asyncio.get_event_loop_policy().get_event_loop()

async def main():
    try:
        await app.start()
        app.me = await app.get_me()
        username = app.me.username
        namebot = app.me.first_name
        log = await app.send_message(LOGGER_ID, "<blockquote><b>Bot sudah aktif Vii</b></blockquote>")
        LOGGER("INFO").info(f"{namebot} | [ @{username} ] | 🔥 Activated! 🔥")
    except Exception as a:
        print(a)
    LOGGER("INFO").info(f"[ BOT TAGALL AKTIF]")
    await checkExpired()
    await idle()


LOGGER("INFO").info("Proses Mengaktifkan Bot Tagall....")
loop.run_until_complete(main())
