# -----------------------------------------------
# 🔸 NOBITA X PRIME — Owner DM Panel
# All key commands work in private for owner.
# Remote control for any group from DM.
# Full /ownerguide with every command listed.
# -----------------------------------------------

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SHUKLAMUSIC import app
from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.misc import db as _stream_db
from SHUKLAMUSIC.utils.database import (
    get_served_chats, get_served_users,
    is_active_chat,
)
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS, OWNER_ID

_chatbot_col   = mongodb.chatbot_settings
_autoreport_col = mongodb.autoreport_settings


def _is_owner(message: Message) -> bool:
    uid = message.from_user.id if message.from_user else 0
    return str(uid) == str(OWNER_ID) or uid in SUDOERS


# ═══════════════════════════════════════════
#  /ownerguide — Full Command Guide
# ═══════════════════════════════════════════

GUIDE_SECTIONS = [

    ("🎵 MUSIC — Group Commands", """\
`/play <song/url>` — Play music in voice chat
`/vplay <song/url>` — Play video in voice chat
`/skip` — Skip to next song
`/pause` — Pause playback
`/resume` — Resume playback
`/stop` — Stop & leave voice chat
`/queue` — Show current queue
`/shuffle` — Shuffle the queue
`/loop` — Toggle loop mode
`/seek <seconds>` — Seek forward
`/speed <0.5–2.0>` — Change playback speed
`/song <name>` — Download & send song
`/channelplay` — Stream in a channel"""),

    ("🤖 AI CHATBOT — Group + DM", """\
`/chatbot on` — Enable chatbot in group
`/chatbot off` — Disable chatbot in group
`/chatbot status` — Check chatbot status
`/chatbothelp` — Full chatbot help

**Teaching:**
`/teach keyword | reply` — Teach a keyword reply
`/unlearn keyword` — Forget a keyword
`/learned` — List all keywords

**User Profiles (AI Memory):**
`/addprofile @user info` — Save user info for AI
`/delprofile @user` — Remove user profile
`/profiles` — List all saved profiles
`/setmyprofile info` — Set your own profile
`/mymemory` — See your saved profile
`/deletemyprofile` — Delete your profile

**Owner Remote (from DM):**
`/rmchatbot <chat_id> on/off` — Toggle chatbot in any group"""),

    ("🛡️ AUTO-REPORT SYSTEM", """\
`/autoreport on` — Enable in group
`/autoreport off` — Disable in group
`/autoreport status` — Check status

AI detects abuse/threats/hate/copyright/spam
and files multiple Telegram reports silently.

**Owner Remote (from DM):**
`/rmautoreport <chat_id> on/off` — Toggle in any group"""),

    ("👑 SESSION MANAGER — Owner DM Only", """\
`/addsession <string>` — Add new userbot session
`/listsessions` — List all active sessions
`/removesession <slot>` — Remove a session

Supports STRING_SESSION1–7 from config +
unlimited dynamic sessions via /addsession.
Sessions saved in MongoDB, auto-restore on restart."""),

    ("🔨 SUDO / OWNER COMMANDS", """\
`/broadcast <msg>` — Broadcast to all groups
`/gban @user reason` — Global ban user
`/ungban @user` — Remove global ban
`/gbannedusers` — List globally banned users
`/sudoers` — List sudo users
`/addsudo @user` — Add sudo user
`/delsudo @user` — Remove sudo user
`/maintenance on/off` — Toggle maintenance mode
`/restart` — Restart the bot
`/update` — Pull latest from GitHub & restart
`/logs` — Get bot logs
`/cleanmongo` — Clean old MongoDB data"""),

    ("🛠️ GROUP ADMIN COMMANDS", """\
**Music Auth:**
`/auth @user` — Allow user to use music cmds
`/unauth @user` — Remove auth
`/authlist` — List authed users

**Moderation:**
`/ban @user` — Ban user
`/unban @user` — Unban user
`/mute @user` — Mute user
`/unmute @user` — Unmute user
`/purge` — Delete messages
`/unbanall` — Unban all users
`/unpinall` — Unpin all messages
`/promote @user` — Promote to admin
`/demote @user` — Demote admin

**Group Tools:**
`/guardian on/off` — Anti-flood guardian
`/nightmode on/off` — Night mode (auto-restrict)
`/autoapprove on/off` — Auto-approve join requests
`/welcome on/off` — Welcome new members
`/vclogger on/off` — Log VC join/leave
`/playmode` — Change play mode settings
`/settings` — Bot settings for group
`/lang <code>` — Set group language
`/stats` — Group music statistics"""),

    ("🎮 GAMES & FUN — Group", """\
`/triviabattle` — Start trivia battle
`/dicebattle @user` — Dice battle
`/numberbomb` — Number bomb game
`/roulette` — Russian roulette
`/taprace` — Tap race game
`/slots` — Slot machine
`/hotvote` — Hot or Not vote
`/chatfighton` — Enable chat fight mode
`/wordgame` / `startword` — Word chain game
`/imposter` — Imposter game
`/quickgame` — Quick quiz

`/truth` / `/dare` — Truth or dare
`/joke` — Random joke
`/quote` — Random quote
`/shayari` — Random shayari
`/love @user` — Love calculator"""),

    ("🛠️ TOOLS & UTILITIES", """\
`/tts <text>` — Text to speech (Male voice)
`/tts <lang> <text>` — TTS in specific language
`/tr <lang> <text>` — Translate text
`/ping` — Check bot ping
`/speedtest` — Internet speed test
`/qr <text>` — Generate QR code
`/weather <city>` — Weather info
`/movie <name>` — Movie info
`/pypi <package>` — PyPI package info
`/setmyfont` — Set your custom font style
`/carbon <code>` — Beautiful code image
`/telegraph <text>` — Post to Telegraph
`/paste <text>` — Paste to Hastebin
`/webshot <url>` — Screenshot website
`/zip` / `/unzip` — File compress/extract
`/upscale` — Upscale image quality
`/bgremove` — Remove image background
`/sticker` — Create sticker
`/kang` — Steal sticker

`/ytdl <url>` — Download YouTube video
`/insta <url>` — Download Instagram post
`/bing <query>` — Bing image search"""),

    ("📝 NOTES & FILTERS — Group", """\
**Notes:**
`/save <name> <content>` — Save a note
`#notename` — Get saved note
`/notes` — List all notes
`/clear <name>` — Delete a note
`/privatenotes on/off` — Send notes in DM

**Filters:**
`/filter <keyword> <reply>` — Add filter
`/filters` — List all filters
`/stop <keyword>` — Remove filter"""),

    ("📊 STATS & INFO", """\
`/stats` — Bot statistics
`/gstats` — Group music stats
`/queue` — Current playing queue
`/userid` — Get user/chat ID
`/groupinfo` — Group information
`/gpdata` — Group data
`/mongochk` — MongoDB status
`/state` — Bot state info

**Owner Remote (from DM):**
`/rmstats` — Bot-wide stats from DM
`/rmqueue <chat_id>` — Check queue of any group"""),
]


@app.on_message(filters.command("ownerguide") & filters.private & ~BANNED_USERS)
async def owner_guide_cmd(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner ke liye hai.")

    await message.reply_text(
        "╔══「 👑 <b>NOBITA X PRIME — Owner Guide</b> 」\n"
        "║\n"
        "║  Sab commands ki poori list neeche hai.\n"
        "║  Har section alag message mein aayega.\n"
        "║\n"
        "╚════════════════════════"
    )

    for title, body in GUIDE_SECTIONS:
        await message.reply_text(
            f"<b>━━━ {title} ━━━</b>\n\n{body}",
            parse_mode="markdown",
        )

    await message.reply_text(
        "✅ <b>Guide Complete!</b>\n\n"
        "💡 <b>Remote Commands (DM se kisi bhi group ko control karo):</b>\n"
        "<code>/rmchatbot &lt;chat_id&gt; on/off</code>\n"
        "<code>/rmautoreport &lt;chat_id&gt; on/off</code>\n"
        "<code>/rmqueue &lt;chat_id&gt;</code>\n"
        "<code>/rmstats</code>\n\n"
        "🔑 <b>Session Commands:</b>\n"
        "<code>/addsession &lt;string&gt;</code>\n"
        "<code>/listsessions</code>\n"
        "<code>/removesession &lt;slot&gt;</code>"
    )


# ═══════════════════════════════════════════
#  REMOTE CONTROL COMMANDS (from DM)
# ═══════════════════════════════════════════

@app.on_message(filters.command("rmchatbot") & filters.private & ~BANNED_USERS)
async def remote_chatbot(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner.")
    args = message.command
    if len(args) < 3 or args[2].lower() not in ("on", "off"):
        return await message.reply_text(
            "Usage: <code>/rmchatbot &lt;chat_id&gt; on/off</code>\n"
            "Example: <code>/rmchatbot -1001234567890 on</code>"
        )
    try:
        chat_id = int(args[1])
    except ValueError:
        return await message.reply_text("❌ chat_id number hona chahiye (e.g. -1001234567890)")
    val = args[2].lower() == "on"
    await _chatbot_col.update_one(
        {"chat_id": chat_id}, {"$set": {"enabled": val}}, upsert=True
    )
    status = "✅ ON" if val else "❌ OFF"
    await message.reply_text(f"🤖 Chatbot <b>{status}</b> for chat <code>{chat_id}</code>")


@app.on_message(filters.command("rmautoreport") & filters.private & ~BANNED_USERS)
async def remote_autoreport(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner.")
    args = message.command
    if len(args) < 3 or args[2].lower() not in ("on", "off"):
        return await message.reply_text(
            "Usage: <code>/rmautoreport &lt;chat_id&gt; on/off</code>\n"
            "Example: <code>/rmautoreport -1001234567890 on</code>"
        )
    try:
        chat_id = int(args[1])
    except ValueError:
        return await message.reply_text("❌ chat_id number hona chahiye.")
    val = args[2].lower() == "on"
    await _autoreport_col.update_one(
        {"chat_id": chat_id}, {"$set": {"enabled": val}}, upsert=True
    )
    status = "✅ ON" if val else "❌ OFF"
    await message.reply_text(f"🛡️ Auto-Report <b>{status}</b> for chat <code>{chat_id}</code>")


@app.on_message(filters.command("rmstats") & filters.private & ~BANNED_USERS)
async def remote_stats(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner.")
    try:
        chats = await get_served_chats()
        users = await get_served_users()
        await message.reply_text(
            "📊 <b>Bot Statistics</b>\n\n"
            f"👥 <b>Served Groups:</b> <code>{len(chats)}</code>\n"
            f"👤 <b>Served Users:</b> <code>{len(users)}</code>\n"
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>")


@app.on_message(filters.command("rmqueue") & filters.private & ~BANNED_USERS)
async def remote_queue(_, message: Message):
    if not _is_owner(message):
        return await message.reply_text("❌ Sirf Owner.")
    args = message.command
    if len(args) < 2:
        return await message.reply_text(
            "Usage: <code>/rmqueue &lt;chat_id&gt;</code>"
        )
    try:
        chat_id = int(args[1])
    except ValueError:
        return await message.reply_text("❌ chat_id number hona chahiye.")

    if not await is_active_chat(chat_id):
        return await message.reply_text(f"📭 Chat <code>{chat_id}</code> mein koi music nahi chal raha.")

    got = _stream_db.get(chat_id)
    if not got:
        return await message.reply_text("📭 Queue empty hai.")

    now = got[0]
    lines = [
        f"🎵 <b>Now Playing in</b> <code>{chat_id}</code>\n",
        f"<b>Title:</b> {now.get('title','Unknown')[:60]}",
        f"<b>By:</b> {now.get('by','Unknown')}",
        f"<b>Type:</b> {now.get('streamtype','Unknown')}",
    ]
    if len(got) > 1:
        lines.append(f"\n📋 <b>Queue ({len(got)-1} more):</b>")
        for i, item in enumerate(got[1:6], 1):
            lines.append(f"  {i}. {item.get('title','Unknown')[:50]}")
    await message.reply_text("\n".join(lines))


# ═══════════════════════════════════════════
#  STATS in private (for owner)
# ═══════════════════════════════════════════

@app.on_message(filters.command(["stats", "gstats"]) & filters.private & ~BANNED_USERS)
async def stats_private(_, message: Message):
    if not _is_owner(message):
        return
    try:
        chats = await get_served_chats()
        users = await get_served_users()
        await message.reply_text(
            "📊 <b>NOBITA X PRIME — Bot Stats</b>\n\n"
            f"👥 <b>Groups:</b> <code>{len(chats)}</code>\n"
            f"👤 <b>Users:</b> <code>{len(users)}</code>\n\n"
            "Use <code>/rmstats</code> for the same, or <code>/rmqueue &lt;chat_id&gt;</code> "
            "to check queue of any group."
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>")
