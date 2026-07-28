import io
import os
import asyncio
import tempfile
import edge_tts
from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils.database import get_lang
from config import BANNED_USERS

# Language code → edge-tts MALE voice map
LANG_VOICE_MAP = {
    "hi": "hi-IN-MadhurNeural",       # Hindi — Male
    "en": "en-IN-PrabhatNeural",       # English (Indian) — Male
    "en-us": "en-US-GuyNeural",        # English (US) — Male
    "te": "te-IN-MohanNeural",         # Telugu — Male
    "ta": "ta-IN-ValluvarNeural",      # Tamil — Male
    "ml": "ml-IN-MidhunNeural",        # Malayalam — Male
    "kn": "kn-IN-GaganNeural",         # Kannada — Male
    "mr": "mr-IN-ManoharNeural",       # Marathi — Male
    "bn": "bn-IN-BashkarNeural",       # Bengali — Male
    "gu": "gu-IN-NiranjanNeural",      # Gujarati — Male
    "ar": "ar-SA-HamedNeural",         # Arabic — Male
    "fr": "fr-FR-HenriNeural",         # French — Male
    "de": "de-DE-ConradNeural",        # German — Male
    "es": "es-ES-AlvaroNeural",        # Spanish — Male
    "it": "it-IT-DiegoNeural",         # Italian — Male
    "pt": "pt-BR-AntonioNeural",       # Portuguese — Male
    "ru": "ru-RU-DmitryNeural",        # Russian — Male
    "ja": "ja-JP-KeitaNeural",         # Japanese — Male
    "ko": "ko-KR-InJoonNeural",        # Korean — Male
    "zh": "zh-CN-YunxiNeural",         # Chinese — Male
    "tr": "tr-TR-AhmetNeural",         # Turkish — Male
    "pl": "pl-PL-MarekNeural",         # Polish — Male
    "nl": "nl-NL-MaartenNeural",       # Dutch — Male
    "sv": "sv-SE-MattiasNeural",       # Swedish — Male
    "id": "id-ID-ArdiNeural",          # Indonesian — Male
    "ms": "ms-MY-OsmanNeural",         # Malay — Male
    "th": "th-TH-NiwatNeural",         # Thai — Male
    "vi": "vi-VN-NamMinhNeural",       # Vietnamese — Male
    "uk": "uk-UA-OstapNeural",         # Ukrainian — Male
    "ur": "ur-PK-AsadNeural",          # Urdu — Male
    "pa": "pa-IN-OjasNeural",          # Punjabi — Male (fallback to hi if unavailable)
}

# Short alias map (what user types → internal key)
LANG_ALIAS = {
    "hindi": "hi", "english": "en", "telugu": "te", "tamil": "ta",
    "malayalam": "ml", "kannada": "kn", "marathi": "mr", "bengali": "bn",
    "gujarati": "gu", "arabic": "ar", "french": "fr", "german": "de",
    "spanish": "es", "italian": "it", "portuguese": "pt", "russian": "ru",
    "japanese": "ja", "korean": "ko", "chinese": "zh", "turkish": "tr",
    "polish": "pl", "dutch": "nl", "swedish": "sv", "indonesian": "id",
    "malay": "ms", "thai": "th", "vietnamese": "vi", "ukrainian": "uk",
    "urdu": "ur", "punjabi": "pa",
}

TTS_HELP = (
    "**🔊 ᴛᴛs — ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ (Male Voice)**\n\n"
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


async def _synthesize(text: str, voice: str) -> bytes:
    """Generate TTS audio using edge-tts and return MP3 bytes."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


@app.on_message(filters.command(["tts", "speak"]) & ~BANNED_USERS)
async def text_to_speech(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(TTS_HELP)

    parts = message.text.split(None, 2)
    lang_key = None

    # Check if first arg is a known language code or alias
    first_arg = parts[1].lower() if len(parts) >= 2 else ""
    first_arg = LANG_ALIAS.get(first_arg, first_arg)  # resolve aliases

    if len(parts) >= 3 and first_arg in LANG_VOICE_MAP:
        lang_key = first_arg
        text = parts[2]
    else:
        # Auto-detect from group language setting
        try:
            user_lang = await get_lang(message.chat.id)
            user_lang = LANG_ALIAS.get(user_lang.lower(), user_lang.lower())
            lang_key = user_lang if user_lang in LANG_VOICE_MAP else "hi"
        except Exception:
            lang_key = "hi"
        text = message.text.split(None, 1)[1]

    text = text.strip()
    if not text:
        return await message.reply_text(
            "Please provide text!\n\nUsage: `/tts <text>` or `/tts <lang_code> <text>`"
        )

    processing = await message.reply_text("🔊 ɢᴇɴᴇʀᴀᴛɪɴɢ ᴀᴜᴅɪᴏ...")
    try:
        voice = LANG_VOICE_MAP.get(lang_key, "hi-IN-MadhurNeural")
        audio_bytes = await _synthesize(text, voice)

        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "tts_audio.mp3"

        lang_display_map = {
            "hi": "Hindi", "en": "English", "te": "Telugu", "ta": "Tamil",
            "ml": "Malayalam", "ar": "Arabic", "fr": "French", "de": "German",
            "es": "Spanish", "ja": "Japanese", "ko": "Korean", "ru": "Russian",
            "zh": "Chinese", "tr": "Turkish", "bn": "Bengali", "ur": "Urdu",
            "mr": "Marathi", "gu": "Gujarati", "pa": "Punjabi", "kn": "Kannada",
        }
        lang_display = lang_display_map.get(lang_key, lang_key.upper())

        await processing.delete()
        await message.reply_audio(
            audio_file,
            caption=f"🔊 **ᴛᴛs ᴀᴜᴅɪᴏ** · Language: `{lang_display}` · Voice: Male 🎙️",
        )
    except Exception as e:
        await processing.edit_text(
            f"❌ Error: `{e}`\n\n"
            "Use a valid language code like: `hi`, `en`, `te`, `ta`, `ar`, etc.\n"
            "Send `/tts` for the full list."
        )
