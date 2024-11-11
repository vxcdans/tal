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
                    InlineKeyboardButton(text="📂 Menu Bantuan", callback_data = "help")
        ],
    ]
)

def add_panel(username):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="💎 Tambahkan Ke Group", url=f"http://t.me/{username}?startgroup=appstart")
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
            InlineKeyboardButton(text="📋 List Bot", callback_data=f"botgua"),
            InlineKeyboardButton(text="❌ Tutup",callback_data=f"balik")
        ],
    ]

    return buttons

def memek():
    buttons = [
        [
            InlineKeyboardButton(text="❌ Tutup", callback_data=f"balik")
        ],
        [
            InlineKeyboardButton(text="👨‍💻 Developer", url=f"http://t.me/viinotpii")
        ],
    ]

    return buttons

def tolol():
    buttons = [
        [
            InlineKeyboardButton(text="❌ Tutup",callback_data=f"balik")
        ],
    ]

    return buttons

@Bot.on_message(filters.command("start"))
async def start_msgmessag(app : Bot, message : Message):
    bot = await app.get_me()
    username = bot.username
    kontol = message.from_user.id
    user = message.from_user.mention
    log = await app.send_message(LOGGER_ID, f"Liat [sayang](tg://openmessage?user_id=728409811)\n\nSi {message.from_user.mention} Start bot kamu.\n\nUser Id: <code>{message.from_user.id}</code>\nUsername : @{message.from_user.username}")
    chat_type = message.chat.type
    if chat_type == CTYPE.PRIVATE:
        msg = f"Hai {user}!**\n\n**Aku @{username} adalah bot yang dibikin @viinotpii untuk bisa melakukan mention di grup kamu.\n\nSelamat mencoba beb {user}!"
        try:
            await message.reply(text=msg, reply_markup=inline)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inline)
    elif chat_type in [CTYPE.GROUP, CTYPE.SUPERGROUP]:
        msg = f"ihhh ga gitu tau 😡\n\njadiin aku admin dulu beb,kalo ngga dijadiin admin mana bisa mention di grup kamu nah,kalo kamu gatau cara make pc aja {OWNER_NAME}"

        try:
            await message.reply(text=msg, reply_markup=inlinegc)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inlinegc)

@Bot.on_callback_query(filters.regex(r"balik"))
async def balik_cbq(client: Bot, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
        await client.send_message(query.from_user.id, "Ih kamu kemana beb")
    except:
        pass
    try:
        await query.message.delete()
        await client.send_message(query.from_user.id, "Dih malah pergi")
    except:
        pass

@Bot.on_callback_query(filters.regex(r"help"))
async def help_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(anjing())
    text = """**Menu bantuan bot tagall**

/tag : untuk mention member beb

/cancel : untuk membatal mention nya beb

cuma modul tagall doang kok,
gada yang spesial di bot ini,
kan yang spesial itu kamu hehe🥰
kalo mau liat bot lain tuh dibawah klik aja.
"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )

@Bot.on_callback_query(filters.regex(r"oner"))
async def oner_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(memek())
    text = """WOY ANJING BUTTON DI BAWAH ITU BUAT TAU SIAPA YANG BUAT BOT INI YA KONTOL.\nMINIMAL TERIMA KASIH JUGA KEG TOLOL KARNA UDAH DI BUATIN BOT KEREN KAYAA GUAA ANJAAYYY"""
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

Chatbot 
@ViiChtBot

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
