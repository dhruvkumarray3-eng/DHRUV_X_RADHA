import time
import datetime
from collections import defaultdict
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.enums import ChatMemberStatus
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS

guardian_db = mongodb["guardian_settings"]

# In-memory flood tracking: {chat_id: {user_id: [timestamps]}}
flood_tracker: dict = defaultdict(lambda: defaultdict(list))

FLOOD_LIMIT = 5    # messages
FLOOD_TIME = 5     # seconds window
MUTE_DURATION = 300  # 5 min mute


async def is_guardian_enabled(chat_id: int) -> bool:
    doc = await guardian_db.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled"))


async def is_admin(client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    except Exception:
        return False


@app.on_message(filters.command(["guardian"]) & filters.group & ~BANNED_USERS)
async def guardian_cmd(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ ᴀᴅᴍɪɴ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.")

    args = message.command
    if len(args) < 2 or args[1].lower() not in ["on", "off"]:
        doc = await guardian_db.find_one({"chat_id": message.chat.id})
        status = "✅ ᴏɴ" if (doc and doc.get("enabled")) else "❌ ᴏꜰꜰ"
        return await message.reply_text(
            f"🛡️ **ɢᴜᴀʀᴅɪᴀɴ ᴍᴏᴅᴇ** — {status}\n\n"
            "Auto-mutes users who flood messages.\n\n"
            f"• Limit: **{FLOOD_LIMIT}** messages in **{FLOOD_TIME}s** → mute **{MUTE_DURATION // 60} min**\n\n"
            "**ᴜsᴀɢᴇ:**\n"
            "• `/guardian on` — enable\n"
            "• `/guardian off` — disable\n\n"
            "⚠️ Admins are never muted."
        )

    state = args[1].lower() == "on"
    await guardian_db.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"chat_id": message.chat.id, "enabled": state}},
        upsert=True,
    )
    if state:
        await message.reply_text(
            "🛡️ **ɢᴜᴀʀᴅɪᴀɴ ᴍᴏᴅᴇ ᴇɴᴀʙʟᴇᴅ!**\n"
            "Flood protection is now active."
        )
    else:
        await message.reply_text("❌ **ɢᴜᴀʀᴅɪᴀɴ ᴍᴏᴅᴇ ᴅɪsᴀʙʟᴇᴅ.**")


@app.on_message(filters.group & ~filters.bot & ~BANNED_USERS, group=5)
async def guardian_flood_check(client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_guardian_enabled(chat_id):
        return
    if await is_admin(client, chat_id, user_id):
        return

    now = time.time()
    # Keep only timestamps within the window
    flood_tracker[chat_id][user_id] = [
        t for t in flood_tracker[chat_id][user_id] if now - t < FLOOD_TIME
    ]
    flood_tracker[chat_id][user_id].append(now)

    if len(flood_tracker[chat_id][user_id]) >= FLOOD_LIMIT:
        flood_tracker[chat_id][user_id] = []  # Reset counter
        try:
            until_date = datetime.datetime.now() + datetime.timedelta(seconds=MUTE_DURATION)
            await client.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(),
                until_date=until_date,
            )
            await message.reply_text(
                f"🛡️ {message.from_user.mention} has been **muted for 5 minutes** for flooding!\n"
                "Please slow down."
            )
        except Exception:
            pass
