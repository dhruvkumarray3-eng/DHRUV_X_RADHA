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

# ── Font catalogue ─────────────────────────────────────────────────────────────
FONT_OPTIONS = [
    ("typewriter", "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛",   ButtonStyle.PRIMARY),
    ("san",        "𝗦𝗮𝗻𝘀 𝗕𝗼𝗹𝗱",    ButtonStyle.SUCCESS),
    ("script",     "𝓈𝒸𝓇𝒾𝓅𝓉",        ButtonStyle.DANGER),
    ("bold_script","𝓼𝓬𝓻𝓲𝓹𝓽 𝓑𝓸𝓵𝓭",  ButtonStyle.PRIMARY),
    ("gothic",     "𝔊𝔬𝔱𝔥𝔦𝔠",        ButtonStyle.SUCCESS),
    ("bold_gothic","𝕲𝖔𝖙𝖍𝖎𝖈 𝕭𝖔𝖑𝖉",  ButtonStyle.DANGER),
    ("smallcap",   "Sᴍᴀʟʟ Cᴀᴘs",   ButtonStyle.PRIMARY),
    ("serief",     "𝐒𝐞𝐫𝐢𝐟 𝐁𝐨𝐥𝐝",    ButtonStyle.SUCCESS),
    ("slant",      "𝘚𝘭𝘢𝘯𝘵",         ButtonStyle.DANGER),
    ("bold_cool",  "𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄",  ButtonStyle.PRIMARY),
    ("comic",      "ᑕOᗰIᑕ",         ButtonStyle.SUCCESS),
    ("circles",    "Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ",    ButtonStyle.DANGER),
]

FONT_PREVIEW = {
    "typewriter":  "𝙽𝙾𝙱𝙸𝚃𝙰 𝚇 𝙿𝚁𝙸𝙼𝙴",
    "san":         "𝗡𝗢𝗕𝗜𝗧𝗔 𝗫 𝗣𝗥𝗜𝗠𝗘",
    "script":      "𝒩𝑜𝒷𝒾𝓉𝒶 𝒳 𝒫𝓇𝒾𝓂𝑒",
    "bold_script": "𝓝𝓸𝓫𝓲𝓽𝓪 𝓧 𝓟𝓻𝓲𝓶𝓮",
    "gothic":      "𝔑𝔬𝔟𝔦𝔱𝔞 𝔛 𝔓𝔯𝔦𝔪𝔢",
    "bold_gothic": "𝕹𝖔𝖇𝖎𝖙𝖆 𝖃 𝕻𝖗𝖎𝖒𝖊",
    "smallcap":    "ɴᴏʙɪᴛᴀ x ᴘʀɪᴍᴇ",
    "serief":      "𝐍𝐨𝐛𝐢𝐭𝐚 𝐗 𝐏𝐫𝐢𝐦𝐞",
    "slant":       "𝘕𝘰𝘣𝘪𝘵𝘢 𝘟 𝘗𝘳𝘪𝘮𝘦",
    "bold_cool":   "𝑵𝒐𝒃𝒊𝒕𝒂 𝑿 𝑷𝒓𝒊𝒎𝒆",
    "comic":       "ᑎOᗷITᗩ ᙖ ᑭᖇIᗰE",
    "circles":     "Ⓝ︎Ⓞ︎Ⓑ︎Ⓘ︎Ⓣ︎Ⓐ︎ Ⓧ︎ Ⓟ︎Ⓡ︎Ⓘ︎Ⓜ︎Ⓔ︎",
}


def _font_menu_keyboard():
    rows = []
    for i in range(0, len(FONT_OPTIONS), 3):
        chunk = FONT_OPTIONS[i:i + 3]
        rows.append([
            InlineKeyboardButton(text=label, callback_data=f"set_user_font:{key}", style=style)
            for key, label, style in chunk
        ])
    rows.append([
        InlineKeyboardButton(text="❌ ɴᴏ ꜰᴏɴᴛ (ᴅᴇꜰᴀᴜʟᴛ)", callback_data="set_user_font:none", style=ButtonStyle.DANGER),
    ])
    rows.append([
        InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="help_page_4", style=ButtonStyle.SUCCESS),
    ])
    return InlineKeyboardMarkup(rows)


def _font_menu_text(current_font: str | None) -> str:
    preview = FONT_PREVIEW.get(current_font, "ɴᴏʙɪᴛᴀ x ᴘʀɪᴍᴇ")
    current_label = next((lbl for k, lbl, _ in FONT_OPTIONS if k == current_font), "Default")
    return (
        "🔤 <b>Cʜᴏᴏsᴇ Yᴏᴜʀ Fᴏɴᴛ Sᴛʏʟᴇ</b>\n\n"
        f"📌 <b>Current:</b> {current_label}\n"
        f"👁 <b>Preview:</b> {preview}\n\n"
        "Pick a font below — the bot will style its AI replies to you in that font:\n\n"
        "💡 <i>Font only applies to text replies, not code blocks.</i>"
    )


# ── /setmyfont command ─────────────────────────────────────────────────────────
@app.on_message(filters.command(["setmyfont", "myfont"]) & ~BANNED_USERS)
async def setmyfont_cmd(_, message: Message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return
    doc = await user_font_prefs.find_one({"user_id": user_id})
    current = doc.get("font") if doc else None
    await message.reply_text(
        _font_menu_text(current),
        reply_markup=_font_menu_keyboard(),
    )


# ── my_font_menu callback (from Help page 4) ──────────────────────────────────
@app.on_callback_query(filters.regex("^my_font_menu$") & ~BANNED_USERS)
async def my_font_menu_cb(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except Exception:
        pass
    user_id = cq.from_user.id if cq.from_user else None
    current = None
    if user_id:
        doc = await user_font_prefs.find_one({"user_id": user_id})
        current = doc.get("font") if doc else None
    try:
        await cq.edit_message_text(
            _font_menu_text(current),
            reply_markup=_font_menu_keyboard(),
        )
    except Exception:
        await cq.message.reply_text(
            _font_menu_text(current),
            reply_markup=_font_menu_keyboard(),
        )


# ── set_user_font callback ─────────────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^set_user_font:") & ~BANNED_USERS)
async def set_user_font_cb(_, cq: CallbackQuery):
    font_key = cq.data.split(":", 1)[1]
    user_id = cq.from_user.id if cq.from_user else None
    if not user_id:
        return await cq.answer("❌ Could not identify user.", show_alert=True)

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
        await cq.answer(f"✅ Font set! Preview: {preview}", show_alert=True)
        current = font_key

    # Refresh the menu in-place
    try:
        await cq.edit_message_text(
            _font_menu_text(current),
            reply_markup=_font_menu_keyboard(),
        )
    except Exception:
        pass


__help__ = """
 ❍ /setmyfont *:* ᴄʜᴏᴏsᴇ ᴀ ꜰᴏɴᴛ sᴛʏʟᴇ ꜰᴏʀ ᴛʜᴇ ʙᴏᴛ's ᴀɪ ʀᴇᴘʟɪᴇs ᴛᴏ ʏᴏᴜ.
 """

__mod_name__ = "Fᴏɴᴛ Pʀᴇꜰ"
