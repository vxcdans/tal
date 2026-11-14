import asyncio
import random
import time

from pyrogram import enums, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from pyrogram.errors import FloodWait

from tagall import Bot

STATUS = enums.ChatMemberStatus
SPAM_CHATS = set()
PENDING_TAGALL = {}
EMOJIS = ["💌", "👻", "🤡"]
TIMER_OPTIONS = (1, 3, 5, 8, 10)


def timer_keyboard(chat_id, user_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{minutes} menit",
                    callback_data=f"tagall_timer:{minutes}:{chat_id}:{user_id}",
                )
                for minutes in TIMER_OPTIONS[:3]
            ],
            [
                InlineKeyboardButton(
                    f"{minutes} menit",
                    callback_data=f"tagall_timer:{minutes}:{chat_id}:{user_id}",
                )
                for minutes in TIMER_OPTIONS[3:]
            ],
        ]
    )


async def is_chat_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (STATUS.OWNER, STATUS.ADMINISTRATOR)
    except Exception:
        return False


@Bot.on_message(filters.command("tagall") & filters.group)
async def tag_all_users(client, message: Message):
    if not message.from_user or not await is_chat_admin(
        client, message.chat.id, message.from_user.id
    ):
        return await message.reply_text("Hanya admin grup yang dapat menggunakan perintah ini.")

    chat_id = message.chat.id
    if chat_id in SPAM_CHATS or chat_id in PENDING_TAGALL:
        return await message.reply_text("Tagall sedang berjalan atau menunggu pilihan timer.")

    replied = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    if not replied and not text:
        return await message.reply_text(
            "Gunakan /tagall diikuti teks, atau balas pesan yang ingin disertakan."
        )

    PENDING_TAGALL[chat_id] = {
        "user_id": message.from_user.id,
        "text": text,
        "reply_id": replied.id if replied else None,
    }
    await message.reply_text(
        "Pilih durasi Tagall. Proses akan berhenti otomatis setelah waktu habis:",
        reply_markup=timer_keyboard(chat_id, message.from_user.id),
    )


@Bot.on_callback_query(filters.regex(r"^tagall_timer:"))
async def start_tagall_timer(client, query):
    try:
        _, minutes, chat_id, user_id = query.data.split(":")
        minutes, chat_id, user_id = int(minutes), int(chat_id), int(user_id)
    except (ValueError, AttributeError):
        return await query.answer("Pilihan timer tidak valid.", show_alert=True)

    if query.message.chat.id != chat_id or query.from_user.id != user_id:
        return await query.answer("Tombol ini bukan untuk Anda.", show_alert=True)

    if not await is_chat_admin(client, chat_id, query.from_user.id):
        PENDING_TAGALL.pop(chat_id, None)
        return await query.answer("Hanya admin grup yang dapat memulai Tagall.", show_alert=True)

    pending = PENDING_TAGALL.pop(chat_id, None)
    if not pending or chat_id in SPAM_CHATS:
        return await query.answer("Permintaan sudah kedaluwarsa atau Tagall sedang berjalan.", show_alert=True)

    SPAM_CHATS.add(chat_id)
    await query.answer(f"Tagall dimulai selama {minutes} menit.")
    await query.message.edit_text(f"Tagall dimulai. Durasi: {minutes} menit.")

    asyncio.create_task(
        run_tagall(
            client,
            chat_id,
            pending["text"],
            pending["reply_id"],
            minutes * 60,
        )
    )


async def run_tagall(client, chat_id, text, reply_id, duration):
    deadline = time.monotonic() + duration
    count = 0
    mentions = []

    try:
        async for member in client.get_chat_members(chat_id):
            if chat_id not in SPAM_CHATS or time.monotonic() >= deadline:
                break
            if not member.user or member.user.is_bot or member.user.is_deleted:
                continue

            name = member.user.first_name or "Pengguna"
            mentions.append(
                f"{random.choice(EMOJIS)} [{name}](tg://user?id={member.user.id})"
            )

            if len(mentions) >= 5:
                body = "\n".join(mentions)
                if text:
                    body = f"<b>{text}</b>\n\n{body}"
                try:
                    if reply_id:
                        await client.send_message(
                            chat_id, body, reply_to_message_id=reply_id
                        )
                    else:
                        await client.send_message(chat_id, body)
                except FloodWait as error:
                    wait_seconds = getattr(error, "value", 1)
                    if time.monotonic() + wait_seconds >= deadline:
                        break
                    await asyncio.sleep(wait_seconds)
                    continue

                count += len(mentions)
                mentions.clear()
                await asyncio.sleep(2)

        if mentions and chat_id in SPAM_CHATS and time.monotonic() < deadline:
            body = "\n".join(mentions)
            if text:
                body = f"<b>{text}</b>\n\n{body}"
            if reply_id:
                await client.send_message(chat_id, body, reply_to_message_id=reply_id)
            else:
                await client.send_message(chat_id, body)
            count += len(mentions)

        if chat_id in SPAM_CHATS:
            await client.send_message(
                chat_id,
                f"Tagall selesai otomatis. Total anggota yang disebut: {count}.",
            )
    except Exception as error:
        await client.send_message(chat_id, f"Tagall dihentikan karena error: {error}")
    finally:
        SPAM_CHATS.discard(chat_id)


@Bot.on_message(filters.command("cancel") & filters.group)
async def untag(client, message: Message):
    if not message.from_user or not await is_chat_admin(
        client, message.chat.id, message.from_user.id
    ):
        return await message.reply_text("Hanya admin grup yang dapat menghentikan Tagall.")

    chat_id = message.chat.id
    PENDING_TAGALL.pop(chat_id, None)
    if chat_id not in SPAM_CHATS:
        return await message.reply_text("Tidak ada proses Tagall yang sedang berjalan.")

    SPAM_CHATS.discard(chat_id)
    return await message.reply_text("Proses Tagall dihentikan.")
