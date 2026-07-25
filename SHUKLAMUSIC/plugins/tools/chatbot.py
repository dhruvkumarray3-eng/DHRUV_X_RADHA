# -----------------------------------------------
# 🔸 StrangerMusic Project — AI ChatBot (Groq + MongoDB fallback)
# 🔹 Uses Groq LLM when GROQ_API_KEY is set; falls back to keyword auto-reply
# -----------------------------------------------
import re
from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from SHUKLAMUSIC.utils.database import is_nonadmin_chat
from SHUKLAMUSIC.misc import SUDOERS
from config import BANNED_USERS, OWNER_ID, GROQ_API_KEY

chatbot_settings = mongodb.chatbot_settings
chatbot_replies = mongodb.chatbot_replies

_E_ON = 6073371665381724173
_E_OFF = 6073598306510967017
_E_LEARN = 6073117703965511893
_E_ERR = 5978715546865112655
_E_AI = 5471952986970267163


def e(eid, fb):
    return f"<emoji id={eid}>{fb}</emoji>"


# ── Groq client (lazy init) ──────────────────────────────────────────────────
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
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly, helpful Telegram music bot assistant. "
                        "Keep replies short and conversational (1-3 sentences). "
                        "You help users with music, fun chats, and general questions."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
            model="llama3-8b-8192",
            max_tokens=300,
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception:
        return None


CB_HELP = f"""
{e(_E_AI,'🤖')} <b>ChatBot — Command List</b>

{"🟢 <b>AI mode active</b> (Groq LLM)" if GROQ_API_KEY else "🟡 <b>Keyword mode</b> (no GROQ_API_KEY set)"}

• <code>/chatbot on</code> — enable chatbot in this group
• <code>/chatbot off</code> — disable chatbot in this group
• <code>/teach &lt;keyword&gt; | &lt;reply&gt;</code> — teach a keyword reply (admin only)
• <code>/unlearn &lt;keyword&gt;</code> — remove a taught reply (admin only)
• <code>/learned</code> — list learned keywords in this chat
"""


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
    user_id = message.from_user.id
    try:
        if user_id in SUDOERS or str(user_id) == str(OWNER_ID):
            return True
    except Exception:
        pass
    try:
        member = await client.get_chat_member(message.chat.id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


@app.on_message(filters.command("chatbothelp") & ~BANNED_USERS)
async def chatbot_help_cmd(client, message: Message):
    await message.reply_text(CB_HELP)


@app.on_message(filters.command("chatbot") & filters.group & ~BANNED_USERS)
async def chatbot_toggle_cmd(client, message: Message):
    if len(message.command) != 2 or message.command[1].lower() not in ("on", "off"):
        state = await is_chatbot_enabled(message.chat.id)
        mode = "🤖 Groq AI" if GROQ_API_KEY else "📚 Keyword"
        status = f"{e(_E_ON,'🥰')} <b>ON</b>" if state else f"{e(_E_OFF,'🐈')} <b>OFF</b>"
        return await message.reply_text(
            f"{e(_E_AI,'🤖')} <b>ChatBot status:</b> {status} | Mode: {mode}\n\n"
            f"Usage: <code>/chatbot on</code> or <code>/chatbot off</code>"
        )
    if not await is_admin(client, message):
        return await message.reply_text(f"{e(_E_ERR,'🚩')} Only group admins can toggle the chatbot.")
    state = message.command[1].lower() == "on"
    await set_chatbot_enabled(message.chat.id, state)
    mode = "🤖 Groq AI" if GROQ_API_KEY else "📚 Keyword"
    if state:
        await message.reply_text(
            f"{e(_E_ON,'🥰')} <b>ChatBot enabled</b> [{mode}] — I will now reply to messages in this chat."
        )
    else:
        await message.reply_text(f"{e(_E_OFF,'🐈')} <b>ChatBot disabled</b> for this chat.")


@app.on_message(filters.command("teach") & filters.group & ~BANNED_USERS)
async def teach_cmd(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(f"{e(_E_ERR,'🚩')} Only group admins can teach the chatbot.")
    if len(message.command) < 2 or "|" not in message.text:
        return await message.reply_text(f"{e(_E_ERR,'🚩')} Usage: <code>/teach keyword | reply text</code>")
    raw = message.text.split(None, 1)[1]
    if "|" not in raw:
        return await message.reply_text(f"{e(_E_ERR,'🚩')} Usage: <code>/teach keyword | reply text</code>")
    keyword, reply = raw.split("|", 1)
    keyword = keyword.strip().lower()
    reply = reply.strip()
    if not keyword or not reply:
        return await message.reply_text(f"{e(_E_ERR,'🚩')} Both keyword and reply are required.")
    await chatbot_replies.update_one(
        {"chat_id": message.chat.id, "keyword": keyword},
        {"$set": {"reply": reply}},
        upsert=True,
    )
    await message.reply_text(
        f"{e(_E_LEARN,'💐')} Learned! When someone says <b>{keyword}</b>, I'll reply with that text."
    )


@app.on_message(filters.command("unlearn") & filters.group & ~BANNED_USERS)
async def unlearn_cmd(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply_text(f"{e(_E_ERR,'🚩')} Only group admins can do this.")
    if len(message.command) < 2:
        return await message.reply_text(f"{e(_E_ERR,'🚩')} Usage: <code>/unlearn keyword</code>")
    keyword = message.text.split(None, 1)[1].strip().lower()
    result = await chatbot_replies.delete_one({"chat_id": message.chat.id, "keyword": keyword})
    if result.deleted_count:
        await message.reply_text(f"{e(_E_ON,'🥰')} Forgot the reply for <b>{keyword}</b>.")
    else:
        await message.reply_text(f"{e(_E_ERR,'🚩')} No learned reply found for that keyword.")


@app.on_message(filters.command("learned") & filters.group & ~BANNED_USERS)
async def learned_cmd(client, message: Message):
    cursor = chatbot_replies.find({"chat_id": message.chat.id}).limit(50)
    keywords = [doc["keyword"] async for doc in cursor]
    if not keywords:
        return await message.reply_text(
            "I haven't learned any keywords in this chat yet. Teach me with /teach."
        )
    text = (
        f"{e(_E_LEARN,'💐')} <b>Learned keywords in this chat:</b>\n\n"
        + ", ".join(f"<code>{k}</code>" for k in keywords)
    )
    await message.reply_text(text)


@app.on_message(
    filters.group
    & filters.text
    & ~filters.bot
    & ~filters.command(["teach", "unlearn", "learned", "chatbot"])
    & ~BANNED_USERS,
    group=20,
)
async def chatbot_auto_reply(client, message: Message):
    if not message.text or message.text.startswith("/"):
        return
    if not await is_chatbot_enabled(message.chat.id):
        return

    text = message.text.strip().lower()
    text_clean = re.sub(r"[^\w\s]", "", text)

    # 1️⃣ Always check taught keywords first (exact → cleaned → partial)
    doc = await chatbot_replies.find_one({"chat_id": message.chat.id, "keyword": text})
    if not doc:
        doc = await chatbot_replies.find_one({"chat_id": message.chat.id, "keyword": text_clean})
    if not doc:
        cursor = chatbot_replies.find({"chat_id": message.chat.id})
        async for candidate in cursor:
            if candidate["keyword"] in text_clean.split() or candidate["keyword"] in text_clean:
                doc = candidate
                break

    if doc:
        try:
            await message.reply_text(doc["reply"])
        except Exception:
            pass
        return

    # 2️⃣ Fall back to Groq AI when no keyword matched
    if GROQ_API_KEY:
        try:
            ai_reply = await ask_groq(message.text.strip())
            if ai_reply:
                await message.reply_text(ai_reply)
        except Exception:
            pass
