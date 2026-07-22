# -----------------------------------------------
# 🔸 SHUKLAMUSIC — Bot Command Registration
# 🔹 Uses Bot HTTP API directly (token-based) to
#    register /commands with Telegram — same as
#    BotFather, so they appear in the / menu.
# -----------------------------------------------

import os
import aiohttp
from SHUKLAMUSIC.logging import LOGGER

_LOG = LOGGER("SHUKLAMUSIC.core.commands")

_TOKEN = os.environ.get("BOT_TOKEN", "")
_BASE  = f"https://api.telegram.org/bot{_TOKEN}"

# ── User commands — shown to everyone ───────────────────────────────────────
_USER_CMDS = [
    # ── Music ──
    ("play",      "❤️‍🔥 ᴘʟᴀʏ ᴀᴜᴅɪᴏ | sᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ"),
    ("vplay",     "☄️ ᴘʟᴀʏ ᴠɪᴅᴇᴏ | sᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ"),
    ("pause",     "🫠 ᴘᴀᴜsᴇ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ"),
    ("resume",    "✨ ʀᴇsᴜᴍᴇ ᴘᴀᴜsᴇᴅ ᴛʀᴀᴄᴋ"),
    ("skip",      "☄️ sᴋɪᴘ ᴛᴏ ɴᴇxᴛ ᴛʀᴀᴄᴋ"),
    ("stop",      "🤕 sᴛᴏᴘ & ᴄʟᴇᴀʀ ǫᴜᴇᴜᴇ"),
    ("end",       "🥀 ᴇɴᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴇssɪᴏɴ"),
    ("queue",     "🌹 ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏ ǫᴜᴇᴜᴇ"),
    ("loop",      "✨ ᴛᴏɢɢʟᴇ ʟᴏᴏᴘ | ᴏɴ / ᴏғғ"),
    ("shuffle",   "🌹 sʜᴜғғʟᴇ ǫᴜᴇᴜᴇ ʀᴀɴᴅᴏᴍʟʏ"),
    ("seek",      "🫰 sᴇᴇᴋ ᴛᴏ ᴛɪᴍᴇ | ᴇɢ: 1:30"),
    ("speed",     "☄️ sᴇᴛ sᴘᴇᴇᴅ | ᴇɢ: 1.5x, 2x"),
    ("song",      "🌹 ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ᴀs ᴍᴘ3 ᴀᴜᴅɪᴏ"),
    # ── Info / Utility ──
    ("start",     "✨ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ & sᴇᴇ ʜᴏᴍᴇ"),
    ("help",      "😇 ᴀʟʟ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs ᴍᴇɴᴜ"),
    ("ping",      "☄️ ᴄʜᴇᴄᴋ ʙᴏᴛ ʀᴇsᴘᴏɴsᴇ sᴘᴇᴇᴅ"),
    ("stats",     "🫡 ʙᴏᴛ sᴛᴀᴛs | ᴜᴘᴛɪᴍᴇ, ʀᴀᴍ, ᴄᴘᴜ"),
    ("id",        "🦁 ɢᴇᴛ ᴜsᴇʀ ɪᴅ ᴏʀ ᴄʜᴀᴛ ɪᴅ"),
    ("info",      "😇 ᴠɪᴇᴡ ᴅᴇᴛᴀɪʟᴇᴅ ᴜsᴇʀ ɪɴғᴏ"),
    ("search",    "🫰 sᴇᴀʀᴄʜ ʏᴏᴜᴛᴜʙᴇ ʙʏ ɴᴀᴍᴇ"),
    ("tr",        "😇 ᴛʀᴀɴsʟᴀᴛᴇ ᴛᴇxᴛ ᴛᴏ ᴀɴʏ ʟᴀɴɢ"),
    ("tts",       "🌹 ᴄᴏɴᴠᴇʀᴛ ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ"),
    ("qr",        "✨ ɢᴇɴᴇʀᴀᴛᴇ ǫʀ ᴄᴏᴅᴇ ғʀᴏᴍ ᴛᴇxᴛ"),
    ("weather",   "☄️ ᴄʜᴇᴄᴋ ᴡᴇᴀᴛʜᴇʀ ʙʏ ᴄɪᴛʏ"),
    ("movie",     "🌹 sᴇᴀʀᴄʜ ᴍᴏᴠɪᴇ ɪɴғᴏ & ʀᴀᴛɪɴɢ"),
    ("github",    "🫡 ᴠɪᴇᴡ ɢɪᴛʜᴜʙ ᴜsᴇʀ ᴘʀᴏғɪʟᴇ"),
    ("carbon",    "✨ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴏᴅᴇ sɴɪᴘᴘᴇᴛ ɪᴍᴀɢᴇ"),
    ("paste",     "🌹 ᴘᴀsᴛᴇ ᴛᴇxᴛ ᴏɴʟɪɴᴇ"),
    ("love",      "❤️‍🩹 ᴄᴀʟᴄᴜʟᴀᴛᴇ ʟᴏᴠᴇ % ᴡɪᴛʜ ᴜsᴇʀ"),
    ("couples",   "🌹 ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ ɪɴ ɢʀᴏᴜᴘ"),
    ("dice",      "🦁 ʀᴏʟʟ ᴀ ᴅɪᴄᴇ"),
    ("kang",      "😇 ᴄʟᴏɴᴇ sᴛɪᴄᴋᴇʀ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ"),
    ("notes",     "🌹 ᴠɪᴇᴡ sᴀᴠᴇᴅ ɢʀᴏᴜᴘ ɴᴏᴛᴇs"),
    ("save",      "🫡 sᴀᴠᴇ ᴀ ɴᴏᴛᴇ ɪɴ ɢʀᴏᴜᴘ"),
    ("get",       "🫰 ɢᴇᴛ ᴀ sᴀᴠᴇᴅ ɴᴏᴛᴇ"),
    ("cleanmongo","🤕 ᴄʟᴇᴀɴ ᴊᴜɴᴋ ᴅᴀᴛᴀ ᴀɴᴅ ᴅʙ sᴛᴀᴛs"),
]

# ── Admin commands — shown only to group admins ──────────────────────────────
_ADMIN_CMDS = [
    # ── Voice Chat Controls ──
    ("cplay",      "❤️‍🔥 ᴄʜᴀɴɴᴇʟ — ᴘʟᴀʏ ᴀᴜᴅɪᴏ"),
    ("cvplay",     "☄️ ᴄʜᴀɴɴᴇʟ — ᴘʟᴀʏ ᴠɪᴅᴇᴏ"),
    ("playmode",   "❤️‍🔥 ᴄʜᴀɴɢᴇ ᴘʟᴀʏ ᴍᴏᴅᴇ sᴇᴛᴛɪɴɢ"),
    ("autoend",    "🤕 ᴛᴏɢɢʟᴇ ᴀᴜᴛᴏ-ᴇɴᴅ ᴡʜᴇɴ ᴇᴍᴘᴛʏ"),
    ("vclogger",   "🫡 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴊᴏɪɴ/ʟᴇᴀᴠᴇ ʟᴏɢɢᴇʀ"),
    # ── Member Management ──
    ("ban",        "👻 ʙᴀɴ ᴀ ᴜsᴇʀ ғʀᴏᴍ ɢʀᴏᴜᴘ"),
    ("unban",      "✨ ᴜɴʙᴀɴ ᴀ ᴜsᴇʀ"),
    ("kick",       "🤕 ᴋɪᴄᴋ ᴀ ᴜsᴇʀ ᴏᴜᴛ"),
    ("mute",       "🫠 ᴍᴜᴛᴇ ᴀ ᴜsᴇʀ"),
    ("unmute",     "😇 ᴜɴᴍᴜᴛᴇ ᴀ ᴜsᴇʀ"),
    ("tmute",      "🫠 ᴛᴇᴍᴘ ᴍᴜᴛᴇ | ᴅᴜʀᴀᴛɪᴏɴ"),
    ("unmuteall",  "😇 ᴜɴᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀs"),
    # ── Admin Rights ──
    ("auth",       "😇 ᴀᴜᴛʜᴏʀɪsᴇ ᴀ ᴜsᴇʀ ᴛᴏ ᴜsᴇ ᴍᴜsɪᴄ"),
    ("unauth",     "🥀 ʀᴇᴍᴏᴠᴇ ᴜsᴇʀ ᴀᴜᴛʜ"),
    ("authlist",   "😇 ʟɪsᴛ ᴀʟʟ ᴀᴜᴛʜ ᴜsᴇʀs"),
    ("promote",    "🦁 ᴘʀᴏᴍᴏᴛᴇ ᴜsᴇʀ ᴛᴏ ᴀᴅᴍɪɴ"),
    ("fullpromote","🦁 ғᴜʟʟ ᴀᴅᴍɪɴ ᴘʀᴏᴍᴏᴛᴇ"),
    ("demote",     "🥀 ᴅᴇᴍᴏᴛᴇ ᴀɴ ᴀᴅᴍɪɴ"),
    # ── Group Tools ──
    ("purge",      "☄️ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs ɪɴ ʙᴜʟᴋ"),
    ("pin",        "🫡 ᴘɪɴ ᴀ ᴍᴇssᴀɢᴇ"),
    ("unpin",      "🌹 ᴜɴᴘɪɴ ᴀ ᴍᴇssᴀɢᴇ"),
    ("all",        "🦁 ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs"),
    ("admins",     "😇 ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴀᴅᴍɪɴs"),
    ("nightmode",  "🌹 ᴀᴜᴛᴏ ɴɪɢʜᴛ ᴍᴏᴅᴇ ᴏɴ/ᴏғғ"),
    ("settings",   "🫡 ɢʀᴏᴜᴘ sᴇᴛᴛɪɴɢs ᴘᴀɴᴇʟ"),
    ("setphoto",   "✨ sᴇᴛ ɢʀᴏᴜᴘ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ"),
    ("settitle",   "🌹 sᴇᴛ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ"),
    ("zombies",    "🥀 ʀᴇᴍᴏᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs"),
    ("welcome",    "😇 sᴇᴛ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ"),
    ("reload",     "☄️ ʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ"),
    ("filter",     "🌹 ᴀᴅᴅ ᴀ ᴋᴇʏᴡᴏʀᴅ ғɪʟᴛᴇʀ"),
    ("filters",    "🌹 ʟɪsᴛ ᴀʟʟ ᴋᴇʏᴡᴏʀᴅ ғɪʟᴛᴇʀs"),
]

# ── All scopes to delete before re-registering ──────────────────────────────
_DELETE_SCOPES = [
    {"type": "default"},
    {"type": "all_private_chats"},
    {"type": "all_group_chats"},
    {"type": "all_chat_administrators"},
]

# ── Scopes to register ───────────────────────────────────────────────────────
_SET_SCOPES = [
    # (scope_dict, commands_list)
    ({"type": "default"},                  _USER_CMDS),
    ({"type": "all_private_chats"},        _USER_CMDS),
    ({"type": "all_group_chats"},          _USER_CMDS),
    ({"type": "all_chat_administrators"},  _ADMIN_CMDS + _USER_CMDS),
]


async def _api(session: aiohttp.ClientSession, method: str, payload: dict) -> dict:
    async with session.post(f"{_BASE}/{method}", json=payload) as r:
        return await r.json()


async def register_bot_commands():
    """
    Delete all existing commands from every scope, then re-register
    user + admin commands via the Bot HTTP API (token-based).
    """
    if not _TOKEN:
        _LOG.warning("BOT_TOKEN not set — skipping command registration.")
        return

    async with aiohttp.ClientSession() as session:

        # 1️⃣  Wipe every scope clean first
        for scope in _DELETE_SCOPES:
            res = await _api(session, "deleteMyCommands", {"scope": scope})
            if not res.get("ok"):
                _LOG.warning(f"deleteMyCommands [{scope['type']}]: {res}")

        # 2️⃣  Register fresh commands for each scope
        ok_count = 0
        for scope, cmds in _SET_SCOPES:
            payload = {
                "commands": [
                    {"command": cmd, "description": desc}
                    for cmd, desc in cmds
                ],
                "scope": scope,
            }
            res = await _api(session, "setMyCommands", payload)
            if res.get("ok"):
                ok_count += 1
            else:
                _LOG.warning(f"setMyCommands [{scope['type']}]: {res}")

    _LOG.info(
        f"✅ Commands registered: {len(_USER_CMDS)} user • "
        f"{len(_ADMIN_CMDS)} admin • {ok_count}/{len(_SET_SCOPES)} scopes OK."
    )
