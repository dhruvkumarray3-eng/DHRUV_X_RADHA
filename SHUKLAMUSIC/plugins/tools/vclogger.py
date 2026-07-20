import asyncio
from datetime import datetime
from logging import getLogger
from typing import Dict, Set
import random
from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb

LOGGER = getLogger(__name__)

vc_active_users: Dict[int, Set[int]] = {}   # chat_id → set of user_ids currently in VC
active_vc_chats: Set[int] = set()           # chats being monitored right now
vc_join_times: Dict[int, Dict[int, datetime]] = {}  # chat_id → {user_id → join_time}
vc_logging_status: Dict[int, bool] = {}     # chat_id → enabled/disabled (default True)

vcloggerdb = mongodb.vclogger
prefixes = [".", "!", "/", "@", "?", "'"]


# ─────────────────────────── helpers ────────────────────────────

def _format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        m, s = divmod(seconds, 60)
        return f"{m}m {s}s" if s else f"{m}m"
    else:
        h, rem = divmod(seconds, 3600)
        m = rem // 60
        return f"{h}h {m}m" if m else f"{h}h"


def to_small_caps(text: str) -> str:
    mapping = {
        "a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ꜰ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ",
        "k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ",
        "u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ",
        "A":"ᴀ","B":"ʙ","C":"ᴄ","D":"ᴅ","E":"ᴇ","F":"ꜰ","G":"ɢ","H":"ʜ","I":"ɪ","J":"ᴊ",
        "K":"ᴋ","L":"ʟ","M":"ᴍ","N":"ɴ","O":"ᴏ","P":"ᴘ","Q":"ǫ","R":"ʀ","S":"s","T":"ᴛ",
        "U":"ᴜ","V":"ᴠ","W":"ᴡ","X":"x","Y":"ʏ","Z":"ᴢ",
    }
    return "".join(mapping.get(c, c) for c in text)


async def _send_and_autodelete(chat_id: int, text: str, delay: int = 15):
    try:
        msg = await app.send_message(chat_id, text)
        asyncio.create_task(_delete_later(msg, delay))
    except Exception as e:
        LOGGER.error(f"VCLogger send error for {chat_id}: {e}")


async def _delete_later(message, delay: int):
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except Exception:
        pass


# ─────────────────────────── DB ops ─────────────────────────────

async def _get_status(chat_id: int) -> bool:
    if chat_id in vc_logging_status:
        return vc_logging_status[chat_id]
    try:
        doc = await vcloggerdb.find_one({"chat_id": chat_id})
        if doc:
            status = doc.get("status", True)
            vc_logging_status[chat_id] = status
            return status
    except Exception:
        pass
    return True   # default ON


async def _save_status(chat_id: int, status: bool):
    try:
        await vcloggerdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"chat_id": chat_id, "status": status}},
            upsert=True,
        )
    except Exception as e:
        LOGGER.error(f"VCLogger save error: {e}")


# ─────────────────────── participant polling ─────────────────────

async def _get_participants(chat_id: int) -> Set[int]:
    """Return set of user_ids currently in the VC using PyTgCalls."""
    try:
        # Lazy import to avoid circular deps
        from SHUKLAMUSIC.core.call import SHUKLA
        from SHUKLAMUSIC.utils.database import group_assistant
        assistant = await group_assistant(SHUKLA, chat_id)
        participants = await assistant.get_participants(chat_id)
        result = set()
        for p in participants:
            uid = getattr(p, "user_id", None)
            if uid:
                result.add(uid)
        return result
    except Exception:
        return set()


async def _monitor_loop(chat_id: int):
    LOGGER.info(f"VCLogger: started monitoring chat {chat_id}")
    while chat_id in active_vc_chats:
        try:
            if not await _get_status(chat_id):
                break

            new_users = await _get_participants(chat_id)
            current_users = vc_active_users.get(chat_id, set())

            joined = new_users - current_users
            left   = current_users - new_users

            for uid in joined:
                asyncio.create_task(_on_join(chat_id, uid))
            for uid in left:
                asyncio.create_task(_on_leave(chat_id, uid))

            vc_active_users[chat_id] = new_users

        except Exception as e:
            LOGGER.error(f"VCLogger monitor error for {chat_id}: {e}")

        await asyncio.sleep(6)

    LOGGER.info(f"VCLogger: stopped monitoring chat {chat_id}")


async def _on_join(chat_id: int, user_id: int):
    # Record join time
    vc_join_times.setdefault(chat_id, {})[user_id] = datetime.now()
    try:
        user = await app.get_users(user_id)
        name = user.first_name or "Someone"
        mention = f'<a href="tg://user?id={user_id}"><b>{to_small_caps(name)}</b></a>'
        msgs = [
            f"🎤 {mention} ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴠᴄ! ʟᴇᴛ's ᴍᴀᴋᴇ ɪᴛ ʟɪᴠᴇʟʏ 🎶",
            f"✨ {mention} ɪs ɴᴏᴡ ɪɴ ᴛʜᴇ ᴠᴄ — ᴡᴇʟᴄᴏᴍᴇ ᴀʙᴏᴀʀᴅ! 💫",
            f"🔥 {mention} ʜᴀs ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴠɪʙᴇ — ʟᴇᴛ's ʀᴏᴄᴋ! 🎵",
            f"👑 {mention} ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴠᴄ — ᴛʜᴇ ᴘᴀʀᴛʏ ᴊᴜsᴛ ɢᴏᴛ ʙᴇᴛᴛᴇʀ! 🥳",
            f"🌟 {mention} ɪs ʜᴇʀᴇ! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴠᴄ ʙᴏss 😎",
        ]
        await _send_and_autodelete(chat_id, random.choice(msgs))
    except Exception as e:
        LOGGER.error(f"VCLogger join handler error: {e}")


async def _on_leave(chat_id: int, user_id: int):
    join_time = vc_join_times.get(chat_id, {}).pop(user_id, None)
    duration_str = None
    if join_time:
        secs = int((datetime.now() - join_time).total_seconds())
        duration_str = _format_duration(secs)
    try:
        user = await app.get_users(user_id)
        name = user.first_name or "Someone"
        mention = f'<a href="tg://user?id={user_id}"><b>{to_small_caps(name)}</b></a>'
        if duration_str:
            msgs = [
                f"👋 {mention} ʟᴇғᴛ ᴛʜᴇ ᴠᴄ ᴀғᴛᴇʀ <b>{duration_str}</b> — ʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ ʙᴀᴄᴋ! 🌟",
                f"🚪 {mention} sᴛᴇᴘᴘᴇᴅ ᴏᴜᴛ ᴀғᴛᴇʀ <b>{duration_str}</b> — ᴄᴏᴍᴇ ʙᴀᴄᴋ sᴏᴏɴ! 💖",
                f"✌️ {mention} ᴡᴀs ʜᴇʀᴇ ғᴏʀ <b>{duration_str}</b> — ᴍɪssɪɴɢ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ 🎶",
                f"☠️ {mention} ʟᴇғᴛ ᴀғᴛᴇʀ <b>{duration_str}</b> — ᴅᴏɴ'ᴛ ʙᴇ ᴀ sᴛʀᴀɴɢᴇʀ! 😇",
            ]
        else:
            msgs = [
                f"👋 {mention} ʟᴇғᴛ ᴛʜᴇ ᴠᴄ — ʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ ʙᴀᴄᴋ! 🌟",
                f"🚪 {mention} sᴛᴇᴘᴘᴇᴅ ᴏᴜᴛ — ᴅᴏɴ'ᴛ ᴛᴀᴋᴇ ᴛᴏᴏ ʟᴏɴɢ! 💖",
                f"✌️ {mention} sᴀɪᴅ ɢᴏᴏᴅʙʏᴇ — ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴀɴᴅ ᴊᴏɪɴ ᴛʜᴇ ғᴜɴ! 🎶",
            ]
        await _send_and_autodelete(chat_id, random.choice(msgs))
    except Exception as e:
        LOGGER.error(f"VCLogger leave handler error: {e}")


# ─────────────────────── public API ─────────────────────────────

async def start_vc_monitoring(chat_id: int):
    """Call this when music starts in a chat (from call.py join_call)."""
    if not await _get_status(chat_id):
        return
    if chat_id in active_vc_chats:
        return   # already monitoring
    active_vc_chats.add(chat_id)
    # Seed current participants so first poll doesn't spam greetings
    try:
        vc_active_users[chat_id] = await _get_participants(chat_id)
    except Exception:
        vc_active_users[chat_id] = set()
    asyncio.create_task(_monitor_loop(chat_id))


async def stop_vc_monitoring(chat_id: int):
    """Call this when music stops in a chat (from call.py stop_stream)."""
    active_vc_chats.discard(chat_id)
    vc_active_users.pop(chat_id, None)
    vc_join_times.pop(chat_id, None)


# ─────────────────────── /vclogger command ───────────────────────

@app.on_message(
    filters.command("vclogger", prefixes=prefixes) & filters.group
)
async def vclogger_command(_, message: Message):
    chat_id = message.chat.id
    args = message.text.split()
    status = await _get_status(chat_id)
    prefix_ui = ", ".join(f"<b>{p}vclogger</b>" for p in prefixes)
    state_ui = to_small_caps(str(status))

    if len(args) == 1:
        await message.reply(
            f"📌 <b>VC Logging:</b> <b>{state_ui}</b>\n"
            f"Use {prefix_ui} <b>[on | off]</b>",
            disable_web_page_preview=True,
        )
    elif len(args) == 2:
        arg = args[1].lower()
        if arg in ("on", "enable", "yes"):
            vc_logging_status[chat_id] = True
            await _save_status(chat_id, True)
            await message.reply(f"✅ <b>VC logging ENABLED</b>")
        elif arg in ("off", "disable", "no"):
            vc_logging_status[chat_id] = False
            await _save_status(chat_id, False)
            await stop_vc_monitoring(chat_id)
            await message.reply(f"🚫 <b>VC logging DISABLED</b>")
        else:
            await message.reply("❌ Use <b>[on | off]</b>")


# ─────────────────────── startup init ────────────────────────────

async def initialize_vc_logger():
    """Called at startup — just load persisted on/off settings."""
    try:
        count = 0
        async for doc in vcloggerdb.find({}):
            vc_logging_status[doc["chat_id"]] = doc.get("status", True)
            count += 1
        LOGGER.info(f"VCLogger: loaded settings for {count} chats (monitoring starts when music plays)")
    except Exception as e:
        LOGGER.error(f"VCLogger init error: {e}")
