# -----------------------------------------------
# 🔸 SHUKLAMUSIC — Clean Mongo Plugin
# 🔹 /cleanmongo — sudo only
# Cleans junk data, shows DB stats, alerts owner
# -----------------------------------------------
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
import config
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from SHUKLAMUSIC.misc import SUDOERS

# ── MongoDB size alert threshold (bytes) ───────────────────────────────────
_ALERT_THRESHOLD = 400 * 1024 * 1024   # 400 MB → warn before Atlas 512 MB cap
_alert_sent = False                     # avoid flooding

# ── Emoji button row ────────────────────────────────────────────────────────
_CLEAN_BUTTONS = [
    [
        InlineKeyboardButton("😊 ᴄʟᴇᴀɴ ᴀғᴋ",      callback_data="cmg_afk",     style=ButtonStyle.PRIMARY),
        InlineKeyboardButton("❤️‍🩹 ᴄʟᴇᴀɴ ɴᴏᴛᴇs",   callback_data="cmg_notes",   style=ButtonStyle.PRIMARY),
    ],
    [
        InlineKeyboardButton("🫠 ᴄʟᴇᴀɴ ғɪʟᴛᴇʀs",  callback_data="cmg_filters", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton("❤️‍🔥 ᴄʟᴇᴀɴ ᴀʟʟ",     callback_data="cmg_all",     style=ButtonStyle.DANGER),
    ],
    [
        InlineKeyboardButton("😇 ᴅʙ sᴛᴀᴛs",        callback_data="cmg_stats",   style=ButtonStyle.SUCCESS),
        InlineKeyboardButton("👻 ᴄᴀɴᴄᴇʟ",          callback_data="cmg_cancel",  style=ButtonStyle.DANGER),
    ],
]


# ── Helpers ─────────────────────────────────────────────────────────────────
async def _get_db_stats() -> dict:
    """Return dbStats dict from the bot's database."""
    try:
        stats = await mongodb.command("dbStats")
        data_mb   = stats.get("dataSize",    0) / 1024 / 1024
        store_mb  = stats.get("storageSize", 0) / 1024 / 1024
        total_mb  = stats.get("totalSize",   stats.get("storageSize", 0)) / 1024 / 1024
        colls     = stats.get("collections", 0)
        objs      = stats.get("objects",     0)
        return {
            "data_mb": round(data_mb, 2),
            "store_mb": round(store_mb, 2),
            "total_mb": round(total_mb, 2),
            "collections": colls,
            "objects": objs,
            "raw_size": stats.get("storageSize", 0),
        }
    except Exception as e:
        return {"error": str(e)}


def _fill_bar(used_mb: float, limit_mb: float = 512) -> str:
    pct = min(used_mb / limit_mb, 1.0)
    filled = int(pct * 10)
    bar = "🟥" * filled + "⬜" * (10 - filled)
    return f"{bar} {pct*100:.1f}%"


async def _stats_text() -> str:
    s = await _get_db_stats()
    if "error" in s:
        return f"❌ DB error: `{s['error']}`"
    bar = _fill_bar(s["store_mb"])
    return (
        f"<b>🗄 MongoDB Stats</b>\n\n"
        f"✨ ᴅᴀᴛᴀ sɪᴢᴇ   : <code>{s['data_mb']} MB</code>\n"
        f"🫠 sᴛᴏʀᴀɢᴇ    : <code>{s['store_mb']} MB</code>\n"
        f"❤️‍🔥 ᴄᴏʟʟᴇᴄᴛɪᴏɴs : <code>{s['collections']}</code>\n"
        f"😇 ᴏʙᴊᴇᴄᴛs    : <code>{s['objects']}</code>\n\n"
        f"<b>Atlas 512MB limit</b>\n{bar}"
    )


# ── Clean functions ──────────────────────────────────────────────────────────
async def _clean_afk() -> str:
    try:
        res = await mongodb.afk.delete_many({})
        return f"😊 AFK ᴄʟᴇᴀɴᴇᴅ: <b>{res.deleted_count}</b> ᴇɴᴛʀɪᴇs"
    except Exception as e:
        return f"❌ AFK error: {e}"


async def _clean_notes() -> str:
    try:
        res = await mongodb.notes.delete_many({})
        return f"❤️‍🩹 ɴᴏᴛᴇs ᴄʟᴇᴀɴᴇᴅ: <b>{res.deleted_count}</b> ᴇɴᴛʀɪᴇs"
    except Exception as e:
        return f"❌ Notes error: {e}"


async def _clean_filters() -> str:
    try:
        res = await mongodb.filters.delete_many({})
        return f"🫠 ғɪʟᴛᴇʀs ᴄʟᴇᴀɴᴇᴅ: <b>{res.deleted_count}</b> ᴇɴᴛʀɪᴇs"
    except Exception as e:
        return f"❌ Filters error: {e}"


async def _clean_all() -> str:
    results = await asyncio.gather(
        _clean_afk(), _clean_notes(), _clean_filters(), return_exceptions=True
    )
    return "\n".join(str(r) for r in results)


# ── Mongo full alert scheduler ───────────────────────────────────────────────
async def _check_mongo_size():
    global _alert_sent
    s = await _get_db_stats()
    if "error" in s:
        return
    if s["raw_size"] >= _ALERT_THRESHOLD:
        if not _alert_sent:
            _alert_sent = True
            try:
                await app.send_message(
                    config.OWNER_ID,
                    f"⚠️ <b>MongoDB Alert!</b>\n\n"
                    f"Your database is using <b>{s['store_mb']} MB</b> "
                    f"out of the free-tier <b>512 MB</b> limit.\n\n"
                    f"Use /cleanmongo to free up space now! 🤕",
                )
            except Exception:
                pass
    else:
        _alert_sent = False   # reset once usage drops


_mongo_scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
_mongo_scheduler.add_job(_check_mongo_size, trigger="interval", hours=6)
_mongo_scheduler.start()


# ── /cleanmongo command ──────────────────────────────────────────────────────
@app.on_message(filters.command("cleanmongo") & SUDOERS)
async def cleanmongo_cmd(client, message: Message):
    text = await _stats_text()
    await message.reply_text(
        text + "\n\n<i>Choose an action below 👇</i>",
        reply_markup=InlineKeyboardMarkup(_CLEAN_BUTTONS),
    )


# ── Callback handlers ────────────────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^cmg_"))
async def cleanmongo_cb(client, cq: CallbackQuery):
    if cq.from_user.id not in SUDOERS:
        return await cq.answer("🤕 sᴜᴅᴏ ᴏɴʟʏ!", show_alert=True)

    action = cq.data

    if action == "cmg_cancel":
        await cq.message.delete()
        return

    if action == "cmg_stats":
        text = await _stats_text()
        await cq.edit_message_text(
            text + "\n\n<i>Choose an action below 👇</i>",
            reply_markup=InlineKeyboardMarkup(_CLEAN_BUTTONS),
        )
        return

    await cq.answer("🫰 ᴘʀᴏᴄᴇssɪɴɢ…")

    if action == "cmg_afk":
        result = await _clean_afk()
    elif action == "cmg_notes":
        result = await _clean_notes()
    elif action == "cmg_filters":
        result = await _clean_filters()
    elif action == "cmg_all":
        result = await _clean_all()
    else:
        return

    stats = await _stats_text()
    await cq.edit_message_text(
        f"{result}\n\n{stats}\n\n<i>Choose an action below 👇</i>",
        reply_markup=InlineKeyboardMarkup(_CLEAN_BUTTONS),
    )
