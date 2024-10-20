from tagall.helpers.admins import *
from pyrogram import filters
from pyrogram.types import Message
from tagall.helpers.database import impo_off, impo_on, check_pretender, add_userdata, get_userdata, usr_data
from tagall import Bot, app



@Bot.on_message(filters.text & ~filters.private & filters.group, group=34)
async def chk_usr(app: Bot, message: Message):
    if message.sender_chat or not await check_pretender(message.chat.id):
        return
    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    usernamebefore, first_name, lastname_before = await get_userdata(message.from_user.id)
    msg = ""
    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""
**Penyamar Terdeteksi**
**Nama** : {message.from_user.mention}
**User ID** : {message.from_user.id}\n
"""
    if usernamebefore != message.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else "TIDAK ADA USERNAME"
        usernameafter = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "TIDAK ADA USERNAME"
        )
        msg += """
**Mengganti Username**
**Dari** : {bef}
**Ke** : {aft}\n
""".format(bef=usernamebefore, aft=usernameafter)
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if first_name != message.from_user.first_name:
        msg += """
**Mengganti Nama Depan**
**Dari** : {bef}
**Ke** : {aft}\n
""".format(
            bef=first_name, aft=message.from_user.first_name
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if lastname_before != message.from_user.last_name:
        lastname_before = lastname_before or "TIDAK ADA NAMA BELAKANG"
        lastname_after = message.from_user.last_name or "TIDAK ADA NAMA BELAKANG"
        msg += """
**Mengganti Nama Belakang**
**Dari** : {bef}
**Ke** : {aft}\n
""".format(
            bef=lastname_before, aft=lastname_after
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if msg != "":
        await message.reply_photo("https://graph.org/file/a8f472db59ffc2fa1a10c.jpg", caption=msg)

@app.on_message(filters.command("imposter") & filters.group & Admin, group=32)
async def set_mataa(app: Bot, message: Message):
    if len(message.command) == 1:
        return await message.reply("**Penggunaan Deteksi Penyamar: penyamar on|off**")
    if message.command[1] == "on":
        cekset = await impo_on(message.chat.id)
        if cekset:
            await message.reply("**Mode penyamar sudah diaktifkan.**")
        else:
            await impo_on(message.chat.id)
            await message.reply(f"**Berhasil mengaktifkan mode penyamar untuk {message.chat.title}**")
    elif message.command[1] == "off":
        cekset = await impo_off(message.chat.id)
        if not cekset:
            await message.reply("**Mode penyamar sudah dinonaktifkan.**")
        else:
            await impo_off(message.chat.id)
            await message.reply(f"**Berhasil menonaktifkan mode penyamar untuk {message.chat.title}**")
    else:
        await message.reply("**Penggunaan Deteksi Penyamar: penyamar enable|disable**")
