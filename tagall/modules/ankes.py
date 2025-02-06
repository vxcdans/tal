from pyrogram import Client, filters, idle
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import re
import os

from pyrogram.types import EmojiStatus, MessageEntity
from pyrogram import types
from pyrogram.raw.types import ReactionCustomEmoji, ReactionEmoji
from pyrogram.enums import MessageEntityType, ChatType
from pyrogram.raw import functions
from pyrogram.errors.exceptions.bad_request_400 import ReactionInvalid, MessageTooLong

from tagall import Bot
from tagall.config import *
from tagall.helpers.tools import *
from tagall.helpers.admins import *
from tagall.helpers.message import *
from tagall.helpers.database import *

from pyrogram.raw.functions.messages import TranslateText
from tagall.helpers.database import mongo_client
from tagall import *


db = mongo_client["DOR"]
user_collection = db["user_dia"]
gc = db["listgrup"]
psnz = db["msg_text"]

async def get_user_ids(client_id):
    user_ids = await user_collection.find_one({"_id": client_id})
    return user_ids["user_dia"] if user_ids else []

async def get_blacklist_status(client_id):
    blacklist_status = await db.settings.find_one({"_id": client_id})
    return blacklist_status["status"] if blacklist_status else False

async def set_blacklist_status(client_id, status):
    await db.settings.update_one({"_id": client_id}, {"$set": {"status": status}}, upsert=True)

async def get_chat_ids(client_id):
    chat_ids = await gc.find_one({"_id": client_id})
    return chat_ids["grup"] if chat_ids else []

async def get_msg_ids(client_id):
    msg_ids = await psnz.find_one({"_id": client_id})
    return msg_ids["msg_text"] if msg_ids else []

async def purge(message):
    await asyncio.sleep(0.5)
    await message.delete()

def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else ""
        if len(message.command) < 2
        else " ".join(message.command[1:])
    )
    return msg

def emoji(alias):
    emojis = {
        "bintang": "<emoji id=5931592939514892319>⭐</emoji>",
        "loading": "<emoji id=5801044672658805468>✨</emoji>",
        "proses": "<emoji id=6276248783525251352>🔄</emoji>",
        "gagal": "<emoji id=6278161560095426411>❌</emoji>",
        "done": "<emoji id=5852871561983299073>✅</emoji>",
        "upload": "<emoji id=5911100572508885928>♻️</emoji>",
        "roses": "<emoji id=5341312820698948923>🙃</emoji>",
        "selesai": "<emoji id=5341576484446283436>😎</emoji>",
        "on": "<emoji id=6275808772715710450>🎚️</emoji>",
        "off": "<emoji id=6276295366740543459>⛔</emoji>",
        "daftar": "<emoji id=5974045315391556490>📝</emoji>",
    }
    return emojis.get(alias, "Emoji tidak ditemukan.")

Q = emoji("bintang")
gagal = emoji("gagal")
prs = emoji("proses")
batal = emoji("gagal")
rs = emoji("roses")
sls = emoji("selesai")
dn = emoji("done")
on = emoji("on")
off = emoji("off")
dftr = emoji("daftar")

@Bot.on_message(filters.command("piw") & filters.group & Admin)
async def add_user_to_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(f"{batal} <i>gunakan format** : `/piw` **user id atau balas ke pesan untuk menambahkan ke daftar antigcast</i>", quote=True)
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        try:
            user_id = int(m.command[1])
        except ValueError:
            try:
                user = await c.get_users(m.command[1])
                user_id = user.id
            except Exception as e:
                await m.reply_text(f"{gagal} <i>Tidak dapat menemukan pengguna dengan username</i> {m.command[1]}", quote=True)
                return

    user_ids = await get_user_ids(c.me.id)
    if user_id not in user_ids:
        user_ids.append(user_id)
        await user_collection.update_one({"_id": c.me.id}, {"$set": {"user_dia": user_ids}}, upsert=True)
        await m.reply_text(f"<i>user `{user_id}` ditambahkan ke daftar antigcast</i>", quote=True)
    else:
        await m.reply_text(f"<i>user tersebut sudah ada di daftar antigcast</i> {Q}", quote=True)


@Bot.on_message(filters.command("listpiw") & filters.group & Admin)
async def display_blacklist(client, message):
    user_ids = await get_user_ids(client.me.id)
    await message.reply_text(f"{dftr} ini hasilnya : `{user_ids}`\n", quote=True)

@Bot.on_message(filters.command("unpiw") & filters.group & Admin)
async def remove_user_from_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(f"<i>gunakan format : `/unpiw` user id atau balas ke pesan untuk menghapus dari daftar antigcast</i>", quote=True)
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        user_id = int(m.command[1])

    user_ids = await get_user_ids(c.me.id)
    if user_id in user_ids:
        user_ids.remove(user_id)
        await user_collection.update_one({"_id": c.me.id}, {"$set": {"user_dia": user_ids}}, upsert=True)
        await m.reply_text(f"user dengan id `{user_id}` telah dihapus dalam daftar antigcast {dn}", quote=True)
    else:
        await m.reply_text(f"user tersebut tidak ada dalam daftar antigcast {gagal}", quote=True)

@Bot.on_message(filters.command("cek") & filters.group & Admin)
async def checkstatus(client, message):
    cek = await get_blacklist_status(client.me.id)
    if cek == True:
        await message.reply_text(f"<i>Antigcast Aktif</i> {dn}", quote=True)
    else:
        await message.reply_text(f"<i>Antigcast Tidak Aktif</i> {gagal}", quote=True)        

@Bot.on_message(filters.command("on") & filters.group & Admin)
async def enable_blacklist(c, m):
    await set_blacklist_status(c.me.id, True)
    await m.reply_text(f"<i>antigcast di aktifkan</i> {on}", quote=True)

@Bot.on_message(filters.command("off") & filters.group & Admin)
async def disable_blacklist(c, m):
    await set_blacklist_status(c.me.id, False)
    await m.reply_text(f"<i>antigcast di nonaktifkan</i> {off}", quote=True)

@Bot.on_message(filters.command("addgc") & filters.user(OWNER_ID))
async def add_group_to_antigcast(c, m):
    type = (ChatType.GROUP, ChatType.SUPERGROUP)

    if m.chat.type not in type:
        await m.reply_text(f"{gagal} gunakan fitur ini di grup!")
        return

    user_id = m.chat.id
    chat_ids = await get_chat_ids(c.me.id)
    if user_id not in chat_ids:
        chat_ids.append(user_id)
        await gc.update_one({"_id": c.me.id}, {"$set": {"grup": chat_ids}}, upsert=True)
        await m.reply_text(f"<i>grup dengan id `{user_id}` **telah ditambahkan ke daftar antigcast</i> {dn}", quote=True)
    else:
        await m.reply_text(f"<i>grup tersebut sudah ada dalam daftar antigcast</i> {Q}", quote=True)

@Bot.on_message(filters.command("rmgc") & filters.user(OWNER_ID))
async def remove_group_from_antigcast(c, m):
    type = (ChatType.GROUP, ChatType.SUPERGROUP)
    if m.chat.type not in type:
        await m.reply_text(f"{gagal} Gunakan fitur ini di grup atau berikan ID grup", quote=True)
        return

    chat_id = None
    if len(m.command) >= 2:
        try:
            chat_id = int(m.command[1])
        except ValueError:
            await m.reply_text(f"{gagal} ID grup tidak valid", quote=True)
            return

    if not chat_id:
        chat_id = m.chat.id

    chat_ids = await get_chat_ids(c.me.id)
    if chat_id in chat_ids:
        chat_ids.remove(chat_id)
        await gc.update_one({"_id": c.me.id}, {"$set": {"grup": chat_ids}}, upsert=True)
        await m.reply_text(f" Grup dengan ID {chat_id} telah dihapus dari daftar antigcast {dn}", quote=True)
    else:
        await m.reply_text(f" Grup dengan ID {chat_id} tidak ada dalam daftar antigcast {gagal}", quote=True)


@Bot.on_message(filters.command("listgc") & filters.user(OWNER_ID))
async def display_antigcast(c, m):
    user_ids = await get_chat_ids(c.me.id)
    await m.reply_text(f"{dftr} daftar grup antigcast : `{user_ids}` \n", quote=True)



@Bot.on_message(filters.group & ~filters.me, group=75)
async def delete_messages(client, message):
    try:
        chat_ids = await get_chat_ids(client.me.id)
        if message.chat.id not in chat_ids:
            return

        blacklist_status = await get_blacklist_status(client.me.id)
        if not blacklist_status:
            return

        user_ids = await get_user_ids(client.me.id)
        user_msg_patterns = await get_msg_ids(client.me.id)

        if message.from_user.id in user_ids:
            return await message.delete()
        else:
            for pattern in user_msg_patterns:
                if bool(re.search(pattern, message.text)):
                    msg = await message.reply_text(f"<blockquote><b>{dn} <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a> Mampus Goblok Text Lu Masuk Ke Database</b></blockquote>")
                    await asyncio.sleep(1)
                    await msg.delete()
                    return await message.delete()
    except Exception:
        pass
