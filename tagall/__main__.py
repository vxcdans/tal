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
        log = await app.send_message(LOGGER_ID, "<blockquote><b>UDAH NYALA GUA JINK</b></blockquote>")
        LOGGER("INFO").info(f"{namebot} | [ @{username} ] | 🔥 MENYALA MEMEK NYA! 🔥")
    except Exception as a:
        print(a)
    LOGGER("INFO").info(f"[ BOT NYA UDAH IDUP YA ANJING JANGAN LUPA MAKASIH KE @Darensupport]")
    await checkExpired()
    await idle()


LOGGER("INFO").info("Otewe Gua Idupin Ni Njing....")
loop.run_until_complete(main())
