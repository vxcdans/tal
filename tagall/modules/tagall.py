import random
from asyncio import sleep

import asyncio

from tagall import Bot
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant

from tagall.config import *
from tagall.helpers.tools import *
from tagall.helpers.admins import *
from tagall.helpers.message import *
from tagall.helpers.database import *

STATUS = enums.ChatMemberStatus
SPAM_CHATS = []
emoji = "💌".split(
    " "
)

Admin = filters.create(isAdmin)

@Bot.on_message(filters.command("tag") & filters.group & Admin)
async def tag_all_users(_,message): 
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:
        await message.reply_text("𝘒𝘢𝘴𝘪𝘩 𝘵𝘦𝘹𝘵 𝘯𝘺𝘢 𝘥𝘰𝘯𝘨 𝘴𝘦𝘯𝘨") 
        return                  
    if replied:
        SPAM_CHATS.append(message.chat.id)      
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id): 
            if message.chat.id not in SPAM_CHATS:
                break       
            usernum += 8
            usertxt += f" [{m.user.first_name}](tg://user?id={m.user.id})) "
            if usernum == 1:
                await replied.reply_text(usertxt)
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        text = message.text.split(None, 1)[1]

        SPAM_CHATS.append(message.chat.id)
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):       
            if message.chat.id not in SPAM_CHATS:
                break 
            usernum += 1
            usertxt += f"{random.choice(emoji)} [{m.user.first_name}](tg://user?id={m.user.id})\n"
            if usernum == 5:
                await app.send_message(message.chat.id,f'{text}\n\n{usertxt}\n🛒 @vstreid')
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""                          
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass

@Bot.on_message(filters.command("cancel") & filters.group & Admin)
async def untag(client, message: Message):
    if not message.chat.id in SPAM_CHATS:
        return await message.reply("𝘕𝘨𝘨𝘢 𝘢𝘥𝘢 𝘱𝘳𝘰𝘴𝘦𝘴 𝘵𝘢𝘨𝘢𝘭𝘭𝘢𝘯 𝘯𝘪𝘩")
    else:
        try:
            SPAM_CHATS.remove(message.chat.id)
        except:
            pass
        return await message.reply("𝘗𝘳𝘰𝘴𝘦𝘴 𝘵𝘢𝘨𝘢𝘭𝘭 𝘣𝘦𝘳𝘩𝘦𝘯𝘵𝘪 𝘴𝘦𝘯𝘨")
