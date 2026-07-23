from pyrogram import filters
from pyrogram.types import Message, ChatJoinRequest
from pyrogram.enums import ChatMemberStatus
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS

autoapprove_db = mongodb["autoapprove_settings"]


async def is_autoapprove_on(chat_id: int) -> bool:
    doc = await autoapprove_db.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled"))


@app.on_message(filters.command(["autoapprove"]) & filters.group & ~BANNED_USERS)
async def autoapprove_cmd(client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text("❌ ᴀᴅᴍɪɴ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.")
    except Exception:
        return

    args = message.command
    if len(args) < 2 or args[1].lower() not in ["on", "off"]:
        state = await is_autoapprove_on(message.chat.id)
        return await message.reply_text(
            f"🔔 **ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ** — {'✅ ᴏɴ' if state else '❌ ᴏꜰꜰ'}\n\n"
            "Automatically approves all join requests to this group.\n\n"
            "**ᴜsᴀɢᴇ:**\n"
            "• `/autoapprove on` — enable\n"
            "• `/autoapprove off` — disable\n\n"
            "⚠️ Bot must have **Add Members** permission."
        )

    state = args[1].lower() == "on"
    await autoapprove_db.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"chat_id": message.chat.id, "enabled": state}},
        upsert=True,
    )
    if state:
        await message.reply_text(
            "✅ **ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴇɴᴀʙʟᴇᴅ!**\n"
            "All join requests will be automatically approved."
        )
    else:
        await message.reply_text("❌ **ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴅɪsᴀʙʟᴇᴅ.**")


@app.on_chat_join_request(filters.group)
async def auto_approve_handler(client, join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    if not await is_autoapprove_on(chat_id):
        return
    try:
        await client.approve_chat_join_request(chat_id, join_request.from_user.id)
        try:
            await client.send_message(
                join_request.from_user.id,
                f"✅ Your join request for **{join_request.chat.title}** has been approved!\n\n"
                f"Welcome to the group! 🎉",
            )
        except Exception:
            pass
    except Exception:
        pass
