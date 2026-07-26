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

# Country / region / keyword → language code mapping (180+ countries/regions)
_COUNTRY_MAP = {
    # ── Arabic (ar) ────────────────────────────────────────────────────────
    "iraq": "ar", "iraqi": "ar", "عراق": "ar",
    "saudi": "ar", "saudi arabia": "ar", "arabia": "ar", "arab": "ar",
    "egypt": "ar", "egyptian": "ar", "مصر": "ar",
    "syria": "ar", "syrian": "ar", "سوريا": "ar",
    "jordan": "ar", "jordanian": "ar",
    "kuwait": "ar", "kuwaiti": "ar",
    "uae": "ar", "emirates": "ar", "dubai": "ar", "abu dhabi": "ar",
    "qatar": "ar", "bahrain": "ar", "oman": "ar",
    "lebanon": "ar", "lebanese": "ar",
    "libya": "ar", "libyan": "ar",
    "morocco": "ar", "moroccan": "ar", "المغرب": "ar",
    "algeria": "ar", "algerian": "ar",
    "tunisia": "ar", "tunisian": "ar",
    "sudan": "ar", "sudanese": "ar",
    "yemen": "ar", "yemeni": "ar",
    "somalia": "ar",
    "mauritania": "ar",
    "djibouti": "ar",
    "comoros": "ar",
    "arabic": "ar", "عربي": "ar", "عربية": "ar",

    # ── Hindi (hi) ─────────────────────────────────────────────────────────
    "india": "hi", "indian": "hi", "bharat": "hi",
    "hindi": "hi", "हिंदी": "hi", "हिन्दी": "hi",
    "uttar pradesh": "hi", "rajasthan": "hi", "madhya pradesh": "hi",
    "bihar": "hi", "haryana": "hi", "delhi": "hi", "uttarakhand": "hi",
    "jharkhand": "hi", "chhattisgarh": "hi", "himachal pradesh": "hi",

    # ── Urdu (ur) ──────────────────────────────────────────────────────────
    "pakistan": "ur", "pakistani": "ur", "urdu": "ur", "اردو": "ur",
    "پاکستان": "ur",

    # ── Punjabi (pa) ───────────────────────────────────────────────────────
    "punjab": "pa", "punjabi": "pa", "ਪੰਜਾਬੀ": "pa",

    # ── Bengali (bn) ───────────────────────────────────────────────────────
    "bangladesh": "bn", "bengal": "bn", "bengali": "bn", "bangla": "bn",
    "west bengal": "bn", "বাংলাদেশ": "bn", "বাংলা": "bn",

    # ── Telugu (te) ────────────────────────────────────────────────────────
    "telugu": "te", "andhra": "te", "telangana": "te",
    "andhra pradesh": "te", "తెలుగు": "te",

    # ── Tamil (ta) ─────────────────────────────────────────────────────────
    "tamil": "ta", "tamilnadu": "ta", "tamil nadu": "ta",
    "srilanka": "ta", "sri lanka": "ta", "தமிழ்": "ta",

    # ── Marathi (mr) ───────────────────────────────────────────────────────
    "marathi": "mr", "maharashtra": "mr", "मराठी": "mr",

    # ── Gujarati (gu) ──────────────────────────────────────────────────────
    "gujarati": "gu", "gujarat": "gu", "ગુજરાતી": "gu",

    # ── Malayalam (ml) ─────────────────────────────────────────────────────
    "malayalam": "ml", "kerala": "ml", "മലയാളം": "ml",

    # ── Kannada (kn) ───────────────────────────────────────────────────────
    "kannada": "kn", "karnataka": "kn", "ಕನ್ನಡ": "kn",

    # ── Spanish (es) ───────────────────────────────────────────────────────
    "spain": "es", "spanish": "es", "español": "es",
    "mexico": "es", "méxico": "es",
    "colombia": "es", "colombian": "es",
    "argentina": "es", "argentinian": "es",
    "peru": "es", "perú": "es",
    "venezuela": "es", "venezuelan": "es",
    "chile": "es", "chilean": "es",
    "ecuador": "es",
    "bolivia": "es",
    "paraguay": "es",
    "uruguay": "es",
    "cuba": "es", "cuban": "es",
    "dominican republic": "es",
    "honduras": "es",
    "el salvador": "es",
    "nicaragua": "es",
    "costa rica": "es",
    "panama": "es",
    "guatemala": "es",
    "puerto rico": "es",

    # ── Russian (ru) ───────────────────────────────────────────────────────
    "russia": "ru", "russian": "ru", "русский": "ru", "россия": "ru",
    "belarus": "ru", "belarusian": "ru", "беларусь": "ru",
    "kazakhstan": "ru", "казахстан": "ru",
    "kyrgyzstan": "ru", "kyrgyz": "ru",
    "tajikistan": "ru",
    "moldova": "ru",

    # ── Turkish (tr) ───────────────────────────────────────────────────────
    "turkey": "tr", "turkish": "tr", "türkiye": "tr", "türkçe": "tr",
    "türk": "tr",

    # ── Indonesian (id) ────────────────────────────────────────────────────
    "indonesia": "id", "indonesian": "id", "bahasa": "id",
    "jakarta": "id", "bali": "id", "java": "id",

    # ── French (fr) ────────────────────────────────────────────────────────
    "france": "fr", "french": "fr", "français": "fr",
    "belgium": "fr", "switzerland": "fr",
    "canada french": "fr", "québec": "fr", "quebec": "fr",
    "senegal": "fr", "ivory coast": "fr", "cameroon": "fr",
    "mali": "fr", "burkina faso": "fr", "niger": "fr",
    "chad": "fr", "guinea": "fr", "benin": "fr", "togo": "fr",
    "madagascar": "fr", "congo": "fr", "gabon": "fr",
    "central african republic": "fr",
    "burundi": "fr", "rwanda": "fr",
    "haiti": "fr",

    # ── English (en) ───────────────────────────────────────────────────────
    "english": "en", "uk": "en", "united kingdom": "en",
    "usa": "en", "america": "en", "united states": "en",
    "australia": "en", "australian": "en",
    "canada": "en", "canadian": "en",
    "new zealand": "en",
    "ireland": "en", "irish": "en",
    "south africa": "en",
    "nigeria": "en", "nigerian": "en",
    "ghana": "en", "ghanaian": "en",
    "kenya": "en", "kenyan": "en",
    "uganda": "en",
    "tanzania": "en",
    "zimbabwe": "en",
    "zambia": "en",
    "botswana": "en",
    "namibia": "en",
    "sierra leone": "en",
    "liberia": "en",
    "gambia": "en",
    "singapore": "en",
    "philippines": "en", "filipino": "en",
    "malaysia": "en", "malaysian": "en",
    "myanmar": "en", "burma": "en",
    "jamaica": "en",
    "trinidad": "en",
    "barbados": "en",
    "guyana": "en",
    "belize": "en",
    "papua new guinea": "en",
    "fiji": "en",
    "solomon islands": "en",
    "vanuatu": "en",
    "samoa": "en",
    "tonga": "en",
    "kiribati": "en",
    "nauru": "en",
    "tuvalu": "en",
    "palau": "en",
    "marshall islands": "en",
    "micronesia": "en",
    # Countries that default to English (no specific language file)
    "china": "en", "chinese": "en",
    "japan": "en", "japanese": "en",
    "korea": "en", "korean": "en",
    "vietnam": "en", "vietnamese": "en",
    "thailand": "en", "thai": "en",
    "cambodia": "en", "khmer": "en",
    "laos": "en",
    "nepal": "en", "nepali": "en",
    "bhutan": "en",
    "maldives": "en",
    "afghanistan": "en",
    "iran": "en", "persian": "en", "farsi": "en",
    "ethiopia": "en", "ethiopian": "en",
    "eritrea": "en",
    "mozambique": "en",
    "angola": "en",
    "malawi": "en",
    "rwanda english": "en",
    "lesotho": "en",
    "eswatini": "en", "swaziland": "en",
    "germany": "en", "german": "en",
    "italy": "en", "italian": "en",
    "portugal": "en", "portuguese": "en",
    "netherlands": "en", "dutch": "en",
    "sweden": "en", "swedish": "en",
    "norway": "en", "norwegian": "en",
    "denmark": "en", "danish": "en",
    "finland": "en", "finnish": "en",
    "poland": "en", "polish": "en",
    "ukraine": "en", "ukrainian": "en",
    "czech republic": "en", "czechia": "en",
    "slovakia": "en",
    "hungary": "en", "hungarian": "en",
    "romania": "en", "romanian": "en",
    "bulgaria": "en", "bulgarian": "en",
    "croatia": "en", "croatian": "en",
    "serbia": "en", "serbian": "en",
    "bosnia": "en",
    "albania": "en",
    "north macedonia": "en",
    "kosovo": "en",
    "montenegro": "en",
    "slovenia": "en",
    "estonia": "en",
    "latvia": "en",
    "lithuania": "en",
    "georgia (country)": "en",
    "armenia": "en",
    "azerbaijan": "en",
    "uzbekistan": "en",
    "turkmenistan": "en",
    "mongolia": "en",
    "north korea": "en",
    "taiwan": "en",
    "hong kong": "en",
    "macau": "en",
    "brunei": "en",
    "timor-leste": "en",
    "israel": "en",
    "cyprus": "en",
    "malta": "en",
    "iceland": "en",
    "luxembourg": "en",
    "andorra": "en",
    "monaco": "en",
    "liechtenstein": "en",
    "san marino": "en",
    "vatican": "en",
    "austria": "en",
    "greece": "en", "greek": "en",
    "brazil": "en", "brazilian": "en",
    "suriname": "en",
    "mexico city": "es",
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
