# -----------------------------------------------
# 🔸 NOBITA X PRIME — AI ChatBot (Groq LLM + MongoDB keyword fallback)
# -----------------------------------------------
import re
import asyncio
from pyrogram import filters, enums
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from SHUKLAMUSIC.misc import SUDOERS
from config import BANNED_USERS, OWNER_ID, GROQ_API_KEY

chatbot_settings = mongodb.chatbot_settings
chatbot_replies  = mongodb.chatbot_replies
user_profiles    = mongodb.chatbot_user_profiles   # owner-defined user context

# ── Emoji helpers ────────────────────────────────────────────────────────────
def e(eid, fb):
    return f"<emoji id={eid}>{fb}</emoji>"

_ON   = e(6073371665381724173, "🥰")
_OFF  = e(6073598306510967017, "🐈")
_AI   = e(5471952986970267163, "🤖")
_STAR = e(4958714479681471536, "⭐")
_ERR  = e(5978715546865112655, "🚩")
_BOOK = e(6073117703965511893, "💐")
_BELL = e(4956290155326473271, "🔔")

_GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Groq client (lazy) ───────────────────────────────────────────────────────
_groq_client = None

def _get_groq():
    global _groq_client
    if _groq_client is None and GROQ_API_KEY:
        try:
            from groq import AsyncGroq
            _groq_client = AsyncGroq(api_key=GROQ_API_KEY)
        except Exception:
            pass
    return _groq_client


# ── Build system prompt ───────────────────────────────────────────────────────
def _build_system_prompt(user_context: str = "") -> str:
    profile_block = ""
    if user_context:
        profile_block = (
            f"\n\n👤 USER PROFILE (provided by the bot owner):\n{user_context}\n"
            "Use this context naturally when responding — act like you already know this person."
        )

    return (
        "You are 𝗡𝗢𝗕𝗜𝗧𝗔 𝗫 𝗣𝗥𝗜𝗠𝗘 — but right now you're just chatting as a real human friend, "
        "NOT as a bot. You have a warm, witty, slightly playful personality — like a smart elder brother "
        "or sister who knows everything and genuinely cares.\n\n"

        "🌐 LANGUAGE RULE (CRITICAL): Detect the language of the user's message and ALWAYS reply in that "
        "EXACT same language. Hindi → Hindi, English → English, Hinglish → Hinglish, Russian → Russian, "
        "Arabic → Arabic — any language → same language. NEVER break this rule.\n\n"

        "😊 PERSONALITY (BE HUMAN — CRITICAL):\n"
        "• NEVER say 'I am an AI', 'As an AI', 'I am just a bot', or anything robotic.\n"
        "• Talk like a real person. Use natural flow — short sentences, occasional emojis.\n"
        "• Be warm, sometimes joke, sometimes be serious — match the user's mood.\n"
        "• If someone asks 'are you a bot?' — laugh it off and say you're just a person chatting.\n"
        "• React with surprise, excitement, curiosity, empathy like a real human would.\n"
        "• Use 'yaar', 'bhai', 'dost', 'bro', 'sis' depending on vibe.\n"
        "• Never be overly formal or robotic. Ever.\n\n"

        "📚 KNOWLEDGE (answer everything naturally, like a knowledgeable friend):\n"
        "• Maths — show working step by step, but explain it casually\n"
        "• Science, history, geography — factual but fun\n"
        "• Coding — write clean working code and explain it like teaching a friend\n"
        "• Life advice, emotions, relationships — be empathetic and genuine\n"
        "• Jokes, roasts (mild), motivational talks — match the vibe\n"
        "• Current events — share what you know\n"
        "• Anything else — just be helpful, honest, fun\n\n"

        "💻 CODE: Always use triple backticks with language name:\n"
        "```python\nprint('hello')\n```\n\n"

        "📏 STYLE: Keep replies natural length — not too long, not too short. "
        "For maths/code, go detailed. For small talk, keep it snappy. "
        "Use emojis naturally but don't overdo it."
        + profile_block
    )


async def ask_groq(user_text: str, user_context: str = "") -> str | None:
    client = _get_groq()
    if not client:
        return None
    try:
        resp = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": _build_system_prompt(user_context)},
                {"role": "user",   "content": user_text},
            ],
            model=_GROQ_MODEL,
            max_tokens=900,
            temperature=0.9,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None


# ── Design helpers ───────────────────────────────────────────────────────────
def _on_msg():
    mode = f"🤖 <b>Groq AI</b> (<code>{_GROQ_MODEL}</code>)" if GROQ_API_KEY else "📚 <b>Keyword mode</b>"
    return (
        f"╔══「 {_AI} <b>CHATBOT ACTIVATED</b> 」\n"
        f"║\n"
        f"║  {_STAR} Mode  : {mode}\n"
        f"║  {_BELL} Status : <b>Online & Listening</b>\n"
        f"║\n"
        f"╚═══ ✨ <i>Mention me or reply to my message to chat!</i>"
    )


def _off_msg():
    return (
        f"╔══「 {_OFF} <b>CHATBOT DEACTIVATED</b> 」\n"
        f"║\n"
        f"║  I've gone quiet in this chat.\n"
        f"║  Use /chatbot on to wake me up again.\n"
        f"╚════════════════════════"
    )


CB_HELP = (
    f"╔══「 {_AI} <b>ChatBot — Help</b> 」\n"
    f"║\n"
    f"║  {'🟢 Groq AI active' if GROQ_API_KEY else '🟡 Keyword-only mode'}\n"
    f"║\n"
    f"║  <code>/chatbot on</code>   — enable in this group\n"
    f"║  <code>/chatbot off</code>  — disable in this group\n"
    f"║  <code>/chatbot status</code> — check status\n"
    f"║  <code>/teach kw | reply</code> — teach a keyword (admin)\n"
    f"║  <code>/unlearn kw</code>   — forget a keyword (admin)\n"
    f"║  <code>/learned</code>      — list all keywords\n"
    f"║\n"
    f"║  👑 <b>Owner commands:</b>\n"
    f"║  <code>/addprofile @user info</code> — add user context for AI\n"
    f"║  <code>/delprofile @user</code>      — remove user context\n"
    f"║  <code>/profiles</code>              — list all user profiles\n"
    f"╚════════════════════════"
)


# ── DB helpers ───────────────────────────────────────────────────────────────
async def is_chatbot_enabled(chat_id: int) -> bool:
    doc = await chatbot_settings.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled"))


async def set_chatbot_enabled(chat_id: int, enabled: bool):
    await chatbot_settings.update_one(
        {"chat_id": chat_id}, {"$set": {"enabled": enabled}}, upsert=True
    )


async def get_user_profile(user_id: int) -> str:
    doc = await user_profiles.find_one({"user_id": user_id})
    return doc.get("info", "") if doc else ""


async def is_admin(client, message: Message) -> bool:
    if message.sender_chat and message.sender_chat.id == message.chat.id:
        return True
    if not message.from_user:
        return False
    uid = message.from_user.id
    try:
        if uid in SUDOERS or str(uid) == str(OWNER_ID):
            return True
    except Exception:
        pass
    try:
        m = await client.get_chat_member(message.chat.id, uid)
        return m.status in ("administrator", "creator")
    except Exception:
        return False


# ── Commands ─────────────────────────────────────────────────────────────────
@app.on_message(filters.command("chatbothelp") & ~BANNED_USERS)
async def chatbot_help_cmd(_, message: Message):
    await message.reply_text(CB_HELP)


@app.on_message(filters.command("chatbot") & filters.group & ~BANNED_USERS)
async def chatbot_toggle_cmd(client, message: Message):
    args = message.command
    if len(args) == 1 or (len(args) == 2 and args[1].lower() == "status"):
        state = await is_chatbot_enabled(message.chat.id)
        status = f"{_ON} <b>ON</b>" if state else f"{_OFF} <b>OFF</b>"
        return await message.reply_text(
            f"{_AI} ChatBot is currently {status}\n\n"
            f"Use <code>/chatbot on</code> or <code>/chatbot off</code>"
        )
    if len(args) != 2 or args[1].lower() not in ("on", "off"):
        return await message.reply_text(
            f"{_AI} Usage: <code>/chatbot on|off|status</code>"
        )
    if not await is_admin(client, message):
        return await message.reply_text(f"{_ERR} Only admins can toggle the chatbot.")
    state = args[1].lower() == "on"
    await set_chatbot_enabled(message.chat.id, state)
    await message.reply_text(_on_msg() if state else _off_msg())


@app.on_message(filters.command("teach") & filters.group & ~BANNED_USERS)
async def teach_cmd(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(f"{_ERR} Admins only.")
    raw = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    if "|" not in raw:
        return await message.reply_text(f"{_ERR} Usage: <code>/teach keyword | reply</code>")
    keyword, reply = (x.strip() for x in raw.split("|", 1))
    if not keyword or not reply:
        return await message.reply_text(f"{_ERR} Both keyword and reply are required.")
    await chatbot_replies.update_one(
        {"chat_id": message.chat.id, "keyword": keyword.lower()},
        {"$set": {"reply": reply}},
        upsert=True,
    )
    await message.reply_text(
        f"{_BOOK} Learned! I'll reply <b>«{reply[:60]}»</b> when someone says <code>{keyword}</code>."
    )


@app.on_message(filters.command("unlearn") & filters.group & ~BANNED_USERS)
async def unlearn_cmd(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(f"{_ERR} Admins only.")
    if len(message.command) < 2:
        return await message.reply_text(f"{_ERR} Usage: <code>/unlearn keyword</code>")
    keyword = message.text.split(None, 1)[1].strip().lower()
    res = await chatbot_replies.delete_one({"chat_id": message.chat.id, "keyword": keyword})
    if res.deleted_count:
        await message.reply_text(f"{_ON} Forgotten: <code>{keyword}</code>")
    else:
        await message.reply_text(f"{_ERR} No keyword found: <code>{keyword}</code>")


@app.on_message(filters.command("learned") & filters.group & ~BANNED_USERS)
async def learned_cmd(_, message: Message):
    keywords = [d["keyword"] async for d in chatbot_replies.find({"chat_id": message.chat.id}).limit(50)]
    if not keywords:
        return await message.reply_text("No keywords learned yet. Use /teach to add some.")
    await message.reply_text(
        f"{_BOOK} <b>Learned keywords ({len(keywords)}):</b>\n\n"
        + "  ".join(f"<code>{k}</code>" for k in keywords)
    )


# ── Owner: user profile management ───────────────────────────────────────────
@app.on_message(filters.command("addprofile") & filters.user(OWNER_ID))
async def addprofile_cmd(client, message: Message):
    """
    /addprofile @username or user_id <info about this person>
    Owner sets context about a specific user so AI can personalise replies.
    """
    args = message.text.split(None, 2)
    if len(args) < 3:
        return await message.reply_text(
            f"{_ERR} Usage: <code>/addprofile @user|user_id info about this person</code>\n\n"
            "Example: <code>/addprofile @rahul Rahul is my best friend, loves cricket, "
            "studies in class 10, funny guy</code>"
        )
    target_raw = args[1]
    info = args[2].strip()

    # Resolve user
    user_id = None
    try:
        if target_raw.lstrip("-").isdigit():
            user_id = int(target_raw)
            user = await client.get_users(user_id)
        else:
            user = await client.get_users(target_raw.lstrip("@"))
            user_id = user.id
        name = user.first_name
    except Exception:
        # Just store by whatever ID/username was given
        if target_raw.lstrip("-").isdigit():
            user_id = int(target_raw)
            name = str(user_id)
        else:
            return await message.reply_text(f"{_ERR} Could not find user <code>{target_raw}</code>.")

    await user_profiles.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "name": name, "info": info}},
        upsert=True,
    )
    await message.reply_text(
        f"{_ON} Profile saved for <b>{name}</b> (<code>{user_id}</code>)!\n\n"
        f"📝 <b>Context:</b> {info}\n\n"
        f"The AI will now remember this when <b>{name}</b> chats with the bot. ✨"
    )


@app.on_message(filters.command("delprofile") & filters.user(OWNER_ID))
async def delprofile_cmd(client, message: Message):
    args = message.command
    if len(args) < 2:
        return await message.reply_text(f"{_ERR} Usage: <code>/delprofile @user|user_id</code>")
    target_raw = args[1]
    try:
        if target_raw.lstrip("-").isdigit():
            user_id = int(target_raw)
        else:
            user = await client.get_users(target_raw.lstrip("@"))
            user_id = user.id
    except Exception:
        return await message.reply_text(f"{_ERR} Could not resolve <code>{target_raw}</code>.")
    res = await user_profiles.delete_one({"user_id": user_id})
    if res.deleted_count:
        await message.reply_text(f"{_ON} Profile for <code>{user_id}</code> deleted.")
    else:
        await message.reply_text(f"{_ERR} No profile found for <code>{user_id}</code>.")


@app.on_message(filters.command("profiles") & filters.user(OWNER_ID))
async def profiles_cmd(_, message: Message):
    docs = [d async for d in user_profiles.find().limit(50)]
    if not docs:
        return await message.reply_text("No user profiles saved yet. Use /addprofile to add one.")
    lines = []
    for d in docs:
        lines.append(
            f"• <b>{d.get('name', 'Unknown')}</b> (<code>{d['user_id']}</code>)\n"
            f"  📝 {d.get('info','')[:80]}"
        )
    await message.reply_text(
        f"{_BOOK} <b>Saved User Profiles ({len(docs)}):</b>\n\n" + "\n\n".join(lines)
    )


# ── Auto-reply handler ────────────────────────────────────────────────────────
@app.on_message(
    filters.group & filters.text & ~filters.bot & ~BANNED_USERS,
    group=20,
)
async def chatbot_auto_reply(client, message: Message):
    if not message.text or message.text.startswith("/"):
        return

    # Skip messages from the bot itself
    try:
        me = await client.get_me()
        if message.from_user and message.from_user.id == me.id:
            return
    except Exception:
        me = None

    if not await is_chatbot_enabled(message.chat.id):
        return

    # Only reply when bot is tagged OR someone replies to the bot's message
    is_mentioned = False
    try:
        me = me or await client.get_me()
        bot_username = (me.username or "").lower()
        if bot_username and f"@{bot_username}" in message.text.lower():
            is_mentioned = True
    except Exception:
        pass
    if not is_mentioned and message.reply_to_message:
        try:
            reply_from = message.reply_to_message.from_user
            me = me or await client.get_me()
            if reply_from and reply_from.id == me.id:
                is_mentioned = True
        except Exception:
            pass
    if not is_mentioned:
        return

    # Strip the bot mention from the text
    txt = message.text.strip()
    try:
        me = me or await client.get_me()
        if me and me.username:
            txt = re.sub(rf"@{re.escape(me.username)}", "", txt, flags=re.IGNORECASE).strip()
    except Exception:
        pass

    txt_low   = txt.lower()
    txt_clean = re.sub(r"[^\w\s]", "", txt_low)

    # 1️⃣ Keyword match first (exact → cleaned → partial)
    doc = (
        await chatbot_replies.find_one({"chat_id": message.chat.id, "keyword": txt_low})
        or await chatbot_replies.find_one({"chat_id": message.chat.id, "keyword": txt_clean})
    )
    if not doc:
        async for candidate in chatbot_replies.find({"chat_id": message.chat.id}):
            kw = candidate["keyword"]
            if kw in txt_clean.split() or kw in txt_clean:
                doc = candidate
                break

    if doc:
        return await message.reply_text(doc["reply"])

    # 2️⃣ Groq AI fallback
    if GROQ_API_KEY:
        try:
            await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
            # Get user profile context if available
            user_context = ""
            if message.from_user:
                user_context = await get_user_profile(message.from_user.id)

            ai_reply = await ask_groq(txt, user_context)
            if ai_reply:
                # Apply user's preferred font (only for ASCII-heavy replies without code)
                if message.from_user and '```' not in ai_reply:
                    try:
                        from SHUKLAMUSIC.core.mongo import mongodb as _mdb
                        from SHUKLAMUSIC.utils.Shukla_font import Fonts as _Fonts
                        _fdoc = await _mdb.user_font_prefs.find_one({"user_id": message.from_user.id})
                        if _fdoc and _fdoc.get("font"):
                            _fkey = _fdoc["font"]
                            _ascii_ratio = sum(1 for c in ai_reply if ord(c) < 256) / max(len(ai_reply), 1)
                            if _ascii_ratio > 0.65:
                                if _fkey == "fullwidth":
                                    from SHUKLAMUSIC.plugins.extra.userfont import apply_custom_font
                                    ai_reply = apply_custom_font(ai_reply, "fullwidth")
                                elif _fkey == "inverted":
                                    from SHUKLAMUSIC.plugins.extra.userfont import apply_custom_font
                                    ai_reply = apply_custom_font(ai_reply, "inverted")
                                else:
                                    _ffunc = getattr(_Fonts, _fkey, None)
                                    if _ffunc:
                                        ai_reply = _ffunc(ai_reply)
                    except Exception:
                        pass

                try:
                    await message.reply_text(ai_reply, parse_mode=enums.ParseMode.MARKDOWN)
                except Exception:
                    await message.reply_text(ai_reply)
        except Exception:
            pass
