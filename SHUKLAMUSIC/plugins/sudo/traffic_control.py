# -----------------------------------------------
# 🔸 NOBITA X PRIME — Telegram Traffic Control
# 🔹 Owner-only remote flood & rate-limit manager
# -----------------------------------------------
import time
import asyncio
from collections import defaultdict, deque
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from config import OWNER_ID, BANNED_USERS

# ── DB ───────────────────────────────────────────────────────────────────────
traffic_db   = mongodb.traffic_control     # per-chat flood settings
traffic_logs = mongodb.traffic_logs        # message rate log

# ── In-memory rate tracker ───────────────────────────────────────────────────
# chat_id → deque of unix timestamps (last 60 s)
_rate_map: dict[int, deque] = defaultdict(lambda: deque())
_warned:   set[int]         = set()        # chats already warned this window


# ── Helpers ──────────────────────────────────────────────────────────────────
async def get_settings(chat_id: int) -> dict:
    doc = await traffic_db.find_one({"chat_id": chat_id})
    if not doc:
        return {"enabled": False, "limit": 30, "window": 60, "action": "warn"}
    return doc


async def save_settings(chat_id: int, **kwargs):
    await traffic_db.update_one(
        {"chat_id": chat_id},
        {"$set": kwargs},
        upsert=True,
    )


# ── Passive traffic counter ──────────────────────────────────────────────────
@app.on_message(filters.group & ~BANNED_USERS, group=99)
async def count_traffic(client, message: Message):
    """Count every group message for rate analysis — silent background handler."""
    chat_id = message.chat.id
    now = time.time()
    dq = _rate_map[chat_id]
    dq.append(now)

    cfg = await get_settings(chat_id)
    if not cfg.get("enabled"):
        return

    window = int(cfg.get("window", 60))
    limit  = int(cfg.get("limit",  30))

    # Trim old timestamps
    while dq and now - dq[0] > window:
        dq.popleft()

    count = len(dq)

    # Log to DB every 100 messages
    if count % 100 == 0:
        await traffic_logs.update_one(
            {"chat_id": chat_id, "date": time.strftime("%Y-%m-%d")},
            {"$inc": {"total": 100}},
            upsert=True,
        )

    if count > limit and chat_id not in _warned:
        _warned.add(chat_id)
        action = cfg.get("action", "warn")
        try:
            if action == "warn":
                await client.send_message(
                    chat_id,
                    f"⚠️ <b>Traffic Alert!</b>\n\n"
                    f"📊 <b>{count}</b> messages in last <b>{window}s</b> "
                    f"(limit: <b>{limit}</b>)\n\n"
                    f"🔥 <i>Slow down to avoid Telegram flood limits!</i>",
                )
            elif action == "slow":
                await client.set_slow_mode(chat_id, 3)
                await client.send_message(
                    chat_id,
                    f"🐢 <b>Slow-mode ON (3s)</b> — High traffic detected: "
                    f"<b>{count} msg/{window}s</b>",
                )
        except Exception:
            pass

        # Auto-reset warn flag after window
        async def _reset():
            await asyncio.sleep(window)
            _warned.discard(chat_id)
        asyncio.create_task(_reset())


# ── /traffic — show stats ────────────────────────────────────────────────────
@app.on_message(
    filters.command("traffic") & filters.user(OWNER_ID)
)
async def traffic_stats(client, message: Message):
    args = message.command[1:]

    # /traffic global
    if args and args[0].lower() == "global":
        chats = await traffic_db.count_documents({})
        active = sum(1 for dq in _rate_map.values() if dq)
        total_today = 0
        async for doc in traffic_logs.find({"date": time.strftime("%Y-%m-%d")}):
            total_today += doc.get("total", 0)
        return await message.reply_text(
            f"📊 <b>Global Traffic Report</b>\n\n"
            f"🛡 Monitored chats : <code>{chats}</code>\n"
            f"🔥 Active right now: <code>{active}</code>\n"
            f"📨 Messages today : <code>{total_today}+</code>\n\n"
            f"Use <code>/traffic &lt;chat_id&gt;</code> for per-chat details."
        )

    # /traffic <chat_id>
    if args:
        try:
            cid = int(args[0])
        except ValueError:
            return await message.reply_text("❌ Usage: <code>/traffic &lt;chat_id&gt;</code>")
    else:
        if message.chat.type.name in ("GROUP", "SUPERGROUP"):
            cid = message.chat.id
        else:
            return await message.reply_text(
                "Usage:\n"
                "<code>/traffic</code> — this chat\n"
                "<code>/traffic global</code> — all chats\n"
                "<code>/traffic &lt;chat_id&gt;</code> — specific chat"
            )

    cfg = await get_settings(cid)
    dq  = _rate_map.get(cid, deque())
    now = time.time()
    window = int(cfg.get("window", 60))
    recent = sum(1 for t in dq if now - t <= window)

    log = await traffic_logs.find_one({"chat_id": cid, "date": time.strftime("%Y-%m-%d")})
    today = (log or {}).get("total", 0)

    status = "🟢 ON" if cfg.get("enabled") else "🔴 OFF"
    await message.reply_text(
        f"📊 <b>Traffic Control — Chat</b> <code>{cid}</code>\n\n"
        f"🛡 Flood guard : {status}\n"
        f"⚡ Rate limit  : <code>{cfg.get('limit',30)}</code> msg / <code>{window}s</code>\n"
        f"🚦 Action      : <code>{cfg.get('action','warn')}</code>\n"
        f"📡 Now (window): <code>{recent}</code> messages\n"
        f"📨 Today total : <code>{today}+</code>",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 Enable", callback_data=f"tc_on:{cid}", style=ButtonStyle.SUCCESS),
                InlineKeyboardButton("🔴 Disable", callback_data=f"tc_off:{cid}", style=ButtonStyle.DANGER),
            ],
            [
                InlineKeyboardButton("⚡ Set limit", callback_data=f"tc_limit:{cid}", style=ButtonStyle.PRIMARY),
                InlineKeyboardButton("🔄 Refresh", callback_data=f"tc_refresh:{cid}", style=ButtonStyle.PRIMARY),
            ],
        ]),
    )


# ── /floodctrl on|off [chat_id] ───────────────────────────────────────────────
@app.on_message(
    filters.command("floodctrl") & filters.user(OWNER_ID)
)
async def floodctrl_cmd(client, message: Message):
    args = message.command[1:]
    if not args:
        return await message.reply_text(
            "Usage:\n"
            "<code>/floodctrl on</code> — enable in this chat\n"
            "<code>/floodctrl off</code> — disable in this chat\n"
            "<code>/floodctrl on &lt;chat_id&gt;</code> — enable remotely\n"
            "<code>/floodctrl off &lt;chat_id&gt;</code> — disable remotely"
        )
    state = args[0].lower() == "on"
    cid = int(args[1]) if len(args) > 1 else message.chat.id
    await save_settings(cid, enabled=state, chat_id=cid)
    icon = "🟢" if state else "🔴"
    await message.reply_text(
        f"{icon} Flood control <b>{'enabled' if state else 'disabled'}</b> "
        f"for chat <code>{cid}</code>."
    )


# ── /setflood <limit> [window_seconds] [chat_id] ─────────────────────────────
@app.on_message(
    filters.command(["setflood", "setfloodlimit"]) & filters.user(OWNER_ID)
)
async def setflood_cmd(client, message: Message):
    args = message.command[1:]
    if not args:
        return await message.reply_text(
            "Usage: <code>/setflood &lt;limit&gt; [window_secs] [chat_id]</code>\n\n"
            "Example: <code>/setflood 20 60</code> — max 20 msg per 60 s\n"
            "Action options: warn (default) or slow"
        )
    try:
        limit  = int(args[0])
        window = int(args[1]) if len(args) > 1 else 60
        cid    = int(args[2]) if len(args) > 2 else message.chat.id
    except ValueError:
        return await message.reply_text("❌ All arguments must be integers.")

    await save_settings(cid, chat_id=cid, limit=limit, window=window, enabled=True)
    await message.reply_text(
        f"✅ Flood limit set for <code>{cid}</code>:\n"
        f"⚡ <b>{limit}</b> messages per <b>{window}s</b>\n"
        f"🛡 Flood control auto-enabled."
    )


# ── /setfloodaction warn|slow [chat_id] ───────────────────────────────────────
@app.on_message(
    filters.command("setfloodaction") & filters.user(OWNER_ID)
)
async def setfloodaction_cmd(client, message: Message):
    args = message.command[1:]
    if not args or args[0].lower() not in ("warn", "slow"):
        return await message.reply_text(
            "Usage: <code>/setfloodaction warn|slow [chat_id]</code>\n\n"
            "• <b>warn</b> — send a warning message\n"
            "• <b>slow</b> — enable slow-mode (3s)"
        )
    action = args[0].lower()
    cid    = int(args[1]) if len(args) > 1 else message.chat.id
    await save_settings(cid, action=action)
    await message.reply_text(
        f"✅ Flood action for <code>{cid}</code> set to <b>{action}</b>."
    )


# ── Inline callbacks ──────────────────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^tc_(on|off|refresh|limit):(-?\d+)$"))
async def tc_callback(client, query):
    if query.from_user.id != OWNER_ID:
        return await query.answer("🔒 Owner only.", show_alert=True)

    action_str, cid_str = query.data.split(":")[0].split("_")[1], query.data.split(":")[1]
    cid = int(cid_str)

    if action_str == "on":
        await save_settings(cid, enabled=True, chat_id=cid)
        await query.answer("🟢 Flood control enabled.", show_alert=True)
    elif action_str == "off":
        await save_settings(cid, enabled=False, chat_id=cid)
        await query.answer("🔴 Flood control disabled.", show_alert=True)
    elif action_str == "limit":
        await query.answer(
            f"Use /setflood <limit> [window] {cid} to change the limit.",
            show_alert=True,
        )
        return
    elif action_str == "refresh":
        await query.answer("🔄 Refreshed!", show_alert=False)

    # Re-render stats
    cfg = await get_settings(cid)
    dq  = _rate_map.get(cid, deque())
    now = time.time()
    window = int(cfg.get("window", 60))
    recent = sum(1 for t in dq if now - t <= window)
    status = "🟢 ON" if cfg.get("enabled") else "🔴 OFF"
    try:
        await query.message.edit_text(
            f"📊 <b>Traffic Control — Chat</b> <code>{cid}</code>\n\n"
            f"🛡 Flood guard : {status}\n"
            f"⚡ Rate limit  : <code>{cfg.get('limit',30)}</code> msg / <code>{window}s</code>\n"
            f"🚦 Action      : <code>{cfg.get('action','warn')}</code>\n"
            f"📡 Now (window): <code>{recent}</code> messages\n",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🟢 Enable", callback_data=f"tc_on:{cid}", style=ButtonStyle.SUCCESS),
                    InlineKeyboardButton("🔴 Disable", callback_data=f"tc_off:{cid}", style=ButtonStyle.DANGER),
                ],
                [
                    InlineKeyboardButton("⚡ Set limit", callback_data=f"tc_limit:{cid}", style=ButtonStyle.PRIMARY),
                    InlineKeyboardButton("🔄 Refresh", callback_data=f"tc_refresh:{cid}", style=ButtonStyle.PRIMARY),
                ],
            ]),
        )
    except Exception:
        pass
