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
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import *
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.utils import bot_sys_stats
from SHUKLAMUSIC.utils.decorators.language import language
from SHUKLAMUSIC.utils.inline import supp_markup
from config import BANNED_USERS, PING_VIDEO_URL
from SHUKLAMUSIC.utils.branding import BRAND_LINK, POWERED_BY
import random


@app.on_message(filters.command("ping", prefixes=["/"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_video(
        PING_VIDEO_URL,
        caption=f"{_['ping_1'].format(app.mention)}\n\n{POWERED_BY}",
        supports_streaming=True,
    )
    pytgping = await SHUKLA.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    caption = _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping)
    caption = caption.replace("https://t.me/II_NOBITA_X_PRIME_II", BRAND_LINK)
    await response.edit_caption(
        caption=caption,
        reply_markup=supp_markup(_),
    )
