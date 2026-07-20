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
from pyrogram import filters, Client, enums
from pyrogram.enums import ButtonStyle
from SHUKLAMUSIC import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.types import ChatPermissions
from SHUKLAMUSIC.mongo.nightmodedb import nightdb, nightmode_on, nightmode_off, get_nightchats 


CLOSE_CHAT = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_change_info=False,
    can_add_web_page_previews=False,
    can_pin_messages=False,
    can_invite_users=False
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=True,
    can_add_web_page_previews=True,
    can_pin_messages=True,
    can_invite_users=True
)

buttons = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton("๏ ᴇɴᴀʙʟᴇ ๏", callback_data="add_night", style=ButtonStyle.SUCCESS),
        InlineKeyboardButton("๏ ᴅɪsᴀʙʟᴇ ๏", callback_data="rm_night", style=ButtonStyle.DANGER),
    ]]
)

@app.on_message(filters.command("nightmode") & filters.group)
async def _nightmode(_, message):
    return await message.reply_photo(
        photo="https://telegra.ph//file/06649d4d0bbf4285238ee.jpg",
        caption="**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ɴɪɢʜᴛᴍᴏᴅᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**",
        reply_markup=buttons
    )


@app.on_callback_query(filters.regex("^(add_night|rm_night)$"))
async def nightcb(_, query: CallbackQuery):
    data = query.data 
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    check_night = await nightdb.find_one({"chat_id": chat_id})

    administrators = []
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m.user.id)

    if user_id not in administrators:
        return await query.answer("❌ Only admins can use this!", show_alert=True)

    if data == "add_night":
        if check_night:
            await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
        else:
            await nightmode_on(chat_id)
            await query.message.edit_caption(
                "**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ᴇɴᴀʙʟᴇᴅ!\n\n"
                "ɢʀᴏᴜᴘ ᴡɪʟʟ ᴄʟᴏsᴇ ᴀᴛ 12ᴀᴍ ᴀɴᴅ ᴏᴘᴇɴ ᴀᴛ 06ᴀᴍ [IST].**"
            )

    elif data == "rm_night":
        if check_night:
            await nightmode_off(chat_id)
            await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ᴅɪsᴀʙʟᴇᴅ!**")
        else:
            await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ᴀʟʀᴇᴀᴅʏ ᴏғғ.**")


async def start_nightmode():
    schats = await get_nightchats()
    for chat in schats:
        chat_id = int(chat["chat_id"])
        try:
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph//file/06649d4d0bbf4285238ee.jpg",
                caption="**ᴍᴀʏ ᴛʜᴇ ᴀɴɢᴇʟs ғʀᴏᴍ ʜᴇᴀᴠᴇɴ ʙʀɪɴɢ ᴛʜᴇ sᴡᴇᴇᴛᴇsᴛ ᴏғ ᴀʟʟ ᴅʀᴇᴀᴍs ғᴏʀ ʏᴏᴜ. ᴍᴀʏ ʏᴏᴜ ʜᴀᴠᴇ ʟᴏɴɢ ᴀɴᴅ ʙʟɪssғᴜʟ sʟᴇᴇᴘ ғᴜʟʟ ᴏғ ʜᴀᴘᴘʏ ᴅʀᴇᴀᴍs.\n\nɢʀᴏᴜᴘ ɪs ᴄʟᴏsɪɴɢ ɢᴏᴏᴅ ɴɪɢʜᴛ ᴇᴠᴇʀʏᴏɴᴇ  !**"
            )
            await app.set_chat_permissions(chat_id, CLOSE_CHAT)
        except Exception as e:
            print(f"Unable to close group {chat_id}: {e}")


async def close_nightmode():
    schats = await get_nightchats()
    for chat in schats:
        chat_id = int(chat["chat_id"])
        try:
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph//file/14ec9c3ff42b59867040a.jpg",
                caption="**ɢʀᴏᴜᴘ ɪs ᴏᴘᴇɴɪɴɢ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴇᴠᴇʀʏᴏɴᴇ !\n\nᴍᴀʏ ᴛʜɪs ᴅᴀʏ ᴄᴏᴍᴇ ᴡɪᴛʜ ᴀʟʟ ᴛʜᴇ ʟᴏᴠᴇ ʏᴏᴜʀ ʜᴇᴀʀᴛ ᴄᴀɴ ʜᴏʟᴅ ᴀɴᴅ ʙʀɪɴɢ ʏᴏᴜ ᴇᴠᴇʀʏ sᴜᴄᴄᴇss ʏᴏᴜ ᴅᴇsɪʀᴇ. Mᴀʏ ᴇᴀᴄʜ ᴏғ ʏᴏᴜʀ ғᴏᴏᴛsᴛᴇᴘs ʙʀɪɴɢ Jᴏʏ ᴛᴏ ᴛʜᴇ ᴇᴀʀᴛʜ ᴀɴᴅ ʏᴏᴜʀsᴇʟғ. ɪ ᴡɪsʜ ʏᴏᴜ ᴀ ᴍᴀɢɪᴄᴀʟ ᴅᴀʏ ᴀɴᴅ ᴀ ᴡᴏɴᴅᴇʀғᴜʟ ʟɪғᴇ ᴀʜᴇᴀᴅ.**"
            )
            await app.set_chat_permissions(chat_id, OPEN_CHAT)
        except Exception as e:
            print(f"Unable to open group {chat_id}: {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(start_nightmode, trigger="cron", hour=23, minute=59)
scheduler.add_job(close_nightmode, trigger="cron", hour=6, minute=1)
scheduler.start()
