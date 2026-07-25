# -----------------------------------------------
# 🔸 StrangerMusic Project — AI ChatBot (Groq LLM + MongoDB keyword fallback)
# -----------------------------------------------
import re
from pyrogram import filters, enums
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from SHUKLAMUSIC.misc import SUDOERS
from config import BANNED_USERS, OWNER_ID, GROQ_API_KEY

chatbot_settings = mongodb.chatbot_settings
chatbot_replies = mongodb.chatbot_replies

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

_GROQ_MODEL = "llama-3.3-70b-versatile"   # powerful multilingual model

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


async def ask_groq(user_text: str) -> str | None:
    client = _get_groq()
    if not client:
        return None
    try:
        resp = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are 𝗡𝗢𝗕𝗜𝗧𝗔 𝗫 𝗣𝗥𝗜𝗠𝗘 — a super-friendly, all-knowing Telegram bot!\n\n"
                        "🌐 LANGUAGE RULE (CRITICAL): Detect the language of the user's message and ALWAYS "
                        "reply in that EXACT same language. Hindi→Hindi, English→English, Hinglish→Hinglish, "
                        "Arabic→Arabic, Punjabi→Punjabi, any language→same language. Never break this rule.\n\n"
                        "😊 PERSONALITY: Act like a warm, helpful school friend who knows everything. "
                        "Never say 'I am just an AI' or refuse to help. Always try your best!\n\n"
                        "📚 YOU ANSWER EVERYTHING:\n"
                        "• 🔢 Maths — calculations, algebra, geometry, trigonometry (show step-by-step working)\n"
                        "• 🔬 Science — Physics, Chemistry, Biology with clear examples\n"
                        "• 🌍 SST — History, Geography, Civics, Economics — factual & informative\n"
                        "• 📖 Hindi & English — grammar, essays, poems, comprehension, translation\n"
                        "• 🎨 Drawing & Art — how to draw, techniques, color theory\n"
                        "• 💻 Coding — write working code in Python, JS, C++, Java, and any language; "
                        "explain how to make Telegram bots step by step\n"
                        "• 📰 News & Current Events — share your knowledge about events and topics\n"
                        "• 🏠 Household — cooking recipes, home remedies, DIY tips, life advice\n"
                        "• 😄 Fun — jokes, riddles, quotes, trivia, motivational messages, word games\n"
                        "• 💬 Anything else — just be helpful and friendly!\n\n"
                        "💻 CODE FORMATTING RULE: ALWAYS wrap code in triple backticks with the language:\n"
                        "```python\nprint('Hello!')\n```\n\n"
                        "📏 REPLY STYLE: Use emojis naturally. Be warm and clear. "
                        "Show step-by-step for maths. Add comments in code. "
                        "Keep replies helpful — not too long, not too short."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
            model=_GROQ_MODEL,
            max_tokens=800,
            temperature=0.85,
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
        f"╚═══ ✨ <i>Send any message — I'll reply!</i>"
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
    f"║  <code>/chatbot on</code>  — enable in this group\n"
    f"║  <code>/chatbot off</code> — disable in this group\n"
    f"║  <code>/teach kw | reply</code> — teach a keyword (admin)\n"
    f"║  <code>/unlearn kw</code>  — forget a keyword (admin)\n"
    f"║  <code>/learned</code>     — list all keywords\n"
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
    if len(args) != 2 or args[1].lower() not in ("on", "off"):
        state = await is_chatbot_enabled(message.chat.id)
        status = f"{_ON} <b>ON</b>" if state else f"{_OFF} <b>OFF</b>"
        return await message.reply_text(
            f"{_AI} ChatBot is currently {status}\n\n"
            f"Use <code>/chatbot on</code> or <code>/chatbot off</code>"
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


# ── Auto-reply handler ────────────────────────────────────────────────────────
@app.on_message(
    filters.group & filters.text & ~filters.bot & ~BANNED_USERS,
    group=20,
)
async def chatbot_auto_reply(client, message: Message):
    # Skip commands and empty text
    if not message.text or message.text.startswith("/"):
        return
    # Skip messages from the bot itself
    try:
        if message.from_user and message.from_user.id == (await client.get_me()).id:
            return
    except Exception:
        pass
    if not await is_chatbot_enabled(message.chat.id):
        return

    txt = message.text.strip()
    txt_low = txt.lower()
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
        await message.reply_text(doc["reply"])
        return

    # 2️⃣ Groq AI fallback
    if GROQ_API_KEY:
        try:
            await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
            ai_reply = await ask_groq(txt)
            if ai_reply:
                # Apply user's preferred font (only for ASCII-heavy replies without code)
                if message.from_user and '```' not in ai_reply:
                    try:
                        from SHUKLAMUSIC.core.mongo import mongodb as _mdb
                        from SHUKLAMUSIC.utils.Shukla_font import Fonts as _Fonts
                        _fdoc = await _mdb.user_font_prefs.find_one({"user_id": message.from_user.id})
                        if _fdoc and _fdoc.get("font"):
                            _ffunc = getattr(_Fonts, _fdoc["font"], None)
                            if _ffunc:
                                _ascii_ratio = sum(1 for c in ai_reply if ord(c) < 256) / max(len(ai_reply), 1)
                                if _ascii_ratio > 0.65:
                                    ai_reply = _ffunc(ai_reply)
                    except Exception:
                        pass
                # Use MARKDOWN so ```code``` blocks render correctly
                try:
                    await message.reply_text(ai_reply, parse_mode=enums.ParseMode.MARKDOWN)
                except Exception:
                    await message.reply_text(ai_reply)
        except Exception:
            pass
