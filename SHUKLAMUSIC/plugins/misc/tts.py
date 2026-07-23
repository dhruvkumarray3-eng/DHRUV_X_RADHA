import io
from gtts import gTTS
from gtts.lang import tts_langs
from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils.database import get_lang
from config import BANNED_USERS

# Language code → gTTS lang map
LANG_MAP = {
    "hi": "hi",   # Hindi
    "en": "en",   # English
    "te": "te",   # Telugu
    "ta": "ta",   # Tamil
    "ml": "ml",   # Malayalam
    "kn": "kn",   # Kannada
    "mr": "mr",   # Marathi
    "bn": "bn",   # Bengali
    "gu": "gu",   # Gujarati
    "pa": "pa",   # Punjabi
    "ur": "ur",   # Urdu
    "ar": "ar",   # Arabic
    "fr": "fr",   # French
    "de": "de",   # German
    "es": "es",   # Spanish
    "it": "it",   # Italian
    "pt": "pt",   # Portuguese
    "ru": "ru",   # Russian
    "ja": "ja",   # Japanese
    "ko": "ko",   # Korean
    "zh": "zh",   # Chinese (Mandarin)
    "tr": "tr",   # Turkish
    "pl": "pl",   # Polish
    "nl": "nl",   # Dutch
    "sv": "sv",   # Swedish
    "id": "id",   # Indonesian
    "ms": "ms",   # Malay
    "th": "th",   # Thai
    "vi": "vi",   # Vietnamese
    "uk": "uk",   # Ukrainian
}

TTS_HELP = (
    "**🔊 ᴛᴛs — ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ**\n\n"
    "**Usage:**\n"
    "• `/tts <text>` — uses your group's language\n"
    "• `/tts <lang_code> <text>` — specify language\n\n"
    "**Examples:**\n"
    "• `/tts Hello everyone!`\n"
    "• `/tts hi नमस्ते दुनिया`\n"
    "• `/tts ar مرحبا بالجميع`\n"
    "• `/tts ja こんにちは`\n\n"
    "**🌍 Language Codes:**\n"
    "`hi` Hindi · `en` English · `te` Telugu\n"
    "`ta` Tamil · `ml` Malayalam · `bn` Bengali\n"
    "`mr` Marathi · `gu` Gujarati · `pa` Punjabi\n"
    "`ur` Urdu · `ar` Arabic · `fr` French\n"
    "`de` German · `es` Spanish · `it` Italian\n"
    "`pt` Portuguese · `ru` Russian · `ja` Japanese\n"
    "`ko` Korean · `zh` Chinese · `tr` Turkish\n"
    "`th` Thai · `vi` Vietnamese · `id` Indonesian"
)


@app.on_message(filters.command(["tts", "speak"]) & ~BANNED_USERS)
async def text_to_speech(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(TTS_HELP)

    parts = message.text.split(None, 2)

    # Check if first arg is a known language code
    if len(parts) >= 3 and parts[1].lower() in LANG_MAP:
        lang_code = LANG_MAP[parts[1].lower()]
        text = parts[2]
    elif len(parts) >= 3 and parts[1].lower() in tts_langs():
        lang_code = parts[1].lower()
        text = parts[2]
    else:
        # Auto-detect from group language setting
        try:
            user_lang = await get_lang(message.chat.id)
            lang_code = LANG_MAP.get(user_lang, "hi")
        except Exception:
            lang_code = "hi"
        text = message.text.split(None, 1)[1]

    text = text.strip()
    if not text:
        return await message.reply_text("Please provide text!\n\nUsage: `/tts <text>` or `/tts <lang_code> <text>`")

    processing = await message.reply_text("🔊 ɢᴇɴᴇʀᴀᴛɪɴɢ ᴀᴜᴅɪᴏ...")
    try:
        tts = gTTS(text, lang=lang_code)
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        audio_file = io.BytesIO(audio_data.read())
        audio_file.name = "tts_audio.mp3"

        lang_names = {
            "hi": "Hindi", "en": "English", "te": "Telugu", "ta": "Tamil",
            "ml": "Malayalam", "ar": "Arabic", "fr": "French", "de": "German",
            "es": "Spanish", "ja": "Japanese", "ko": "Korean", "ru": "Russian",
            "zh": "Chinese", "tr": "Turkish", "bn": "Bengali", "ur": "Urdu",
        }
        lang_display = lang_names.get(lang_code, lang_code.upper())

        await processing.delete()
        await message.reply_audio(
            audio_file,
            caption=f"🔊 **ᴛᴛs ᴀᴜᴅɪᴏ** · Language: `{lang_display}`",
        )
    except Exception as e:
        await processing.edit_text(
            f"❌ Error: `{e}`\n\n"
            "Use a valid language code like: `hi`, `en`, `te`, `ta`, `ar`, etc.\n"
            "Send `/tts` for the full list."
        )
