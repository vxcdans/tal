from tagall import Bot
from pyrogram import Client, filters
from pyrogram.enums import ParseMode


@Bot.on_message(filters.command('id'))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"<blockquote>**[Message Id:]({message.link})** `{message_id}`\n</blockquote>"
    text += f"<blockquote>**[Your Id:](tg://user?id={your_id})** `{your_id}`\n</blockquote>"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"<blockquote>**[User Id:](tg://user?id={user_id})** `{user_id}`\n</blockquote>"

        except Exception:
            return await message.reply_text("Ga Ada User Nya Tolol.", quote=True)

    text += f"<blockquote>**[Chat Id:](https://t.me/{chat.username})** `{chat.id}`\n\n</blockquote>"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"<blockquote>**[Replied Message Id:]({reply.link})** `{reply.id}`\n<blockquote>"
        text += f"<blockquote>**[Replied User Id:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n</blockquote>"

    if reply and reply.forward_from_chat:
        text += f"The Forwarded Channel, {reply.forward_from_chat.title}, Has An Id Of `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"Id Of The Replied Chat/Channel Is `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )