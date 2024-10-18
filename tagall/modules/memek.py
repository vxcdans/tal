
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from tagall import Bot
from tagall import *
from tagall.config import *
from tagall.helpers.tools import *
from tagall.helpers.database import *

#--------------------------

MUST_JOIN = "cehadaren"
#------------------------
@Bot.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply(text=f"<blockquote><b>Ngapain Jelek Start Gua, Cuman Start Doang Kagak Beli Kontol, Gua Cuman Bot Tag All Doang Ngapain Jamet Kaya Lu Start Gua, Haram Hukum Nya, Btw Kalo Mau Liat Liat Kegunaan Gua Join Dulu Ke Link Dibawah.</b></blockquote>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Masuk Dulu", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"Jadiin Admin Dulu Bego Di Ch yang Mau Di Subs: {MUST_JOIN} !")
