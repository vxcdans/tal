import asyncio

from tagall import Bot
from pyrogram import filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from tagall import *
from tagall.config import *
from tagall.helpers.tools import *
from tagall.helpers.database import *


CTYPE = enums.ChatType

# inline buttons
inlinegc = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👨‍💻 Owner", url="https://t.me/viinotpii"),
            InlineKeyboardButton(text="🛒 Store", url="https://t.me/vstreid")
        ]
    ]
)

inline = InlineKeyboardMarkup(
    [
        [
                    InlineKeyboardButton(text="🗳 Support", url="https://t.me/viicombot"),
                    InlineKeyboardButton(text="🛒 Store", url="https://t.me/vstreid")
        ],
        [
                    InlineKeyboardButton(text="👨‍💻 Owner", callback_data = "oner"),
                    InlineKeyboardButton(text="📂 Help Menu", callback_data = "help")
        ],
    ]
)

def add_panel(username):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="💎 Add To Group", url=f"http://t.me/{username}?startgroup=appstart")
            ]
        ]
    )

    return button

def admin_panel():
    buttons = [
        [
            InlineKeyboardButton(text="👨‍💻 Owner", url=f"http://t.me/viinotpii")
        ],
    ]

    return buttons

def anjing():
    buttons = [
        [
            InlineKeyboardButton(text="📋 List Bots", callback_data=f"botgua"),
            InlineKeyboardButton(text="❌ Closed",callback_data=f"balik")
        ],
    ]

    return buttons

def memek():
    buttons = [
        [
            InlineKeyboardButton(text="❌ Closed", callback_data=f"balik")
        ],
        [
            InlineKeyboardButton(text="👨‍💻 Developer", url=f"http://t.me/viinotpii")
        ],
    ]

    return buttons

def tolol():
    buttons = [
        [
            InlineKeyboardButton(text="❌ Closed",callback_data=f"balik")
        ],
    ]

    return buttons

@Bot.on_message(filters.command("start"))
async def start_msgmessag(app : Bot, message : Message):
    bot = await app.get_me()
    username = bot.username
    kontol = message.from_user.id
    user = message.from_user.mention
    log = await app.send_message(LOGGER_ID, f"Hei [Vii](tg://openmessage?user_id=728409811)\n\n {message.from_user.mention} Start your bot.\n\nUser Id: <code>{message.from_user.id}</code>\nUsername : @{message.from_user.username}")
    chat_type = message.chat.type
    if chat_type == CTYPE.PRIVATE:
        msg = f"Hi {user}!**\n\n**@{username} is a bot developed by @viinotpii to be able to mention in your group.\n\nGood luck and always be happy {user}!"
        try:
            await message.reply(text=msg, reply_markup=inline)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inline)
    elif chat_type in [CTYPE.GROUP, CTYPE.SUPERGROUP]:
        msg = f"add me admin access to be able to do your command\n\n#By: {OWNER_NAME}"

        try:
            await message.reply(text=msg, reply_markup=inlinegc)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inlinegc)

@Bot.on_callback_query(filters.regex(r"balik"))
async def balik_cbq(client: Bot, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
        await client.send_message(query.from_user.id, "👋")
    except:
        pass
    try:
        await query.message.delete()
        await client.send_message(query.from_user.id, "👋")
    except:
        pass

@Bot.on_callback_query(filters.regex(r"help"))
async def help_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(anjing())
    text = """**Tagall bot help menu**

/tag : to mention members in your group

/cancel : to cancel mention

just a tagall module,
there's nothing special about this bot,
the special one is you hehe.
If you want to see other bots, just click below.
"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )

@Bot.on_callback_query(filters.regex(r"oner"))
async def oner_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(memek())
    text = """Tuh cek aja siapa yang buat.\nBilang makasih dulu napa jangan main kabur aja"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )

@Bot.on_callback_query(filters.regex(r"botgua"))
async def botgua_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(tolol())
    text = """<blockquote><b>List Bot Vii</b></blockquote>

Anti Gcast 
@AntiBc2Bot

Fsub 
@VxFsubPremBot

Music Manage Bot 
@ViiMusicBot

Mention/Tagall 
@VMentionBot

Userbot 1
@VT_Ubot

Userbot 2
@V1ViiUbot"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )
