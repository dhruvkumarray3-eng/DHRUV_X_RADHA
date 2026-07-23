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
from typing import Union
from pyrogram import filters, types
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils import help_pannel, bot_sys_stats
from SHUKLAMUSIC.utils.database import get_lang, get_served_chats, get_served_users
from SHUKLAMUSIC.utils.decorators.language import LanguageStart, languageCB
from SHUKLAMUSIC.utils.inline.help import (
    help_back_markup, private_help_panel,
    help_pannel_page1, help_pannel_page2, help_pannel_page3, help_pannel_page4,
)
from SHUKLAMUSIC.utils.inline.start import private_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT, SHASHANK_IMG, START_PICS
from strings import get_string, helpers
from SHUKLAMUSIC.utils.stuffs.buttons import BUTTONS
from SHUKLAMUSIC.utils.stuffs.helper import Helper

EFFECT_IDS = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]

@app.on_callback_query(filters.regex("^show_help_private$") & ~BANNED_USERS)
async def show_help_private_cb(client, CallbackQuery):
    """Help & Commands button from the start/home panel — show the actual help panel."""
    try:
        await CallbackQuery.answer()
    except:
        pass
    language = await get_lang(CallbackQuery.message.chat.id)
    _ = get_string(language)
    keyboard = help_pannel(_)
    await CallbackQuery.message.delete()
    await client.send_photo(
        chat_id=CallbackQuery.message.chat.id,
        photo=random.choice(SHASHANK_IMG),
        caption=_["help_1"].format(SUPPORT_CHAT),
        reply_markup=keyboard,
    )


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        # DM → go back to home page
        if update.message.chat.type == ChatType.PRIVATE:
            UP, CPU, RAM, DISK = await bot_sys_stats()
            served_chats = len(await get_served_chats())
            served_users = len(await get_served_users())
            caption = _["start_2"].format(
                update.from_user.mention, app.mention,
                UP, DISK, CPU, RAM, served_users, served_chats,
            )
            await update.message.delete()
            await client.send_photo(
                chat_id=chat_id,
                photo=random.choice(START_PICS),
                has_spoiler=True,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(private_panel(_)),
            )
        else:
            keyboard = help_pannel(_, True)
            await update.edit_message_text(
                _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
            )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            random.choice(SHASHANK_IMG),
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )

@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"], 
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    if cb == "hb1":
        await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
    elif cb == "hb7":
        await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
    elif cb == "hb9":
        await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
    elif cb == "hb12":
        await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)
    elif cb == "hb13":
        await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)
    elif cb == "hb14":
        await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)
    elif cb == "hb15":
        await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)
    elif cb == "hb16":
        await CallbackQuery.edit_message_text(helpers.HELP_16, reply_markup=keyboard)
    elif cb == "hb17":
        await CallbackQuery.edit_message_text(helpers.HELP_17, reply_markup=keyboard)
    elif cb == "hb18":
        await CallbackQuery.edit_message_text(helpers.HELP_18, reply_markup=keyboard)
    elif cb == "hb19":
        await CallbackQuery.edit_message_text(helpers.HELP_19, reply_markup=keyboard)
    elif cb == "hb20":
        await CallbackQuery.edit_message_text(helpers.HELP_20, reply_markup=keyboard)
    elif cb == "hb21":
        await CallbackQuery.edit_message_text(helpers.HELP_21, reply_markup=keyboard)
    elif cb == "hb22":
        await CallbackQuery.edit_message_text(helpers.HELP_22, reply_markup=help_back_markup(_, 3))
    elif cb == "hb23":
        await CallbackQuery.edit_message_text(helpers.HELP_23, reply_markup=help_back_markup(_, 3))
    elif cb == "hb24":
        await CallbackQuery.edit_message_text(helpers.HELP_24, reply_markup=help_back_markup(_, 3))
    elif cb == "hb25":
        await CallbackQuery.edit_message_text(helpers.HELP_25, reply_markup=help_back_markup(_, 3))
    elif cb == "hb26":
        await CallbackQuery.edit_message_text(helpers.HELP_26, reply_markup=help_back_markup(_, 3))
    elif cb == "hb27":
        await CallbackQuery.edit_message_text(helpers.HELP_27, reply_markup=help_back_markup(_, 3))
    elif cb == "hb28":
        await CallbackQuery.edit_message_text(helpers.HELP_28, reply_markup=help_back_markup(_, 3))
    elif cb == "hb29":
        await CallbackQuery.edit_message_text(helpers.HELP_29, reply_markup=help_back_markup(_, 3))
    elif cb == "hb30":
        await CallbackQuery.edit_message_text(helpers.HELP_30, reply_markup=help_back_markup(_, 3))
    elif cb == "hb31":
        await CallbackQuery.edit_message_text(helpers.HELP_31, reply_markup=help_back_markup(_, 3))
    elif cb == "hb32":
        await CallbackQuery.edit_message_text(helpers.HELP_32, reply_markup=help_back_markup(_, 4))
    elif cb == "hb33":
        await CallbackQuery.edit_message_text(helpers.HELP_33, reply_markup=help_back_markup(_, 4))
    elif cb == "hb34":
        await CallbackQuery.edit_message_text(helpers.HELP_34, reply_markup=help_back_markup(_, 4))
    elif cb == "hb35":
        await CallbackQuery.edit_message_text(helpers.HELP_35, reply_markup=help_back_markup(_, 4))
    elif cb == "hb36":
        await CallbackQuery.edit_message_text(helpers.HELP_36, reply_markup=help_back_markup(_, 4))
    elif cb == "hb37":
        await CallbackQuery.edit_message_text(helpers.HELP_37, reply_markup=help_back_markup(_, 4))


@app.on_callback_query(filters.regex("^help_page_") & ~BANNED_USERS)
@languageCB
async def help_page_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    page = CallbackQuery.data.strip()
    if page == "help_page_1":
        keyboard = help_pannel_page1(_)
    elif page == "help_page_2":
        keyboard = help_pannel_page2(_)
    elif page == "help_page_3":
        keyboard = help_pannel_page3(_)
    elif page == "help_page_4":
        keyboard = help_pannel_page4(_)
    else:
        keyboard = help_pannel_page1(_)
    language = await get_lang(CallbackQuery.message.chat.id)
    _ = get_string(language)
    try:
        from config import SUPPORT_CHAT
        await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )
    except Exception:
        await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex("mbot_cb") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(Helper.HELP_M, reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON))


@app.on_callback_query(filters.regex('managebot123'))
async def on_back_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_pannel(_, True)
    if cb == "settings_back_helper":
        await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )

@app.on_callback_query(filters.regex('mplus'))      
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    from pyrogram.enums import ButtonStyle
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="mbot_cb", style=ButtonStyle.PRIMARY)]])
    if cb == "Okieeeeee":
        await CallbackQuery.edit_message_text(f"`something errors`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await CallbackQuery.edit_message_text(getattr(Helper, cb), reply_markup=keyboard)