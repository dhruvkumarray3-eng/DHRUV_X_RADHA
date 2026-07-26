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
from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from strings import get_string, helpers
from SHUKLAMUSIC import app
from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.utils.database import add_sudo, remove_sudo
from SHUKLAMUSIC.utils.decorators.language import language
from SHUKLAMUSIC.utils.extraction import extract_user
from SHUKLAMUSIC.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID

_G = ButtonStyle.SUCCESS   # 🟢
_R = ButtonStyle.DANGER    # 🔴
_B = ButtonStyle.PRIMARY   # 🔵


@app.on_message(filters.command(["addsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["delsudo", "rmsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


# ── /sudolist  ─  OWNER ONLY ─────────────────────────────────────────────────
@app.on_message(
    filters.command(["sudolist", "listsudo", "sudoers"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
    & filters.user(OWNER_ID)
)
async def sudoers_list(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👁 ᴠɪᴇᴡ sᴜᴅᴏ ʟɪsᴛ", callback_data="check_sudo_list", style=_G)],
    ])
    await message.reply_video(
        video="https://files.catbox.moe/56u1wc.mp4",
        caption=(
            "**🔐 sᴜᴅᴏ ʟɪsᴛ — ᴏᴡɴᴇʀ ᴏɴʟʏ**\n\n"
            "**»** ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀᴋᴇ sᴜᴅᴏ ʟɪsᴛ ᴅᴇᴋʜᴏ.\n\n"
            "**» ɴᴏᴛᴇ:** ʏᴇ ꜱɪʀꜰ ʙᴏᴛ ᴏᴡɴᴇʀ ᴅᴇᴋʜ ꜱᴀᴋᴛᴀ ʜᴀɪ. 🔒"
        ),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("^check_sudo_list$"))
async def check_sudo_list(client, callback_query: CallbackQuery):
    # 🔒 OWNER ONLY — no admin, no sudo user can view this
    if callback_query.from_user.id != OWNER_ID:
        return await callback_query.answer(
            "🔒 ʏᴇ ꜱɪʀꜰ ʙᴏᴛ ᴏᴡɴᴇʀ ᴅᴇᴋʜ ꜱᴀᴋᴛᴀ ʜᴀɪ!\n🚫 ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ.",
            show_alert=True,
        )

    owner_user = await app.get_users(OWNER_ID)
    owner_mention = owner_user.first_name if not owner_user.mention else owner_user.mention
    caption = f"**˹ ʟɪꜱᴛ ᴏꜰ ʙᴏᴛ ᴍᴏᴅᴇʀᴀᴛᴏʀꜱ ˼**\n\n**🌹 Oᴡɴᴇʀ** ➥ {owner_mention}\n\n"

    keyboard = [
        [InlineKeyboardButton("🌹 ᴠɪᴇᴡ ᴏᴡɴᴇʀ", url=f"tg://openmessage?user_id={OWNER_ID}", style=_G)],
    ]

    count = 1
    _COLORS = [_B, _R, _G]
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user_mention = user.mention if user else f"**🎁 Sᴜᴅᴏ {count} ɪᴅ:** {user_id}"
                caption += f"**🎁 Sᴜᴅᴏ {count} »** {user_mention}\n"
                color = _COLORS[(count - 1) % 3]
                keyboard.append([
                    InlineKeyboardButton(
                        f"🎁 ᴠɪᴇᴡ sᴜᴅᴏ {count}",
                        url=f"tg://openmessage?user_id={user_id}",
                        style=color,
                    )
                ])
                count += 1
            except Exception:
                continue

    keyboard.append([InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_main_menu", style=_B)])
    await callback_query.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex("^back_to_main_menu$"))
async def back_to_main_menu(client, callback_query: CallbackQuery):
    # Also owner-only
    if callback_query.from_user.id != OWNER_ID:
        return await callback_query.answer("🔒 ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ.", show_alert=True)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👁 ᴠɪᴇᴡ sᴜᴅᴏ ʟɪsᴛ", callback_data="check_sudo_list", style=_G)],
    ])
    await callback_query.message.edit_caption(
        caption=(
            "**🔐 sᴜᴅᴏ ʟɪsᴛ — ᴏᴡɴᴇʀ ᴏɴʟʏ**\n\n"
            "**»** ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀᴋᴇ sᴜᴅᴏ ʟɪsᴛ ᴅᴇᴋʜᴏ.\n\n"
            "**» ɴᴏᴛᴇ:** ʏᴇ ꜱɪʀꜰ ʙᴏᴛ ᴏᴡɴᴇʀ ᴅᴇᴋʜ ꜱᴀᴋᴛᴀ ʜᴀɪ. 🔒"
        ),
        reply_markup=keyboard,
    )


@app.on_message(filters.command(["delallsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def del_all_sudo(client, message: Message, _):
    count = len(SUDOERS) - 1
    for user_id in SUDOERS.copy():
        if user_id != OWNER_ID:
            removed = await remove_sudo(user_id)
            if removed:
                SUDOERS.remove(user_id)
                count -= 1
    await message.reply_text(f"✅ Removed {count} users from the sudo list.")
