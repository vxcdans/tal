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
            InlineKeyboardButton(text="Owner", url="https://t.me/Darenrorr"),
            InlineKeyboardButton(text="Channel", url="https://t.me/cehadaren")
        ]
    ]
)

inline = InlineKeyboardMarkup(
    [
        [
                    InlineKeyboardButton(text="Support", url="https://t.me/darensupport"),
                    InlineKeyboardButton(text="Channel", url="https://t.me/cehadaren")
        ],
        [
                    InlineKeyboardButton(text="Owner", callback_data = "oner"),
                    InlineKeyboardButton(text="Menu Bantuan", callback_data = "help")
        ],
    ]
)

def add_panel(username):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Tambahkan Ke Group", url=f"http://t.me/{username}?startgroup=appstart")
            ]
        ]
    )

    return button

def admin_panel():
    buttons = [
        [
            InlineKeyboardButton(text="Owner", url=f"http://t.me/Darenrorr")
        ],
    ]

    return buttons

def anjing():
    buttons = [
        [
            InlineKeyboardButton(text="List Bot", callback_data=f"botgua"),
            InlineKeyboardButton(text="Tutup",callback_data=f"balik")
        ],
    ]

    return buttons

def memek():
    buttons = [
        [
            InlineKeyboardButton(text="Tutup", callback_data=f"balik")
        ],
        [
            InlineKeyboardButton(text="Developer", url=f"http://t.me/Darenrorr")
        ],
    ]

    return buttons

def tolol():
    buttons = [
        [
            InlineKeyboardButton(text="Tutup",callback_data=f"balik")
        ],
    ]

    return buttons

@Bot.on_message(filters.command("start"))
async def start_msgmessag(app : Bot, message : Message):
    bot = await app.get_me()
    username = bot.username
    user = message.from_user.mention
    chat_type = message.chat.type
    if chat_type == CTYPE.PRIVATE:
        msg = f"<blockquote>**Woy {user} Jelek!**\n\n**Gua Adalah {username} Bot Yang Di Rancang @Darenrorr Untuk Bisa Mention Member Di Group Lu.\n\nKalo Lu Mau Bot Kaya Gua Buat Aja Sendiri Orang Gua Di Rancang Khusus Buat Gc @differentnih Kok.**</blockquote>"
        try:
            await message.reply(text=msg, reply_markup=inline)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inline)
    elif chat_type in [CTYPE.GROUP, CTYPE.SUPERGROUP]:
        msg = f"<blockquote>**Woy Goblok!**\n\n**Jaadiin Gua Admin Dulu Anjing Kalo Kagak Di Jadiin Admin Mana Bisa Mention Member Di Gruop Jelek Lo Ini😡, Kalo Gatau Cara Gunainnya Banyakin Amal Dulu Lu Kocak\n\nCreated by {OWNER_NAME}**</blockquote>"

        try:
            await message.reply(text=msg, reply_markup=inlinegc)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inlinegc)

@Bot.on_callback_query(filters.regex(r"balik"))
async def balik_cbq(client: Bot, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
        await client.send_message(query.from_user.id, "<blockquote>**ANAK ANJING MALAH CABUT**</blockquote>")
    except:
        pass
    try:
        await query.message.delete()
        await client.send_message(query.from_user.id, "<blockquote>**ANAK ANJING MALAH CABUT**</blockquote>")
    except:
        pass

@Bot.on_callback_query(filters.regex(r"help"))
async def help_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(anjing())
    text = """<blockquote>**Menu Bantuan Bot Tagall Ini**</blockquote>

<blockquote>/tag : **UNTUK MENTION MEMBER LA GOBLOK**

/cancel : **ORANG BEGO JUGA TAU KEGUNAANNYA BUAT STOP MENTION**</blockquote>

<blockquote>**Kepo Amat Lu Kontol Liat Liat Menu Bantuan Gua, Gua Bukan Bot Spesial Kaya Nasi Goreng Yang Banyak Fitur Nya Gua Cuma Bot Tag All Doang Tolol**😡!!</blockquote>"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )

@Bot.on_callback_query(filters.regex(r"oner"))
async def oner_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(memek())
    text = """<blockquote>**WOY ANJING BUTTON DI BAWAH ITU BUAT TAU SIAPA YANG BUAT BOT INI YA KONTOL.\nMINIMAL TERIMA KASIH JUGA KEG TOLOL KARNA UDAH DI BUATIN BOT KEREN KAYAA GUAA ANJAAYYY**</blockquote>"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )

@Bot.on_callback_query(filters.regex(r"botgua"))
async def botgua_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(tolol())
    text = """<blockquote>**List Bot Si Daren**</blockquote>

<blockquote>**Anti Gcast 
@bukanantigcastbot**</blockquote>

<blockquote>**Ai Chatbot 
@jancokchatbot**</blockquote>

<blockquote>**String Session 
@Dareenstringbot**</blockquote>

<blockquote>**Mention/Tagall 
@Differenmentionbot**</blockquote>"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )