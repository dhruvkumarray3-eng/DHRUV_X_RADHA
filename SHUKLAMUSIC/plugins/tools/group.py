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
import random
import re
import aiohttp
from pyrogram import Client, filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SHUKLAMUSIC import app
from config import OWNER_ID

_G = ButtonStyle.SUCCESS
_R = ButtonStyle.DANGER
_B = ButtonStyle.PRIMARY


# ── VC started ────────────────────────────────────────────────────────────────
@app.on_message(filters.video_chat_started)
async def vc_started(_, msg: Message):
    await msg.reply(
        "🎙 **ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ!**\n\nᴊᴏɪɴ ᴛʜᴇ ᴠᴄ ᴀɴᴅ ᴇɴᴊᴏʏ ᴍᴜsɪᴄ 🎶",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🎵 Pʟᴀʏ Mᴜsɪᴄ", callback_data="cb_play_instruction", style=_G),
        ]]),
    )


# ── VC ended ──────────────────────────────────────────────────────────────────
@app.on_message(filters.video_chat_ended)
async def vc_ended(_, msg: Message):
    await msg.reply("**👋 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ — sᴇᴇ ʏᴏᴜ ɴᴇxᴛ ᴛɪᴍᴇ! 🌟**")


# ── VC members invited  (custom filter — works with all kurigram versions) ────
_vc_invite_filter = filters.create(
    lambda _, __, m: bool(getattr(m, "video_chat_members_invited", None))
)

_INVITE_MSGS = [
    "🎉 {inviter} ɴᴇ {invited} ᴋᴏ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴍᴇɪɴ ɪɴᴠɪᴛᴇ ᴋɪʏᴀ!\nᴀᴀᴏ ᴀᴜʀ ᴍᴜsɪᴄ ᴋᴀ ᴍᴀᴢᴀ ʟᴏ 🎵",
    "🔥 {inviter} ɴᴇ {invited} ᴋᴏ ᴠᴄ ᴘᴇ ʙᴜʟᴀʏᴀ — ᴀᴀ ᴊᴀᴏ ʙᴏss! 👑",
    "🌟 {invited} ᴋᴏ {inviter} ɴᴇ ᴠᴄ ᴘᴇ ɪɴᴠɪᴛᴇ ᴋɪʏᴀ ʜᴀɪ — ᴊᴏɪɴ ᴋᴀʀᴏ ᴀᴜʀ ᴠɪʙᴇ ᴋᴀʀᴏ! ✨",
    "🎶 {inviter} ʜᴀs ɪɴᴠɪᴛᴇᴅ {invited} ᴛᴏ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ!\nᴄᴏᴍᴇ ᴊᴏɪɴ ᴛʜᴇ ᴘᴀʀᴛʏ 🥳",
    "💫 {invited} ᴋᴏ {inviter} ɴᴇ ᴠᴄ ᴘᴇ ʙᴜʟᴀʏᴀ ʜᴀɪ!\nᴊʟᴅɪ ᴊᴏɪɴ ᴋᴀʀᴏ, ᴍᴀsᴛɪ sʜᴜʀᴜ ʜᴏ ɢᴀʏɪ ʜᴀɪ 🎊",
]

_COLORS = [_G, _B, _R]


@app.on_message(_vc_invite_filter & filters.group)
async def vc_members_invited(_, message: Message):
    try:
        inviter_obj = message.from_user
        inviter_mention = (
            f'<a href="tg://user?id={inviter_obj.id}"><b>{inviter_obj.first_name}</b></a>'
            if inviter_obj else "Someone"
        )

        invited_data = message.video_chat_members_invited
        invited_users = getattr(invited_data, "users", [])

        # Build mention list
        invited_mentions = []
        invited_buttons = []
        for i, user in enumerate(invited_users):
            name = user.first_name or "User"
            mention = f'<a href="tg://user?id={user.id}"><b>{name}</b></a>'
            invited_mentions.append(mention)
            invited_buttons.append(
                InlineKeyboardButton(
                    f"👤 {name}",
                    url=f"tg://user?id={user.id}",
                    style=_COLORS[i % 3],
                )
            )

        invited_str = " & ".join(invited_mentions) if invited_mentions else "someone"

        text = random.choice(_INVITE_MSGS).format(
            inviter=inviter_mention,
            invited=invited_str,
        )

        # Build keyboard: invited user buttons + play music button
        rows = []
        # group invited buttons 2 per row
        for i in range(0, len(invited_buttons), 2):
            rows.append(invited_buttons[i:i+2])
        rows.append([
            InlineKeyboardButton("🎵 Pʟᴀʏ Mᴜsɪᴄ", callback_data="cb_play_instruction", style=_G),
            InlineKeyboardButton("🎤 Jᴏɪɴ VC", callback_data="cb_join_vc_tip", style=_B),
        ])

        await message.reply(
            text,
            reply_markup=InlineKeyboardMarkup(rows),
        )
    except Exception:
        pass


# ── VC invite button callbacks ─────────────────────────────────────────────────
@app.on_callback_query(filters.regex("^cb_play_instruction$"))
async def cb_play_instruction(_, cq):
    await cq.answer(
        "🎵 Gʀᴏᴜᴘ ᴍᴇɪɴ /play <song name> ʟɪᴋʜᴏ!",
        show_alert=True,
    )


@app.on_callback_query(filters.regex("^cb_join_vc_tip$"))
async def cb_join_vc_tip(_, cq):
    await cq.answer(
        "🎤 VC ᴊᴏɪɴ ᴋᴀʀᴏ ᴀᴜʀ ᴍᴜsɪᴄ sᴜɴᴏ! 🎶",
        show_alert=True,
    )


@app.on_message(filters.command("math"))
async def calculate_math(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage:\n`/math 2+2`", quote=True)
    expression = message.text.split(None, 1)[1]
    try:
        result = eval(expression)
        response = f"✅ **Result:** `{result}`"
    except Exception:
        response = "❌ **Invalid expression**"
    await message.reply_text(response, quote=True)


@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def bot_leave(_, message: Message):
    await message.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ !!")
    await app.leave_chat(chat_id=message.chat.id, delete=True)


@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `/spg <query>`", quote=True)

    query = message.text.split(None, 1)[1]
    msg = await message.reply("Searching...")
    start = 1

    async with aiohttp.ClientSession() as session:
        url = (
            f"https://content-customsearch.googleapis.com/customsearch/v1"
            f"?cx=ec8db9e1f9e41e65e&q={query}"
            f"&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}"
        )
        async with session.get(url, headers={"x-referer": "https://explorer.apis.google.com"}) as r:
            response = await r.json()

    if not response.get("items"):
        return await msg.edit_text("No results found!")

    result = ""
    seen = set()
    for item in response["items"]:
        title = item["title"]
        link = item["link"]
        if "/s" in link:
            link = link.replace("/s", "")
        elif re.search(r"\/\d", link):
            link = re.sub(r"\/\d", "", link)
        if "?" in link:
            link = link.split("?")[0]
        if link in seen:
            continue
        seen.add(link)
        result += f"{title}\n{link}\n\n"

    next_btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ Next ▶️", callback_data=f"spg_next {start + 10} {query}")]]
    )
    await msg.edit_text(result, reply_markup=next_btn, disable_web_page_preview=True)
