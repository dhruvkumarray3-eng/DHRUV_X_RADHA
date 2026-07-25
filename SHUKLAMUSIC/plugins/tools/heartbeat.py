# -----------------------------------------------
# 🔸 NOBITA X PRIME — Heartbeat Plugin
# 🔹 Sends a heartbeat ping to LOGGER_ID every 5 min
#    to keep the bot alive and confirm it's running.
# -----------------------------------------------
import asyncio
import time
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

import config
from SHUKLAMUSIC import LOGGER, app
from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.core.mongo import mongodb

_LOG = LOGGER("SHUKLAMUSIC.heartbeat")
_db  = mongodb.heartbeat_settings

# ── In-memory state (loaded from DB at startup) ──────────────────────────────
_hb_enabled: bool = True   # default ON

HEARTBEAT_INTERVAL = 300   # seconds (5 minutes)

_boot_time = time.time()


def _fmt_uptime(seconds: float) -> str:
    d, r = divmod(int(seconds), 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    parts = []
    if d: parts.append(f"{d}d")
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    parts.append(f"{s}s")
    return " ".join(parts)


async def _load_state():
    global _hb_enabled
    doc = await _db.find_one({"_id": "heartbeat"})
    if doc is not None:
        _hb_enabled = doc.get("enabled", True)


async def _save_state():
    await _db.update_one(
        {"_id": "heartbeat"},
        {"$set": {"enabled": _hb_enabled}},
        upsert=True,
    )


async def _heartbeat_loop():
    await _load_state()
    await asyncio.sleep(60)   # wait 1 min after startup before first beat
    beat = 0
    while True:
        try:
            if _hb_enabled and config.LOGGER_ID:
                beat += 1
                uptime = _fmt_uptime(time.time() - _boot_time)
                text = (
                    f"💓 <b>ʜᴇᴀʀᴛʙᴇᴀᴛ #{beat}</b>\n\n"
                    f"🤖 <b>Bot:</b> {app.mention}\n"
                    f"⏱ <b>Uptime:</b> <code>{uptime}</code>\n"
                    f"✅ <b>Status:</b> ᴀʟɪᴠᴇ & ʀᴜɴɴɪɴɢ\n\n"
                    f"<i>Next ping in {HEARTBEAT_INTERVAL // 60} min • use /heartbeat off to mute</i>"
                )
                await app.send_message(config.LOGGER_ID, text)
        except Exception:
            pass
        await asyncio.sleep(HEARTBEAT_INTERVAL)


# Start the loop as a background task when the module loads
asyncio.create_task(_heartbeat_loop())


# ── Command handler ──────────────────────────────────────────────────────────

@app.on_message(
    filters.command(["heartbeat", "hb"], prefixes=["/", "!", "."]) & SUDOERS
)
async def heartbeat_cmd(client, message: Message):
    global _hb_enabled
    args = message.text.split()

    if len(args) == 1:
        # Status check
        state_text = "✅ <b>ON</b>" if _hb_enabled else "❌ <b>OFF</b>"
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Turn ON",
                    callback_data="hb_on",
                    style=ButtonStyle.SUCCESS,
                ),
                InlineKeyboardButton(
                    "❌ Turn OFF",
                    callback_data="hb_off",
                    style=ButtonStyle.DANGER,
                ),
            ]
        ])
        return await message.reply_text(
            f"💓 <b>Heartbeat Status:</b> {state_text}\n\n"
            f"⏱ Interval: every <b>{HEARTBEAT_INTERVAL // 60} minutes</b>\n"
            f"📍 Logger: <code>{config.LOGGER_ID}</code>",
            reply_markup=buttons,
        )

    action = args[1].lower()
    if action in ("on", "enable"):
        _hb_enabled = True
        await _save_state()
        await message.reply_text(
            "✅ <b>Heartbeat ON</b> — ᴄʜᴀɴɴᴇʟ ᴍᴇssᴀɢᴇs ʜᴀʀ 5 ᴍɪɴᴛ ᴊᴀʏᴇɴɢᴇ.",
        )
    elif action in ("off", "disable"):
        _hb_enabled = False
        await _save_state()
        await message.reply_text(
            "❌ <b>Heartbeat OFF</b> — ʟᴏɢɢᴇʀ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴs ʙᴀɴᴅ ᴋᴀʀ ᴅɪʏᴇ.",
        )
    else:
        await message.reply_text(
            "ℹ️ Usage: <code>/heartbeat on</code> | <code>/heartbeat off</code> | <code>/heartbeat</code> (status)"
        )


@app.on_callback_query(filters.regex(r"^hb_(on|off)$") & SUDOERS)
async def heartbeat_callback(client, cq):
    global _hb_enabled
    action = cq.data.split("_")[1]
    if action == "on":
        _hb_enabled = True
        await _save_state()
        await cq.answer("✅ Heartbeat ON!", show_alert=True)
    else:
        _hb_enabled = False
        await _save_state()
        await cq.answer("❌ Heartbeat OFF!", show_alert=True)
    try:
        state_text = "✅ <b>ON</b>" if _hb_enabled else "❌ <b>OFF</b>"
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Turn ON", callback_data="hb_on", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton("❌ Turn OFF", callback_data="hb_off", style=ButtonStyle.DANGER),
            ]
        ])
        await cq.message.edit_text(
            f"💓 <b>Heartbeat Status:</b> {state_text}\n\n"
            f"⏱ Interval: every <b>{HEARTBEAT_INTERVAL // 60} minutes</b>\n"
            f"📍 Logger: <code>{config.LOGGER_ID}</code>",
            reply_markup=buttons,
        )
    except Exception:
        pass
