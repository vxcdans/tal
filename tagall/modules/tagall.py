import asyncio
import time
import html

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
RUN_INFO = {}
TIMER_OPTIONS = (1, 3, 5, 10, 30, 60)

CHANNEL_URL = "https://t.me/fvckdans"
FORCE_JOIN_CHANNEL = "@odistupa"
FORCE_JOIN_URL = "https://t.me/odistupa"
FOOTER = "✨ Powered by : fvckdante"


def timer_keyboard(chat_id, user_id):
    def button(minutes):
        return InlineKeyboardButton(
            f"{minutes} menit",
            callback_data=f"tagall_timer:{minutes}:{chat_id}:{user_id}",
        )

    return InlineKeyboardMarkup([
        [button(1), button(3)],
        [button(5), button(10)],
        [button(30), button(60)],
        [InlineKeyboardButton(
            "∞ Selamanya",
            callback_data=f"tagall_timer:forever:{chat_id}:{user_id}",
        )],
        [InlineKeyboardButton(
            "🚫 Batal",
            callback_data=f"tagall_cancel:{chat_id}:{user_id}",
        )],
    ])


def tag_keyboard(chat_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("BUKA CHANNEL", url=CHANNEL_URL)],
        [InlineKeyboardButton(
            "🛑 Stop Tag",
            callback_data=f"tagall_stop:{chat_id}",
        )],
    ])


def force_join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("JOIN CHANNEL", url=FORCE_JOIN_URL)],
        [InlineKeyboardButton("CEK JOIN", callback_data="forcejoin_check")],
    ])


async def is_force_joined(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        if member.status == STATUS.RESTRICTED:
            return bool(getattr(member, "is_member", False))
        return member.status in (STATUS.OWNER, STATUS.ADMINISTRATOR, STATUS.MEMBER)
    except Exception:
        return False


@Bot.on_callback_query(filters.regex(r"^forcejoin_check$"))
async def forcejoin_check_callback(client, query):
    if await is_force_joined(client, query.from_user.id):
        await query.answer("Verifikasi berhasil! Kamu sudah bisa menggunakan bot.", show_alert=True)
    else:
        await query.answer("Kamu belum bergabung ke @odistupa. Silakan join terlebih dahulu.", show_alert=True)


def report_keyboard(chat_id):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "🗑 Hapus Tag",
            callback_data=f"tagall_delete:{chat_id}",
        )
    ]])


async def is_chat_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (STATUS.OWNER, STATUS.ADMINISTRATOR)
    except Exception:
        return False


async def delete_tag_messages(client, chat_id, message_ids):
    for message_id in message_ids:
        try:
            await client.delete_messages(chat_id, message_id)
        except Exception:
            pass


async def auto_delete(client, chat_id):
    await asyncio.sleep(60)
    info = RUN_INFO.pop(chat_id, None)
    if info:
        await delete_tag_messages(client, chat_id, info["messages"])


@Bot.on_message(filters.command("utag") & filters.group)
async def tag_all_users(client, message: Message):
    if not message.from_user:
        return
    if not await is_force_joined(client, message.from_user.id):
        return await message.reply_text(
            "Untuk menggunakan bot, kamu wajib bergabung ke channel @odistupa terlebih dahulu.",
            reply_markup=force_join_keyboard(),
        )
    if not await is_chat_admin(
        client, message.chat.id, message.from_user.id
    ):
        return await message.reply_text(
            "Hanya admin grup yang dapat menggunakan perintah ini."
        )

    chat_id = message.chat.id

    if chat_id in SPAM_CHATS or chat_id in PENDING_TAGALL:
        return await message.reply_text(
            "Tagall sedang berjalan atau menunggu pilihan timer."
        )

    replied = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not replied and not text:
        return await message.reply_text(
            "Gunakan /utag diikuti teks, atau balas pesan yang ingin disertakan."
        )

    PENDING_TAGALL[chat_id] = {
        "user_id": message.from_user.id,
        "admin_name": message.from_user.first_name or "Admin",
        "text": text,
        "reply_id": replied.id if replied else None,
    }

    await message.reply_text(
        "Pilih durasi Tagall:",
        reply_markup=timer_keyboard(chat_id, message.from_user.id),
    )


@Bot.on_callback_query(filters.regex(r"^tagall_cancel:"))
async def cancel_tagall_timer(client, query):
    try:
        _, chat_id, user_id = query.data.split(":")
        chat_id, user_id = int(chat_id), int(user_id)
    except (ValueError, AttributeError):
        return await query.answer("Tombol tidak valid.", show_alert=True)

    if query.message.chat.id != chat_id or query.from_user.id != user_id:
        return await query.answer("Tombol ini bukan untuk Anda.", show_alert=True)

    if not await is_chat_admin(client, chat_id, query.from_user.id):
        return await query.answer("Hanya admin yang dapat membatalkan.", show_alert=True)

    if PENDING_TAGALL.pop(chat_id, None) is None:
        return await query.answer("Pilihan timer sudah kedaluwarsa.", show_alert=True)

    await query.answer("Pilihan timer dibatalkan.")
    await query.message.edit_text("Pilihan timer Tagall dibatalkan.")


@Bot.on_callback_query(filters.regex(r"^tagall_timer:"))
async def start_tagall_timer(client, query):
    try:
        _, selected, chat_id, user_id = query.data.split(":")
        chat_id, user_id = int(chat_id), int(user_id)
        duration = None if selected == "forever" else int(selected) * 60
    except (ValueError, AttributeError):
        return await query.answer("Pilihan timer tidak valid.", show_alert=True)

    if query.message.chat.id != chat_id or query.from_user.id != user_id:
        return await query.answer("Tombol ini bukan untuk Anda.", show_alert=True)

    if not await is_chat_admin(client, chat_id, query.from_user.id):
        PENDING_TAGALL.pop(chat_id, None)
        return await query.answer("Hanya admin grup yang dapat memulai Tagall.", show_alert=True)

    pending = PENDING_TAGALL.pop(chat_id, None)
    if not pending or chat_id in SPAM_CHATS:
        return await query.answer("Permintaan kedaluwarsa atau Tagall sedang berjalan.", show_alert=True)

    SPAM_CHATS.add(chat_id)
    label = "Selamanya" if duration is None else f"{selected} menit"

    RUN_INFO[chat_id] = {
        "started": time.monotonic(),
        "duration": label,
        "admin": pending["admin_name"],
        "messages": [],
    }

    await query.answer(f"Tagall dimulai: {label}.")
    await query.message.edit_text(f"Tagall dimulai. Durasi: {label}.")

    asyncio.create_task(
        run_tagall(
            client,
            chat_id,
            pending["text"],
            pending["reply_id"],
            duration,
        )
    )


async def run_tagall(client, chat_id, text, reply_id, duration):
    deadline = None if duration is None else time.monotonic() + duration
    count = 0
    mentions = []

    try:
        chat = await client.get_chat(chat_id)
        group_name = html.escape(chat.title or "Grup")
        safe_text = html.escape(text) if text else None

        async for member in client.get_chat_members(chat_id):
            if chat_id not in SPAM_CHATS:
                break

            if deadline is not None and time.monotonic() >= deadline:
                break

            if not member.user or member.user.is_bot or member.user.is_deleted:
                continue

            mentions.append(
                f'<a href="tg://user?id={member.user.id}">🕳️</a>'
            )

            if len(mentions) >= 5:
                body = f"📢 <b>{group_name}</b>"

                if safe_text:
                    body += f"\n\n{safe_text}"

                body += "\n\n" + " , ".join(mentions)
                body += '\n\n✨ Powered by : <a href="https://t.me/fvckdans">fvckdante</a>'

                try:
                    sent = await client.send_message(
                        chat_id,
                        body,
                        reply_to_message_id=reply_id,
                        reply_markup=tag_keyboard(chat_id),
                        parse_mode=enums.ParseMode.HTML,
                        disable_web_page_preview=False,
                    )
                except FloodWait as error:
                    wait_seconds = getattr(error, "value", 1)
                    if deadline is not None and time.monotonic() + wait_seconds >= deadline:
                        break
                    await asyncio.sleep(wait_seconds)
                    continue

                RUN_INFO[chat_id]["messages"].append(sent.id)
                count += len(mentions)
                mentions.clear()
                await asyncio.sleep(2)

        if mentions and chat_id in SPAM_CHATS:
            body = f"📢 <b>{group_name}</b>"

            if safe_text:
                body += f"\n\n{safe_text}"

            body += "\n\n" + " , ".join(mentions)
            body += '\n\n✨ Powered by : <a href="https://t.me/fvckdans">fvckdante</a>'

            sent = await client.send_message(
                chat_id,
                body,
                reply_to_message_id=reply_id,
                reply_markup=tag_keyboard(chat_id),
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=False,
            )

            RUN_INFO[chat_id]["messages"].append(sent.id)
            count += len(mentions)

    except Exception as error:
        print(f"Tagall error: {error}")

    finally:
        SPAM_CHATS.discard(chat_id)

        info = RUN_INFO.get(chat_id)

        if info:
            elapsed = int(time.monotonic() - info["started"])
            minutes, seconds = divmod(elapsed, 60)

            report = (
                "🛑 <b>TagAll dihentikan!</b>\n\n"
                f"⏱ Durasi pilihan: <b>{info['duration']}</b>\n"
                f"⌛ Waktu berjalan: <b>{minutes} menit {seconds} detik</b>\n"
                f"👤 Admin: <b>{html.escape(info['admin'])}</b>\n"
                f"👥 Total disebut: <b>{count}</b>\n\n"
                f"{FOOTER}\n\n"
                "Pesan TagAll dan laporan akan dihapus otomatis dalam 1 menit."
            )

            try:
                report_message = await client.send_message(
                    chat_id,
                    report,
                    reply_markup=report_keyboard(chat_id),
                    parse_mode=enums.ParseMode.HTML,
                )
                info["messages"].append(report_message.id)
                asyncio.create_task(auto_delete(client, chat_id))
            except Exception as error:
                print(f"Tagall report error: {error}")
                RUN_INFO.pop(chat_id, None)


@Bot.on_callback_query(filters.regex(r"^tagall_stop:"))
async def stop_tagall_button(client, query):
    try:
        chat_id = int(query.data.split(":")[1])
    except (ValueError, IndexError):
        return await query.answer("Tombol tidak valid.", show_alert=True)

    if query.message.chat.id != chat_id:
        return await query.answer("Tombol tidak valid.", show_alert=True)

    if not await is_chat_admin(client, chat_id, query.from_user.id):
        return await query.answer("Hanya admin yang dapat menghentikan Tagall.", show_alert=True)

    if chat_id not in SPAM_CHATS:
        return await query.answer("Tagall sudah berhenti.", show_alert=True)

    SPAM_CHATS.discard(chat_id)
    await query.answer("Tagall dihentikan.")


@Bot.on_callback_query(filters.regex(r"^tagall_delete:"))
async def delete_tagall_button(client, query):
    try:
        chat_id = int(query.data.split(":")[1])
    except (ValueError, IndexError):
        return await query.answer("Tombol tidak valid.", show_alert=True)

    if query.message.chat.id != chat_id:
        return await query.answer("Tombol tidak valid.", show_alert=True)

    if not await is_chat_admin(client, chat_id, query.from_user.id):
        return await query.answer("Hanya admin yang dapat menghapus laporan.", show_alert=True)

    info = RUN_INFO.pop(chat_id, None)
    await query.answer("Pesan TagAll dihapus.")

    if info:
        await delete_tag_messages(client, chat_id, info["messages"])
    else:
        try:
            await query.message.delete()
        except Exception:
            pass


@Bot.on_message(filters.command("cancel") & filters.group)
async def untag(client, message: Message):
    if not message.from_user or not await is_chat_admin(
        client, message.chat.id, message.from_user.id
    ):
        return await message.reply_text(
            "Hanya admin grup yang dapat menghentikan Tagall."
        )

    chat_id = message.chat.id
    PENDING_TAGALL.pop(chat_id, None)

    if chat_id not in SPAM_CHATS:
        return await message.reply_text(
            "Tidak ada proses Tagall yang sedang berjalan."
        )

    SPAM_CHATS.discard(chat_id)
    await message.reply_text("Proses Tagall dihentikan.")
