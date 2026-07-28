# -----------------------------------------------
# 🔸 NOBITA X PRIME — Dynamic Session Manager
# Add / remove / list userbot sessions on the fly
# Owner only command — no restart needed
# -----------------------------------------------

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from SHUKLAMUSIC import app, userbot
from SHUKLAMUSIC.core.mongo import mongodb
from SHUKLAMUSIC.core.userbot import assistants, assistantids
from config import BANNED_USERS, OWNER_ID, API_ID, API_HASH, LOGGER_ID

_sessions_col = mongodb.dynamic_sessions   # stores extra sessions persistently

# ── Helper ────────────────────────────────────────────────────────────────────
def _is_owner(message: Message) -> bool:
    uid = message.from_user.id if message.from_user else 0
    return str(uid) == str(OWNER_ID)


async def _start_dynamic_client(session_string: str, slot: int) -> tuple[bool, str]:
    """
    Start a new Pyrogram userbot client from a session string.
    Returns (success, info_text).
    """
    name = f"SHUKLAAss_dyn_{slot}"
    try:
        client = Client(
            name=name,
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            no_updates=True,
            in_memory=True,
        )
        await client.start()
        me = await client.get_me()
        client.id = me.id
        client.name = me.mention
        client.username = me.username or "N/A"

        # Register in global assistants list
        if me.id not in assistantids:
            assistantids.append(me.id)
            assistants.append(slot)

        # Attach to userbot object as a dynamic attribute
        setattr(userbot, f"dyn_{slot}", client)

        try:
            await client.send_message(LOGGER_ID, f"✅ Dynamic Assistant #{slot} Started as {me.mention}")
        except Exception:
            pass

        return True, f"{me.mention} (@{me.username or 'N/A'}) | ID: <code>{me.id}</code>"
    except Exception as e:
        return False, str(e)


# ── /addsession command ───────────────────────────────────────────────────────
@app.on_message(filters.command("addsession") & filters.private & ~BANNED_USERS)
async def addsession_cmd(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner use kar sakta hai.")

    args = message.text.split(None, 1)
    if len(args) < 2 or not args[1].strip():
        count = await _sessions_col.count_documents({})
        return await message.reply_text(
            "╔══「 🔑 <b>Session Manager</b> 」\n"
            "║\n"
            f"║  Active dynamic sessions: <b>{count}</b>\n"
            "║\n"
            "║  <b>Commands:</b>\n"
            "║  <code>/addsession &lt;STRING_SESSION&gt;</code>\n"
            "║      → Add a new userbot session\n"
            "║  <code>/listsessions</code>\n"
            "║      → List all active sessions\n"
            "║  <code>/removesession &lt;slot_number&gt;</code>\n"
            "║      → Remove a session by slot\n"
            "╚════════════════════════\n\n"
            "💡 <i>Session strings are from @StringFatherBot or Pyrogram session generator.</i>"
        )

    session_string = args[1].strip()

    # Check duplicate
    existing = await _sessions_col.find_one({"session": session_string})
    if existing:
        return await message.reply_text("⚠️ Ye session already add hai!")

    processing = await message.reply_text("⏳ Session verify ho raha hai...")

    # Get next slot number
    last = await _sessions_col.find_one(sort=[("slot", -1)])
    slot = (last["slot"] + 1) if last else 101   # dynamic slots start at 101

    ok, info = await _start_dynamic_client(session_string, slot)

    if ok:
        await _sessions_col.insert_one({
            "slot": slot,
            "session": session_string,
            "info": info,
        })
        await processing.edit_text(
            f"✅ <b>Session #{slot} Added Successfully!</b>\n\n"
            f"👤 Account: {info}\n\n"
            "Session ab active hai aur auto-report mein use hoga."
        )
    else:
        await processing.edit_text(
            f"❌ <b>Session add nahi hua!</b>\n\n"
            f"Error: <code>{info}</code>\n\n"
            "Check karo ki session string sahi hai."
        )


# ── /listsessions command ─────────────────────────────────────────────────────
@app.on_message(filters.command("listsessions") & filters.private & ~BANNED_USERS)
async def listsessions_cmd(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner use kar sakta hai.")

    # Built-in slots (from config)
    built_in = []
    import config as cfg
    slot_map = {
        1: cfg.STRING1, 2: cfg.STRING2, 3: cfg.STRING3,
        4: cfg.STRING4, 5: cfg.STRING5, 6: cfg.STRING6, 7: cfg.STRING7,
    }
    for slot, val in slot_map.items():
        if val and val != "None":
            client = getattr(userbot, ["one","two","three","four","five","six","seven"][slot-1], None)
            name = getattr(client, "name", "Unknown") if client else "Not started"
            built_in.append(f"  🔹 Slot {slot}: {name}")

    # Dynamic slots (from DB)
    dynamic = []
    async for doc in _sessions_col.find().sort("slot", 1):
        dynamic.append(f"  🔸 Slot {doc['slot']}: {doc.get('info', 'Unknown')}")

    total = len(built_in) + len(dynamic)
    lines = ["╔══「 📋 <b>Active Sessions</b> 」", "║"]

    if built_in:
        lines.append("║  <b>Built-in (config):</b>")
        lines += [f"║ {l}" for l in built_in]
        lines.append("║")

    if dynamic:
        lines.append("║  <b>Dynamic (added via /addsession):</b>")
        lines += [f"║ {l}" for l in dynamic]
        lines.append("║")

    lines.append(f"║  <b>Total active: {total}</b>")
    lines.append("╚════════════════════════")

    if total == 0:
        return await message.reply_text("📭 Koi session active nahi hai.")

    await message.reply_text("\n".join(lines))


# ── /removesession command ────────────────────────────────────────────────────
@app.on_message(filters.command("removesession") & filters.private & ~BANNED_USERS)
async def removesession_cmd(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner use kar sakta hai.")

    args = message.command
    if len(args) < 2 or not args[1].isdigit():
        return await message.reply_text(
            "Usage: <code>/removesession &lt;slot_number&gt;</code>\n"
            "Slot numbers dekhne ke liye: <code>/listsessions</code>"
        )

    slot = int(args[1])
    doc = await _sessions_col.find_one({"slot": slot})
    if not doc:
        return await message.reply_text(f"❌ Slot {slot} ka koi dynamic session nahi mila.")

    # Stop the client if running
    client = getattr(userbot, f"dyn_{slot}", None)
    if client:
        try:
            if client.id in assistantids:
                assistantids.remove(client.id)
            await client.stop()
        except Exception:
            pass
        try:
            delattr(userbot, f"dyn_{slot}")
        except Exception:
            pass

    await _sessions_col.delete_one({"slot": slot})
    await message.reply_text(f"✅ Session #{slot} successfully remove ho gaya!")


# ── On bot start: restore dynamic sessions from DB ────────────────────────────
async def restore_dynamic_sessions():
    """Called at startup to reload dynamic sessions saved in MongoDB."""
    count = 0
    async for doc in _sessions_col.find().sort("slot", 1):
        slot = doc["slot"]
        session_string = doc.get("session", "")
        if not session_string:
            continue
        ok, info = await _start_dynamic_client(session_string, slot)
        if ok:
            count += 1
        else:
            # Remove broken session from DB
            await _sessions_col.delete_one({"slot": slot})
    if count:
        from SHUKLAMUSIC.logging import LOGGER
        LOGGER(__name__).info(f"Restored {count} dynamic session(s) from database.")
