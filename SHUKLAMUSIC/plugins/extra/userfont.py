# -----------------------------------------------
# 🔸 Nobita X Prime — User Font Preference Plugin
# -----------------------------------------------
from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS

user_font_prefs = mongodb.user_font_prefs

# ── Color cycle: green → red → blue ──────────────────────────────────────────
_G = ButtonStyle.SUCCESS   # 🟢
_R = ButtonStyle.DANGER    # 🔴
_B = ButtonStyle.PRIMARY   # 🔵
_CYCLE = [_G, _R, _B]

# ── All 41 fonts (key, display_label) ─────────────────────────────────────────
FONT_OPTIONS = [
    ("typewriter",   "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛"),
    ("outline",      "𝕆𝕦𝕥𝕝𝕚𝕟𝕖"),
    ("serief",       "𝐒𝐞𝐫𝐢𝐟 𝐁𝐨𝐥𝐝"),
    ("bold_cool",    "𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄"),
    ("cool",         "𝑆𝑒𝑟𝑖𝑓 𝐼𝑡𝑎𝑙𝑖𝑐"),
    ("smallcap",     "Sᴍᴀʟʟ Cᴀᴘs"),
    ("script",       "𝓈𝒸𝓇𝒾𝓅𝓉"),
    ("bold_script",  "𝓼𝓬𝓻𝓲𝓹𝓽 𝓑𝓸𝓵𝓭"),
    ("tiny",         "ᵗⁱⁿʸ"),
    ("comic",        "ᑕOᗰIᑕ"),
    ("san",          "𝗦𝗮𝗻𝘀 𝗕𝗼𝗹𝗱"),
    ("slant_san",    "𝙎𝙡𝙖𝙣𝙩 𝙎𝙖𝙣𝙨"),
    ("slant",        "𝘚𝘭𝘢𝘯𝘵"),
    ("sim",          "𝖲𝗂𝗆𝗉𝗅𝖾"),
    ("circles",      "Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ"),
    ("dark_circle",  "🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎"),
    ("gothic",       "𝔊𝔬𝔱𝔥𝔦𝔠"),
    ("bold_gothic",  "𝕲𝖔𝖙𝖍𝖎𝖈 𝕭𝖔𝖑𝖉"),
    ("cloud",        "C͜͡l͜͡o͜͡u͜͡d͜͡s"),
    ("happy",        "H̆̈ă̈p̆̈p̆̈y̆̈"),
    ("sad",          "S̑̈ȃ̈d̑̈"),
    ("special",      "🇸🇵🇪🇨🇮🇦🇱"),
    ("square",       "🅂🅀🅄🄰🅁🄴"),
    ("dark_square",  "🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎"),
    ("andalucia",    "ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ"),
    ("manga",        "爪卂几ᘜ卂"),
    ("stinky",       "S̾t̾i̾n̾k̾y̾"),
    ("bubbles",      "B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs"),
    ("underline",    "U͟n͟d͟e͟r͟l͟i͟n͟e͟"),
    ("ladybug",      "꒒ꍏꀷꌩꌃꀎꁅ"),
    ("rays",         "R҉a҉y҉s҉"),
    ("birds",        "B҈i҈r҈d҈s҈"),
    ("slash",        "S̸l̸a̸s̸h̸"),
    ("stop",         "s⃠t⃠o⃠p⃠"),
    ("skyline",      "S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆"),
    ("arrows",       "A͎r͎r͎o͎w͎s͎"),
    ("rvnes",        "ዪሀክቿነ"),
    ("strike",       "S̶t̶r̶i̶k̶e̶"),
    ("frozen",       "F༙r༙o༙z༙e༙n༙"),
    ("fullwidth",    "Ｆｕｌｌｗｉｄｔｈ"),
    ("inverted",     "ᴉnʌǝɹʇǝp"),
]

# Preview strings — "NOBITA X PRIME" in each font style
FONT_PREVIEW = {
    "typewriter":  "𝙽𝙾𝙱𝙸𝚃𝙰 𝚇 𝙿𝚁𝙸𝙼𝙴",
    "outline":     "𝕹𝕺𝕭𝕴𝕿𝕬 𝖃 𝕻𝕽𝕴𝕸𝕰",
    "serief":      "𝐍𝐎𝐁𝐈𝐓𝐀 𝐗 𝐏𝐑𝐈𝐌𝐄",
    "bold_cool":   "𝑵𝑶𝑩𝑰𝑻𝑨 𝑿 𝑷𝑹𝑰𝑴𝑬",
    "cool":        "𝑁𝑂𝐵𝐼𝑇𝐴 𝑋 𝑃𝑅𝐼𝑀𝐸",
    "smallcap":    "ɴᴏʙɪᴛᴀ x ᴘʀɪᴍᴇ",
    "script":      "𝒩ℴ𝒷𝒾𝓉𝒶 𝒳 𝒫𝓇𝒾𝓂𝑒",
    "bold_script": "𝓝𝓞𝓑𝓘𝓣𝓐 𝓧 𝓟𝓡𝓘𝓜𝓔",
    "tiny":        "ᴺᴼᴮᴵᵀᴬ ˣ ᴾᴿᴵᴹᴱ",
    "comic":       "ᑎOᗷITᗩ ᙖ ᑭᖇIᗰE",
    "san":         "𝗡𝗢𝗕𝗜𝗧𝗔 𝗫 𝗣𝗥𝗜𝗠𝗘",
    "slant_san":   "𝙉𝙊𝘽𝙄𝙏𝘼 𝙓 𝙋𝙍𝙄𝙈𝙀",
    "slant":       "𝘕𝘖𝘉𝘐𝘛𝘈 𝘟 𝘗𝘙𝘐𝘔𝘌",
    "sim":         "𝖭𝖮𝖡𝖨𝖳𝖠 𝖷 𝖯𝖱𝖨𝖬𝖤",
    "circles":     "Ⓝ︎Ⓞ︎Ⓑ︎Ⓘ︎Ⓣ︎Ⓐ︎ Ⓧ︎ Ⓟ︎Ⓡ︎Ⓘ︎Ⓜ︎Ⓔ︎",
    "dark_circle": "🅝︎🅞︎🅑︎🅘︎🅣︎🅐︎ 🅧︎ 🅟︎🅡︎🅘︎🅜︎🅔︎",
    "gothic":      "𝔑𝔬𝔟𝔦𝔱𝔞 𝔛 𝔓𝔯𝔦𝔪𝔢",
    "bold_gothic": "𝕹𝖔𝖇𝖎𝖙𝖆 𝖃 𝕻𝖗𝖎𝖒𝖊",
    "cloud":       "N͜͡O͜͡B͜͡I͜͡T͜͡A͜͡ X͜͡ P͜͡R͜͡I͜͡M͜͡E͜͡",
    "happy":       "N̆̈Ŏ̈B̆̈Ĭ̈T̆̈Ă̈ X̆̈ P̆̈R̆̈Ĭ̈M̆̈Ĕ̈",
    "sad":         "N̑̈Ȏ̈B̑̈Ȋ̈T̑̈Ȃ̈ X̑̈ P̑̈Ȓ̈Ȋ̈M̑̈Ȇ̈",
    "special":     "🇳 🇴 🇧 🇮 🇹 🇦 🇽 🇵 🇷 🇮 🇲 🇪",
    "square":      "🄽🄾🄱🄸🅃🄰 🅇 🄿🅁🄸🄼🄴",
    "dark_square": "🅽🅾🅱🅸🆃🅰 🆇 🅿🆁🅸🅼🅴",
    "andalucia":   "ꪀꪮ᥇ꪱ𝓽ꪖ ꪲ ρꪱ꥓ꫀ",
    "manga":       "ᑎ口乃ノ丅卂 乂 卩尺ノ爪乇",
    "stinky":      "N̾o̾b̾i̾t̾a̾ X̾ P̾r̾i̾m̾e̾",
    "bubbles":     "N̥ͦo̥ͦb̥ͦi̥ͦt̥ͦḁͦ X̥ͦ P̥ͦr̥ͦi̥ͦm̥ͦe̥ͦ",
    "underline":   "N͟o͟b͟i͟t͟a͟ X͟ P͟r͟i͟m͟e͟",
    "ladybug":     "꒒ꍏꀷꀎꌃꀎꁅ ꊰ ꉣꋪꀤꂵꏂ",
    "rays":        "N҉o҉b҉i҉t҉a҉ X҉ P҉r҉i҉m҉e҉",
    "birds":       "N҈o҈b҈i҈t҈a҈ X҈ P҈r҈i҈m҈e҈",
    "slash":       "N̸o̸b̸i̸t̸a̸ X̸ P̸r̸i̸m̸e̸",
    "stop":        "N⃠o⃠b⃠i⃠t⃠a⃠ X⃠ P⃠r⃠i⃠m⃠e⃠",
    "skyline":     "N̺͆o̺͆b̺͆i̺͆t̺͆a̺͆ X̺͆ P̺͆r̺͆i̺͆m̺͆e̺͆",
    "arrows":      "N͎o͎b͎i͎t͎a͎ X͎ P͎r͎i͎m͎e͎",
    "rvnes":       "ክሀᵽᎥ𝓽ᵽ ᤱ ᵽ𝓻Ꭵꎭꏹ",
    "strike":      "N̶o̶b̶i̶t̶a̶ X̶ P̶r̶i̶m̶e̶",
    "frozen":      "N༙o༙b༙i༙t༙a༙ X༙ P༙r༙i༙m༙e༙",
    "fullwidth":   "Ｎｏｂｉｔａ Ｘ Ｐｒｉｍｅ",
    "inverted":    "Nobita X Prime",   # applied at runtime via invert map
}

# ── Custom font transformers for non-library fonts ───────────────────────────
_FULLWIDTH = {chr(c): chr(c + 0xFF01 - 0x21) for c in range(0x21, 0x7F)}
_FULLWIDTH[" "] = "\u3000"

_INVERT_MAP = {
    'a':'ɐ','b':'q','c':'ɔ','d':'p','e':'ǝ','f':'ɟ','g':'ƃ','h':'ɥ','i':'ᴉ','j':'ɾ',
    'k':'ʞ','l':'l','m':'ɯ','n':'u','o':'o','p':'d','q':'b','r':'ɹ','s':'s','t':'ʇ',
    'u':'n','v':'ʌ','w':'ʍ','x':'x','y':'ʎ','z':'z',
    'A':'∀','B':'ᗺ','C':'Ɔ','D':'ᗡ','E':'Ǝ','F':'ᖵ','G':'פ','H':'H','I':'I','J':'ſ',
    'K':'ʞ','L':'˥','M':'W','N':'N','O':'O','P':'Ԁ','Q':'Q','R':'ᴚ','S':'S','T':'┴',
    'U':'∩','V':'Λ','W':'M','X':'X','Y':'⅄','Z':'Z',
    '0':'0','1':'Ɩ','2':'ᄅ','3':'Ɛ','4':'ㄣ','5':'ϛ','6':'9','7':'ㄥ','8':'8','9':'6',
    '!':'¡','?':'¿','.':'˙',',':'\'','\'':',',
}


def apply_custom_font(text: str, font_key: str) -> str:
    """Apply fullwidth or inverted transform to a string."""
    if font_key == "fullwidth":
        return "".join(_FULLWIDTH.get(c, c) for c in text)
    if font_key == "inverted":
        return "".join(_INVERT_MAP.get(c, c) for c in reversed(text))
    return text


def _font_menu_keyboard(page: int = 1):
    """Build paginated font selection keyboard (12 fonts per page, 3 cols)."""
    PER_PAGE = 12
    start = (page - 1) * PER_PAGE
    chunk = FONT_OPTIONS[start: start + PER_PAGE]
    total_pages = (len(FONT_OPTIONS) + PER_PAGE - 1) // PER_PAGE

    rows = []
    for i in range(0, len(chunk), 3):
        row_fonts = chunk[i:i + 3]
        row = []
        for j, (key, label) in enumerate(row_fonts):
            global_idx = start + i + j
            color = _CYCLE[global_idx % 3]
            row.append(
                InlineKeyboardButton(
                    text=label,
                    callback_data=f"set_user_font:{key}",
                    style=color,
                )
            )
        rows.append(row)

    # Pagination row
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"font_page:{page-1}", style=_B))
    nav.append(InlineKeyboardButton(f"📄 {page}/{total_pages}", callback_data="font_page_noop", style=_G))
    if page < total_pages:
        nav.append(InlineKeyboardButton("➡️", callback_data=f"font_page:{page+1}", style=_B))
    if nav:
        rows.append(nav)

    rows.append([
        InlineKeyboardButton("❌ ɴᴏ ꜰᴏɴᴛ (ᴅᴇꜰᴀᴜʟᴛ)", callback_data="set_user_font:none", style=_R),
    ])
    rows.append([
        InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="help_page_4", style=_G),
    ])
    return InlineKeyboardMarkup(rows)


def _font_menu_text(current_font, page: int = 1) -> str:
    preview = FONT_PREVIEW.get(current_font, "ɴᴏʙɪᴛᴀ x ᴘʀɪᴍᴇ")
    if current_font == "fullwidth":
        preview = apply_custom_font("Nobita X Prime", "fullwidth")
    elif current_font == "inverted":
        preview = apply_custom_font("Nobita X Prime", "inverted")
    current_label = next((lbl for k, lbl in FONT_OPTIONS if k == current_font), "Default")
    total = len(FONT_OPTIONS)
    return (
        f"🔤 <b>Cʜᴏᴏsᴇ Yᴏᴜʀ Fᴏɴᴛ Sᴛʏʟᴇ</b>  <i>({total} fonts)</i>\n\n"
        f"📌 <b>Current:</b> {current_label}\n"
        f"👁 <b>Preview:</b> {preview}\n\n"
        "Pick a font — bot AI replies will use that style for you:\n"
        "💡 <i>Font applies to text replies (not code blocks).</i>"
    )


# ── /setmyfont command ─────────────────────────────────────────────────────────
@app.on_message(filters.command(["setmyfont", "myfont"]) & ~BANNED_USERS)
async def setmyfont_cmd(_, message: Message):
    if not message.from_user:
        return
    doc = await user_font_prefs.find_one({"user_id": message.from_user.id})
    current = doc.get("font") if doc else None
    await message.reply_text(
        _font_menu_text(current, 1),
        reply_markup=_font_menu_keyboard(1),
    )


# ── my_font_menu callback (from Help page 4) ──────────────────────────────────
@app.on_callback_query(filters.regex("^my_font_menu$") & ~BANNED_USERS)
async def my_font_menu_cb(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except Exception:
        pass
    current = None
    if cq.from_user:
        doc = await user_font_prefs.find_one({"user_id": cq.from_user.id})
        current = doc.get("font") if doc else None
    try:
        await cq.edit_message_text(
            _font_menu_text(current, 1),
            reply_markup=_font_menu_keyboard(1),
        )
    except Exception:
        await cq.message.reply_text(
            _font_menu_text(current, 1),
            reply_markup=_font_menu_keyboard(1),
        )


# ── font_page pagination callback ──────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^font_page:(\d+)$") & ~BANNED_USERS)
async def font_page_cb(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except Exception:
        pass
    page = int(cq.data.split(":")[1])
    current = None
    if cq.from_user:
        doc = await user_font_prefs.find_one({"user_id": cq.from_user.id})
        current = doc.get("font") if doc else None
    try:
        await cq.edit_message_text(
            _font_menu_text(current, page),
            reply_markup=_font_menu_keyboard(page),
        )
    except Exception:
        pass


@app.on_callback_query(filters.regex("^font_page_noop$") & ~BANNED_USERS)
async def font_page_noop(_, cq: CallbackQuery):
    await cq.answer("📄 Page indicator", show_alert=False)


# ── set_user_font callback ─────────────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^set_user_font:") & ~BANNED_USERS)
async def set_user_font_cb(_, cq: CallbackQuery):
    font_key = cq.data.split(":", 1)[1]
    if not cq.from_user:
        return await cq.answer("❌ Cannot identify user.", show_alert=True)
    user_id = cq.from_user.id

    if font_key == "none":
        await user_font_prefs.delete_one({"user_id": user_id})
        await cq.answer("✅ Font cleared — using default style.", show_alert=True)
        current = None
    else:
        await user_font_prefs.update_one(
            {"user_id": user_id},
            {"$set": {"font": font_key}},
            upsert=True,
        )
        preview = FONT_PREVIEW.get(font_key, font_key)
        if font_key == "fullwidth":
            preview = apply_custom_font("Nobita X Prime", "fullwidth")
        elif font_key == "inverted":
            preview = apply_custom_font("Nobita X Prime", "inverted")
        await cq.answer(f"✅ Font set!\n{preview}", show_alert=True)
        current = font_key

    try:
        await cq.edit_message_text(
            _font_menu_text(current, 1),
            reply_markup=_font_menu_keyboard(1),
        )
    except Exception:
        pass


__help__ = """
 ❍ /setmyfont *:* ᴄʜᴏᴏsᴇ ꜰʀᴏᴍ 41 ꜰᴏɴᴛ sᴛʏʟᴇs ꜰᴏʀ ᴛʜᴇ ʙᴏᴛ's ᴀɪ ʀᴇᴘʟɪᴇs ᴛᴏ ʏᴏᴜ.
 """

__mod_name__ = "Fᴏɴᴛ Pʀᴇꜰ"
