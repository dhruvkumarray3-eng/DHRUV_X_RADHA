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
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils.database import get_lang, set_lang
from SHUKLAMUSIC.utils.decorators import (
    ActualAdminCB,
    language,
    languageCB,
)
from config import BANNED_USERS
from strings import get_string, languages_present


from pyrogram.enums import ButtonStyle as _BS

_LANG_STYLES = [_BS.PRIMARY, _BS.SUCCESS, _BS.DANGER]

# Country / region / keyword → language code mapping
_COUNTRY_MAP = {
    # Arabic
    "iraq": "ar", "iraqi": "ar", "عراق": "ar",
    "saudi": "ar", "arabia": "ar", "arab": "ar",
    "egypt": "ar", "egyptian": "ar",
    "syria": "ar", "syrian": "ar",
    "jordan": "ar", "kuwait": "ar", "uae": "ar",
    "qatar": "ar", "bahrain": "ar", "oman": "ar",
    "lebanon": "ar", "libya": "ar", "morocco": "ar",
    "arabic": "ar", "عربي": "ar",
    # Hindi
    "india": "hi", "indian": "hi", "bharat": "hi",
    "hindi": "hi", "हिंदी": "hi",
    # Urdu
    "pakistan": "ur", "pakistani": "ur", "urdu": "ur", "اردو": "ur",
    # Punjabi
    "punjab": "pa", "punjabi": "pa", "ਪੰਜਾਬੀ": "pa",
    # Bengali
    "bangladesh": "bn", "bengal": "bn", "bengali": "bn", "bangla": "bn",
    # Telugu
    "telugu": "te", "andhra": "te", "telangana": "te",
    # Tamil
    "tamil": "ta", "tamilnadu": "ta", "srilanka": "ta",
    # Marathi
    "marathi": "mr", "maharashtra": "mr",
    # Gujarati
    "gujarati": "gu", "gujarat": "gu",
    # Malayalam
    "malayalam": "ml", "kerala": "ml",
    # Kannada
    "kannada": "kn", "karnataka": "kn",
    # Spanish
    "spain": "es", "spanish": "es", "mexico": "es", "colombia": "es",
    "argentina": "es", "español": "es",
    # Russian
    "russia": "ru", "russian": "ru", "русский": "ru",
    # Turkish
    "turkey": "tr", "turkish": "tr", "türkiye": "tr",
    # Indonesian
    "indonesia": "id", "indonesian": "id",
    # French
    "france": "fr", "french": "fr", "français": "fr",
    # English
    "english": "en", "uk": "en", "usa": "en", "america": "en",
}


def lanuages_keyboard(_, filter_query: str = ""):
    """Build language keyboard, optionally filtered by search query."""
    query = filter_query.strip().lower()

    # Country name → resolve to language code
    resolved_code = _COUNTRY_MAP.get(query)

    lang_list = [
        k for k in languages_present.keys()
        if not query
        or (resolved_code and k == resolved_code)
        or query in k.lower()
        or query in languages_present[k].lower()
    ]

    buttons = [
        InlineKeyboardButton(
            text=languages_present[i],
            callback_data=f"languages:{i}",
            style=_LANG_STYLES[idx % len(_LANG_STYLES)],
        )
        for idx, i in enumerate(lang_list)
    ]

    keyboard = []
    for i in range(0, len(buttons), 2):
        keyboard.append(buttons[i:i + 2])

    keyboard.append(
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settingsback_helper",
                style=_BS.SUCCESS,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=_BS.DANGER,
            ),
        ]
    )

    return InlineKeyboardMarkup(keyboard), len(lang_list)


@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    # Support: /lang <search> to filter languages
    query = ""
    if len(message.command) > 1:
        query = " ".join(message.command[1:])

    keyboard, count = lanuages_keyboard(_, filter_query=query)

    total = len(languages_present)
    if query:
        header = (
            f"🔍 <b>Search:</b> <code>{query}</code> — {count}/{total} language(s) found\n\n"
            + _["lang_1"]
        )
    else:
        header = f"🌐 <b>{total} languages available</b>\n\n" + _["lang_1"] + \
                 "\n\n💡 <i>Tip: Use <code>/lang &lt;name&gt;</code> to search. E.g. <code>/lang hindi</code></i>"

    if count == 0:
        return await message.reply_text(
            f"❌ No language found for <code>{query}</code>.\n\nUse /lang to see all languages."
        )

    await message.reply_text(header, reply_markup=keyboard)


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except Exception:
        pass

    keyboard, _ = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = CallbackQuery.data.split(":")[1]

    old = await get_lang(CallbackQuery.message.chat.id)

    if str(old) == str(langauge):
        return await CallbackQuery.answer(
            _["lang_4"],
            show_alert=True,
        )

    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(
            _["lang_2"],
            show_alert=True,
        )
    except Exception:
        _ = get_string(old)
        return await CallbackQuery.answer(
            _["lang_3"],
            show_alert=True,
        )

    await set_lang(
        CallbackQuery.message.chat.id,
        langauge,
    )

    keyboard, _ = lanuages_keyboard(_)

    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=keyboard
    )
