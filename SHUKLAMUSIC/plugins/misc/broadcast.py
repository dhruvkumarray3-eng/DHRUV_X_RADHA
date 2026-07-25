# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
import asyncio
from pyrogram import filters
from pyrogram.enums import ButtonStyle, ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SHUKLAMUSIC import app
from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from SHUKLAMUSIC.utils.decorators.language import language
from SHUKLAMUSIC.utils.formatters import alpha_to_int
from config import adminlist

IS_BROADCASTING = False


def _broadcast_selector_markup(chat_id: int, msg_id: int) -> InlineKeyboardMarkup:
    """Target + pin-mode selector shown before broadcast starts."""
    return InlineKeyboardMarkup([
        # ── Row 1: Target audience ──
        [
            InlineKeyboardButton(
                text="👥 ɢʀᴏᴜᴘs",
                callback_data=f"bcast_nopin|groups|{chat_id}|{msg_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="👤 ᴜsᴇʀs",
                callback_data=f"bcast_nopin|users|{chat_id}|{msg_id}",
                style=ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text="📢 ᴄʜᴀɴɴᴇʟs",
                callback_data=f"bcast_nopin|channels|{chat_id}|{msg_id}",
                style=ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(
                text="🌐 ᴀʟʟ",
                callback_data=f"bcast_nopin|all|{chat_id}|{msg_id}",
                style=ButtonStyle.DANGER,
            ),
        ],
        # ── Row 3: Pin options (groups only) ──
        [
            InlineKeyboardButton(
                text="🔊 ɢʀᴏᴜᴘs + ʟᴏᴜᴅ ᴘɪɴ",
                callback_data=f"bcast_loud|groups|{chat_id}|{msg_id}",
                style=ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(
                text="📌 ɢʀᴏᴜᴘs + sɪʟᴇɴᴛ ᴘɪɴ",
                callback_data=f"bcast_silent|groups|{chat_id}|{msg_id}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ ᴄᴀɴᴄᴇʟ",
                callback_data="bcast_cancel",
                style=ButtonStyle.DANGER,
            ),
        ],
    ])


async def _do_broadcast(
    client,
    origin_chat_id: int,
    msg_id: int,
    pin_mode: str,
    target: str = "groups",
) -> tuple:
    """Forward a message to the chosen target.

    target: 'groups' | 'users' | 'channels' | 'all'
    pin_mode: 'loud' | 'silent' | 'nopin'
    Returns (sent_count, failed_count, pinned_count).
    """
    from pyrogram.enums import ChatType

    sent = failed = pinned = 0

    # ── Build recipient list ────────────────────────────────────────────────
    chat_ids: list[int] = []

    if target in ("groups", "channels", "all"):
        for c in await get_served_chats():
            cid = int(c["chat_id"])
            if target == "all":
                chat_ids.append(cid)
            else:
                try:
                    chat_obj = await app.get_chat(cid)
                    is_channel = chat_obj.type == ChatType.CHANNEL
                    if target == "channels" and is_channel:
                        chat_ids.append(cid)
                    elif target == "groups" and not is_channel:
                        chat_ids.append(cid)
                except Exception:
                    if target == "groups":   # assume group when unknown
                        chat_ids.append(cid)

    if target in ("users", "all"):
        for u in await get_served_users():
            chat_ids.append(int(u["user_id"]))

    # ── Send ────────────────────────────────────────────────────────────────
    seen: set[int] = set()
    for cid in chat_ids:
        if cid in seen:
            continue
        seen.add(cid)
        try:
            m = await app.forward_messages(cid, origin_chat_id, msg_id)
            sent += 1
            if pin_mode == "loud":
                try:
                    await m.pin(disable_notification=False)
                    pinned += 1
                except Exception:
                    pass
            elif pin_mode == "silent":
                try:
                    await m.pin(disable_notification=True)
                    pinned += 1
                except Exception:
                    pass
            await asyncio.sleep(0.2)
        except FloodWait as fw:
            flood_time = int(fw.value)
            if flood_time > 200:
                failed += 1
                continue
            await asyncio.sleep(flood_time)
            try:
                m = await app.forward_messages(cid, origin_chat_id, msg_id)
                sent += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1

    return sent, failed, pinned


@app.on_message(filters.command("broadcast") & SUDOERS)
@language
async def braodcast_message(client, message, _):
    global IS_BROADCASTING

    # ── Reply mode: show colorful pin-mode selector ──────────────────────────
    if message.reply_to_message:
        await message.reply_text(
            "📢 <b>ʙʀᴏᴀᴅᴄᴀsᴛ ᴏᴘᴛɪᴏɴs</b>\n\nChoose how to send this message to all chats:",
            reply_markup=_broadcast_selector_markup(
                message.chat.id,
                message.reply_to_message.id,
            ),
        )
        return

    # ── Text mode (legacy flags): broadcast immediately ───────────────────────
    if len(message.command) < 2:
        return await message.reply_text(_["broad_2"])
    query = message.text.split(None, 1)[1]
    flags = [f for f in ["-pin", "-nobot", "-pinloud", "-assistant", "-user"] if f in query]
    for f in flags:
        query = query.replace(f, "")
    if not query.strip():
        return await message.reply_text(_["broad_8"])

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = [int(c["chat_id"]) for c in await get_served_chats()]
        for i in chats:
            try:
                m = await app.send_message(i, text=query)
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                continue
        try:
            await message.reply_text(_["broad_3"].format(sent, pin))
        except Exception:
            pass

    if "-user" in message.text:
        susr = 0
        served_users = [int(u["user_id"]) for u in await get_served_users()]
        for i in served_users:
            try:
                await app.send_message(i, text=query)
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                pass
        try:
            await message.reply_text(_["broad_4"].format(susr))
        except Exception:
            pass

    if "-assistant" in message.text:
        aw = await message.reply_text(_["broad_5"])
        text = _["broad_6"]
        from SHUKLAMUSIC.core.userbot import assistants
        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    await client.send_message(dialog.chat.id, text=query)
                    sent += 1
                    await asyncio.sleep(3)
                except FloodWait as fw:
                    flood_time = int(fw.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception:
                    continue
            text += _["broad_7"].format(num, sent)
        try:
            await aw.edit_text(text)
        except Exception:
            pass
    IS_BROADCASTING = False


# ── Broadcast pin-mode callback handlers ─────────────────────────────────────

@app.on_callback_query(filters.regex(r"^bcast_") & SUDOERS)
async def broadcast_pin_callback(client, cq):
    global IS_BROADCASTING
    data = cq.data

    if data == "bcast_cancel":
        try:
            await cq.message.delete()
        except Exception:
            pass
        await cq.answer("❌ Broadcast cancelled.", show_alert=True)
        return

    # New format: bcast_<pin>|<target>|<chat_id>|<msg_id>
    parts = data.split("|")
    if len(parts) != 4:
        return await cq.answer("Invalid data.", show_alert=True)

    pin_mode       = parts[0].replace("bcast_", "")  # loud | silent | nopin
    target         = parts[1]                          # groups | users | channels | all
    origin_chat_id = int(parts[2])
    msg_id         = int(parts[3])

    _target_labels = {
        "groups": "👥 Groups", "users": "👤 Users",
        "channels": "📢 Channels", "all": "🌐 All",
    }
    _pin_labels = {"loud": "🔊 Loud Pin", "silent": "📌 Silent Pin", "nopin": "📨 No Pin"}
    target_label = _target_labels.get(target, target)
    pin_label    = _pin_labels.get(pin_mode, pin_mode)

    await cq.answer(f"Broadcasting to {target_label}…")
    try:
        await cq.message.edit_text(
            f"📢 <b>Broadcasting…</b>\n"
            f"🎯 <b>Target:</b> {target_label}  •  <b>Pin:</b> {pin_label}\n\n"
            f"⏳ Please wait…"
        )
    except Exception:
        pass

    IS_BROADCASTING = True
    try:
        sent, failed, pinned = await _do_broadcast(
            client, origin_chat_id, msg_id, pin_mode, target=target
        )
    finally:
        IS_BROADCASTING = False

    summary = (
        f"✅ <b>Broadcast Complete!</b>\n\n"
        f"🎯 <b>Target:</b> {target_label}\n"
        f"📤 <b>Sent:</b> {sent}\n"
        f"❌ <b>Failed:</b> {failed}\n"
    )
    if pin_mode != "nopin":
        summary += f"📌 <b>Pinned:</b> {pinned}\n"
    summary += f"\n<i>Pin mode: {pin_label}</i>"

    try:
        await cq.message.edit_text(summary)
    except Exception:
        try:
            await app.send_message(cq.message.chat.id, summary)
        except Exception:
            pass


async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except Exception:
            continue


asyncio.create_task(auto_clean())
