import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import(InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, Message)
from tagall import Bot
from tagall import *


DAREN = [
"https://graph.org/file/a8f472db59ffc2fa1a10c.jpg"
]


@Bot.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    try:
        chat = message.chat
        for members in message.new_chat_members:
            if members.id == app.id:
                count = await app.get_chat_members_count(chat.id)
                username = message.chat.username if message.chat.username else "Private Group"
                msg = (
                    f"<blockquote>**Bejir Ada #New_Group**\n\n**Chat Name:** {message.chat.title}\n**Chat ID:** {message.chat.id}\n**Chat Username:** @{username}\n**Group Members:** {count}\n**DiTambahkan Oleh:** {message.from_user.mention}</blockquote>"
                )
                await app.send_photo(LOGGER_ID, photo=random.choice(DAREN), caption=msg)
    except:
        pass