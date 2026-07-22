# -----------------------------------------------
# 🔸 SHUKLAMUSIC — Bot Command Registration
# 🔹 Registers /commands in BotFather style for
#    users and admins separately via Pyrogram.
# -----------------------------------------------

from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeDefault,
)

from SHUKLAMUSIC import app
from SHUKLAMUSIC.logging import LOGGER


# ── User commands (shown in all chats) ──────────────────────────────────────
_USER_COMMANDS = [
    BotCommand("start",    "✨ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
    BotCommand("help",     "😇 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs"),
    BotCommand("play",     "❤️‍🔥 ᴘʟᴀʏ ᴀᴜᴅɪᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("vplay",    "☄️ ᴘʟᴀʏ ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("pause",    "🫠 ᴘᴀᴜsᴇ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ"),
    BotCommand("resume",   "✨ ʀᴇsᴜᴍᴇ ᴘᴀᴜsᴇᴅ ᴛʀᴀᴄᴋ"),
    BotCommand("skip",     "☄️ sᴋɪᴘ ᴛᴏ ɴᴇxᴛ ᴛʀᴀᴄᴋ"),
    BotCommand("stop",     "🤕 sᴛᴏᴘ & ᴄʟᴇᴀʀ ǫᴜᴇᴜᴇ"),
    BotCommand("end",      "🥀 ᴇɴᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("queue",    "🌹 ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ǫᴜᴇᴜᴇ"),
    BotCommand("loop",     "✨ ᴛᴏɢɢʟᴇ ʟᴏᴏᴘ ᴍᴏᴅᴇ"),
    BotCommand("shuffle",  "🌹 sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇ"),
    BotCommand("seek",     "🫰 sᴇᴇᴋ ᴛᴏ ᴀ ᴘᴏsɪᴛɪᴏɴ"),
    BotCommand("speed",    "☄️ ᴄʜᴀɴɢᴇ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ"),
    BotCommand("song",     "🌹 ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ᴀs ᴍᴘ3"),
    BotCommand("ping",     "☄️ ᴄʜᴇᴄᴋ ʙᴏᴛ ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ"),
    BotCommand("stats",    "🫡 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs"),
    BotCommand("search",   "🫰 sᴇᴀʀᴄʜ ʏᴏᴜᴛᴜʙᴇ"),
    BotCommand("tr",       "😇 ᴛʀᴀɴsʟᴀᴛᴇ ᴛᴇxᴛ"),
    BotCommand("qr",       "✨ ɢᴇɴᴇʀᴀᴛᴇ ǫʀ ᴄᴏᴅᴇ"),
    BotCommand("tts",      "🌹 ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ"),
    BotCommand("weather",  "☄️ ᴄʜᴇᴄᴋ ᴡᴇᴀᴛʜᴇʀ"),
    BotCommand("github",   "🫡 ɢɪᴛʜᴜʙ ᴜsᴇʀ ɪɴғᴏ"),
    BotCommand("movie",    "🌹 sᴇᴀʀᴄʜ ᴍᴏᴠɪᴇ ɪɴғᴏ"),
    BotCommand("id",       "🦁 ɢᴇᴛ ᴜsᴇʀ / ᴄʜᴀᴛ ɪᴅ"),
    BotCommand("info",     "😇 ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ"),
    BotCommand("love",     "❤️‍🩹 ʟᴏᴠᴇ % ᴡɪᴛʜ sᴏᴍᴇᴏɴᴇ"),
    BotCommand("couples",  "🌹 ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ"),
]

# ── Admin commands (shown to group admins only) ──────────────────────────────
_ADMIN_COMMANDS = [
    BotCommand("auth",       "😇 ᴀᴜᴛʜᴏʀɪsᴇ ᴀ ᴜsᴇʀ"),
    BotCommand("unauth",     "🥀 ʀᴇᴍᴏᴠᴇ ᴜsᴇʀ ᴀᴜᴛʜ"),
    BotCommand("ban",        "👻 ʙᴀɴ ᴀ ᴜsᴇʀ"),
    BotCommand("unban",      "✨ ᴜɴʙᴀɴ ᴀ ᴜsᴇʀ"),
    BotCommand("mute",       "🤕 ᴍᴜᴛᴇ ᴀ ᴜsᴇʀ"),
    BotCommand("unmute",     "😇 ᴜɴᴍᴜᴛᴇ ᴀ ᴜsᴇʀ"),
    BotCommand("tmute",      "🫠 ᴛᴇᴍᴘ ᴍᴜᴛᴇ ᴀ ᴜsᴇʀ"),
    BotCommand("promote",    "🦁 ᴘʀᴏᴍᴏᴛᴇ ᴛᴏ ᴀᴅᴍɪɴ"),
    BotCommand("fullpromote","🦁 ғᴜʟʟ ᴀᴅᴍɪɴ ᴘʀᴏᴍᴏᴛᴇ"),
    BotCommand("demote",     "🥀 ᴅᴇᴍᴏᴛᴇ ᴀᴅᴍɪɴ"),
    BotCommand("ban",        "👻 ʙᴀɴ ᴀ ᴜsᴇʀ ғʀᴏᴍ ɢʀᴏᴜᴘ"),
    BotCommand("kick",       "🤕 ᴋɪᴄᴋ ᴀ ᴜsᴇʀ"),
    BotCommand("purge",      "☄️ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs"),
    BotCommand("pin",        "🫡 ᴘɪɴ ᴀ ᴍᴇssᴀɢᴇ"),
    BotCommand("unpin",      "🌹 ᴜɴᴘɪɴ ᴀ ᴍᴇssᴀɢᴇ"),
    BotCommand("all",        "🦁 ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs"),
    BotCommand("admins",     "😇 ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴀᴅᴍɪɴs"),
    BotCommand("cplay",      "❤️‍🔥 ᴄʜᴀɴɴᴇʟ ᴀᴜᴅɪᴏ ᴘʟᴀʏ"),
    BotCommand("cvplay",     "☄️ ᴄʜᴀɴɴᴇʟ ᴠɪᴅᴇᴏ ᴘʟᴀʏ"),
    BotCommand("playmode",   "❤️‍🔥 ᴄʜᴀɴɢᴇ ᴘʟᴀʏ ᴍᴏᴅᴇ"),
    BotCommand("nightmode",  "🌹 ᴀᴜᴛᴏ ɴɪɢʜᴛ ᴍᴏᴅᴇ"),
    BotCommand("settings",   "🫡 ɢʀᴏᴜᴘ sᴇᴛᴛɪɴɢs"),
    BotCommand("setphoto",   "✨ sᴇᴛ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ"),
    BotCommand("settitle",   "🌹 sᴇᴛ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ"),
    BotCommand("zombies",    "🥀 ʀᴇᴍᴏᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄs"),
    BotCommand("reload",     "☄️ ʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ"),
    BotCommand("welcome",    "😇 sᴇᴛ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ"),
    BotCommand("autoend",    "🤕 ᴀᴜᴛᴏ ᴇɴᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("vclogger",   "🫡 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʟᴏɢɢᴇʀ"),
]


async def register_bot_commands():
    """Register all commands with Telegram so they appear in the / menu."""
    try:
        # Default scope — all chats (fallback)
        await app.set_bot_commands(
            _USER_COMMANDS,
            scope=BotCommandScopeDefault(),
        )

        # Private chats — user commands
        await app.set_bot_commands(
            _USER_COMMANDS,
            scope=BotCommandScopeAllPrivateChats(),
        )

        # Group chats — user commands
        await app.set_bot_commands(
            _USER_COMMANDS,
            scope=BotCommandScopeAllGroupChats(),
        )

        # Group admins — admin commands (overlaid on top of user commands)
        await app.set_bot_commands(
            _ADMIN_COMMANDS + _USER_COMMANDS,
            scope=BotCommandScopeAllChatAdministrators(),
        )

        LOGGER("SHUKLAMUSIC.core.commands").info(
            f"✅ Registered {len(_USER_COMMANDS)} user + {len(_ADMIN_COMMANDS)} admin commands."
        )
    except Exception as e:
        LOGGER("SHUKLAMUSIC.core.commands").warning(f"⚠ Command registration failed: {e}")
