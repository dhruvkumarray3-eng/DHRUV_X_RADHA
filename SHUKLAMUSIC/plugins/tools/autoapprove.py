from pyrogram import filters
from pyrogram.types import Message, ChatJoinRequest
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import RPCError
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS
from SHUKLAMUSIC.logging import LOGGER

autoapprove_db = mongodb["autoapprove_settings"]
_LOG = LOGGER(__name__)


async def is_autoapprove_on(chat_id: int) -> bool:
    doc = await autoapprove_db.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled"))


async def _can_approve_requests(client, chat_id: int) -> bool:
    """Return whether the bot has Telegram's required invite permission."""
    bot_id = getattr(client, "id", None)
    if not bot_id:
        bot_id = (await client.get_me()).id
    member = await client.get_chat_member(chat_id, bot_id)
    if member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR):
        privileges = member.privileges
        return member.status == ChatMemberStatus.OWNER or bool(
            privileges and privileges.can_invite_users
        )
    return False


@app.on_message(filters.command(["autoapprove"]) & filters.group & ~BANNED_USERS)
async def autoapprove_cmd(client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text("❌ ᴀᴅᴍɪɴ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.")
    except RPCError as error:
        _LOG.warning("Could not check auto-approve admin in %s: %s", message.chat.id, error)
        return await message.reply_text(
            "❌ I could not verify your admin rights. Please try again."
        )

    args = message.command
    if len(args) < 2 or args[1].lower() not in ["on", "off"]:
        try:
            state = await is_autoapprove_on(message.chat.id)
        except Exception:
            _LOG.exception(
                "Could not read auto-approve setting for %s", message.chat.id
            )
            return await message.reply_text(
                "❌ MongoDB is temporarily unavailable. Please try again shortly."
            )
        return await message.reply_text(
            f"🔔 **ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ** — {'✅ ᴏɴ' if state else '❌ ᴏꜰꜰ'}\n\n"
            "Automatically approves all join requests to this group.\n\n"
            "**ᴜsᴀɢᴇ:**\n"
            "• `/autoapprove on` — enable\n"
            "• `/autoapprove off` — disable\n\n"
            "⚠️ Bot must have **Add Members** permission."
        )

    state = args[1].lower() == "on"
    if state:
        try:
            if not await _can_approve_requests(client, message.chat.id):
                return await message.reply_text(
                    "❌ I need the **Add Members / Invite Users** admin permission "
                    "before auto-approve can be enabled."
                )
        except RPCError as error:
            _LOG.warning(
                "Could not check bot auto-approve permission in %s: %s",
                message.chat.id,
                error,
            )
            return await message.reply_text(
                "❌ I could not check my admin permissions. "
                "Promote me with **Add Members** permission and try again."
            )

    try:
        await autoapprove_db.update_one(
            {"chat_id": message.chat.id},
            {"$set": {"chat_id": message.chat.id, "enabled": state}},
            upsert=True,
        )
    except Exception:
        _LOG.exception(
            "Could not save auto-approve setting for %s", message.chat.id
        )
        return await message.reply_text(
            "❌ MongoDB is temporarily unavailable. The setting was not changed."
        )
    if state:
        await message.reply_text(
            "✅ **ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴇɴᴀʙʟᴇᴅ!**\n"
            "All join requests will be automatically approved."
        )
    else:
        await message.reply_text("❌ **ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴅɪsᴀʙʟᴇᴅ.**")


@app.on_chat_join_request()
async def auto_approve_handler(client, join_request: ChatJoinRequest):
    chat_id = join_request.chat.id
    try:
        enabled = await is_autoapprove_on(chat_id)
    except Exception:
        _LOG.exception("Could not read auto-approve setting for %s", chat_id)
        return
    if not enabled:
        return
    try:
        await client.approve_chat_join_request(chat_id, join_request.from_user.id)
        _LOG.info(
            "Auto-approved join request from %s in %s",
            join_request.from_user.id,
            chat_id,
        )
        try:
            await client.send_message(
                join_request.from_user.id,
                f"✅ Your join request for **{join_request.chat.title}** has been approved!\n\n"
                f"Welcome to the group! 🎉",
            )
        except Exception:
            # Users may have blocked the bot; approval itself already succeeded.
            _LOG.debug("Could not DM approved user %s", join_request.from_user.id)
    except RPCError as error:
        _LOG.warning(
            "Auto-approve failed for %s in %s: %s",
            join_request.from_user.id,
            chat_id,
            error,
        )
