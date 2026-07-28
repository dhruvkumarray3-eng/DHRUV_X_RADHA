# -----------------------------------------------
# 🔸 NOBITA X PRIME — Auto Report System
# Detects harmful behaviour via Groq AI and
# files multiple Telegram reports with evidence.
# No violation keywords are stored in this file.
# -----------------------------------------------

import asyncio
from pyrogram import filters, enums
from pyrogram.types import Message
from pyrogram import raw

from SHUKLAMUSIC import app, userbot
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS, GROQ_API_KEY, LOGGER_ID, OWNER_ID

_report_col = mongodb.autoreport_settings   # per-chat on/off toggle
_report_log  = mongodb.autoreport_log        # track already-reported msg IDs

# ── Groq abuse-detection helper ───────────────────────────────────────────────
async def _is_harmful(text: str) -> tuple[bool, str]:
    """
    Returns (is_harmful: bool, category: str).
    category is one of: 'harassment', 'threat', 'hate_speech',
                        'copyright', 'spam', 'safe'
    Uses Groq AI — no violation words stored in code.
    """
    if not GROQ_API_KEY or not text or len(text.strip()) < 3:
        return False, "safe"
    try:
        from groq import AsyncGroq
        client = AsyncGroq(api_key=GROQ_API_KEY)
        resp = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a content moderation classifier. "
                        "Analyse the message and respond with ONLY a JSON object, "
                        "no explanation, no markdown:\n"
                        '{"harmful": true/false, "category": "<category>"}\n'
                        "Categories: harassment, threat, hate_speech, copyright, spam, safe\n"
                        "Be strict — only mark harmful if clearly abusive, threatening, "
                        "hateful, or a blatant copyright/spam violation. "
                        "Normal arguments, sarcasm, or mild language = safe."
                    ),
                },
                {"role": "user", "content": text[:500]},
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=60,
            temperature=0.0,
        )
        import json, re
        raw_text = resp.choices[0].message.content.strip()
        match = re.search(r'\{.*?\}', raw_text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return bool(data.get("harmful")), str(data.get("category", "safe"))
    except Exception:
        pass
    return False, "safe"


# Map AI category → Telegram report reason (raw API value)
_REASON_MAP = {
    "harassment":   "spam",
    "threat":       "violence",
    "hate_speech":  "spam",
    "copyright":    "copyright",
    "spam":         "spam",
}


async def _get_report_reason(category: str):
    """Return the raw Telegram InputReportReason for the given category."""
    from pyrogram.raw import types as raw_types
    mapping = {
        "spam":      raw_types.InputReportReasonSpam(),
        "violence":  raw_types.InputReportReasonViolence(),
        "copyright": raw_types.InputReportReasonCopyright(),
    }
    tg_key = _REASON_MAP.get(category, "spam")
    return mapping.get(tg_key, raw_types.InputReportReasonSpam())


# ── DB helpers ────────────────────────────────────────────────────────────────
async def _is_enabled(chat_id: int) -> bool:
    doc = await _report_col.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled", True))   # default ON


async def _set_enabled(chat_id: int, val: bool):
    await _report_col.update_one(
        {"chat_id": chat_id}, {"$set": {"enabled": val}}, upsert=True
    )


async def _already_reported(msg_id: int, chat_id: int) -> bool:
    doc = await _report_log.find_one({"msg_id": msg_id, "chat_id": chat_id})
    return bool(doc)


async def _mark_reported(msg_id: int, chat_id: int):
    await _report_log.update_one(
        {"msg_id": msg_id, "chat_id": chat_id},
        {"$set": {"msg_id": msg_id, "chat_id": chat_id}},
        upsert=True,
    )


# ── Core report function ──────────────────────────────────────────────────────
async def _file_reports(chat_id: int, msg_id: int, category: str):
    """
    File multiple Telegram reports on a single message using all
    available userbot sessions as separate reporters.
    """
    reason = await _get_report_reason(category)

    clients = []
    for attr in ("one", "two", "three", "four", "five"):
        c = getattr(userbot, attr, None)
        if c and getattr(c, "is_connected", False):
            clients.append(c)

    if not clients:
        # Fall back to app (bot) if no userbot session available
        clients = [app]

    success = 0
    for c in clients:
        try:
            peer = await c.resolve_peer(chat_id)
            await c.invoke(
                raw.functions.messages.Report(
                    peer=peer,
                    id=[msg_id],
                    reason=reason,
                    message=f"Automated report: {category} detected by NOBITA X PRIME",
                )
            )
            success += 1
            await asyncio.sleep(0.8)   # small delay between reports
        except Exception:
            pass

    return success


# ── Commands ──────────────────────────────────────────────────────────────────
@app.on_message(filters.command("autoreport") & filters.group & ~BANNED_USERS)
async def autoreport_cmd(client, message: Message):
    from SHUKLAMUSIC.plugins.tools.chatbot import is_admin
    if not await is_admin(client, message):
        return await message.reply_text("❌ Only admins can change auto-report settings.")

    args = message.command
    if len(args) < 2 or args[1].lower() not in ("on", "off", "status"):
        state = await _is_enabled(message.chat.id)
        return await message.reply_text(
            f"🛡️ **Auto-Report** is currently {'✅ ON' if state else '❌ OFF'}\n\n"
            "Usage: `/autoreport on` or `/autoreport off`"
        )

    sub = args[1].lower()
    if sub == "status":
        state = await _is_enabled(message.chat.id)
        return await message.reply_text(
            f"🛡️ Auto-Report: {'✅ Enabled' if state else '❌ Disabled'}\n"
            "I silently monitor messages and report harmful content to Telegram."
        )

    val = sub == "on"
    await _set_enabled(message.chat.id, val)
    if val:
        await message.reply_text(
            "🛡️ **Auto-Report ENABLED**\n\n"
            "I will now silently detect and report harmful messages "
            "(harassment, threats, hate speech, copyright, spam) "
            "directly to Telegram — automatically, with evidence."
        )
    else:
        await message.reply_text("🛡️ **Auto-Report DISABLED** in this chat.")


# ── Auto-detection handler ────────────────────────────────────────────────────
@app.on_message(
    filters.group & filters.text & ~filters.bot & ~BANNED_USERS,
    group=25,
)
async def autoreport_handler(client, message: Message):
    if not message.text or message.text.startswith("/"):
        return
    if not await _is_enabled(message.chat.id):
        return
    if await _already_reported(message.id, message.chat.id):
        return

    # Skip very short messages
    if len(message.text.strip()) < 8:
        return

    is_harmful, category = await _is_harmful(message.text)
    if not is_harmful:
        return

    # Mark before filing to avoid race conditions
    await _mark_reported(message.id, message.chat.id)

    # File reports in the background — don't block the chat
    asyncio.create_task(_do_report_and_log(message, category))


async def _do_report_and_log(message: Message, category: str):
    try:
        count = await _file_reports(message.chat.id, message.id, category)

        sender_info = "Unknown"
        try:
            if message.from_user:
                u = message.from_user
                sender_info = (
                    f"{u.first_name or ''} {u.last_name or ''}".strip()
                    + (f" (@{u.username})" if u.username else "")
                    + f" [<code>{u.id}</code>]"
                )
        except Exception:
            pass

        log_text = (
            f"🚨 <b>Auto-Report Filed</b>\n\n"
            f"📍 <b>Chat:</b> <code>{message.chat.id}</code>\n"
            f"👤 <b>Sender:</b> {sender_info}\n"
            f"🏷️ <b>Category:</b> <code>{category}</code>\n"
            f"📨 <b>Reports sent:</b> {count}\n"
            f"🔗 <b>Message ID:</b> <code>{message.id}</code>\n\n"
            f"📝 <b>Content preview:</b>\n"
            f"<i>{message.text[:200] if message.text else 'N/A'}</i>"
        )
        await app.send_message(LOGGER_ID, log_text)
    except Exception:
        pass
