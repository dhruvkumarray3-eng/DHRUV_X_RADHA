from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS

fsub_db = mongodb["fsub_settings"]


async def get_fsub(chat_id: int):
    doc = await fsub_db.find_one({"chat_id": chat_id})
    return (doc.get("channel"), doc.get("channel_username")) if doc else (None, None)


async def is_subscribed(client, user_id: int, channel) -> bool:
    try:
        member = await client.get_chat_member(channel, user_id)
        return member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]
    except Exception:
        return True  # If check fails, don't block


@app.on_message(filters.command(["fsub", "setfsub"]) & filters.group & ~BANNED_USERS)
async def set_fsub_cmd(client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text("❌ ᴀᴅᴍɪɴ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.")
    except Exception:
        return

    if len(message.command) < 2:
        channel, _ = await get_fsub(message.chat.id)
        if channel:
            return await message.reply_text(
                f"📢 **ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴀᴄᴛɪᴠᴇ**\n"
                f"Required channel: `{channel}`\n\n"
                "Use `/fsub off` to disable."
            )
        return await message.reply_text(
            "**📢 ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ sᴇᴛᴜᴘ**\n\n"
            "Users must join your channel before using bot commands in this group.\n\n"
            "**ᴜsᴀɢᴇ:** `/fsub @channel` ᴏʀ `/fsub channel_id`\n"
            "**ᴅɪsᴀʙʟᴇ:** `/fsub off`\n\n"
            "⚠️ Bot must be admin in the channel!"
        )

    arg = message.command[1]
    if arg.lower() == "off":
        await fsub_db.delete_one({"chat_id": message.chat.id})
        return await message.reply_text("✅ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴅɪsᴀʙʟᴇᴅ.")

    try:
        channel_chat = await client.get_chat(arg)
        await fsub_db.update_one(
            {"chat_id": message.chat.id},
            {
                "$set": {
                    "chat_id": message.chat.id,
                    "channel": channel_chat.id,
                    "channel_username": channel_chat.username or str(channel_chat.id),
                    "channel_title": channel_chat.title,
                }
            },
            upsert=True,
        )
        await message.reply_text(
            f"✅ **ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ sᴇᴛ!**\n"
            f"Channel: **{channel_chat.title}**\n\n"
            "Users must join this channel to use bot commands in this group.\n"
            "⚠️ Make sure the bot is an admin in the channel!"
        )
    except Exception as e:
        await message.reply_text(
            f"❌ Error: `{e}`\n\nMake sure the channel exists and the bot is its admin."
        )


@app.on_message(filters.group & ~BANNED_USERS, group=10)
async def fsub_check(client, message: Message):
    """FSub middleware — check subscription before allowing commands."""
    if not message.from_user:
        return
    if not message.text or not message.text.startswith("/"):
        return  # Only check on commands

    channel, channel_username = await get_fsub(message.chat.id)
    if not channel:
        return

    # Admins are exempt
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return
    except Exception:
        return

    if await is_subscribed(client, message.from_user.id, channel):
        return

    try:
        channel_chat = await client.get_chat(channel)
        invite_url = f"https://t.me/{channel_chat.username}" if channel_chat.username else None
        keyboard = (
            InlineKeyboardMarkup([[InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_url)]])
            if invite_url
            else None
        )
        await message.reply_text(
            f"⚠️ {message.from_user.mention}, you must join our channel to use this bot!\n\n"
            f"📢 **Channel:** {channel_chat.title}\n"
            "After joining, try your command again.",
            reply_markup=keyboard,
        )
        message.stop_propagation()
    except Exception:
        pass
