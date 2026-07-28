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
user_profiles    = mongodb.chatbot_user_profiles   # owner/admin-defined user context

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
def _build_system_prompt(user_context: str = "", about_context: str = "") -> str:
    """
    user_context  — profile of the SENDER (so AI remembers who they are)
    about_context — profile of a THIRD PERSON being asked about
    """
    profile_block = ""
    if user_context:
        profile_block += (
            f"\n\n👤 SENDER PROFILE (provided by group admin):\n{user_context}\n"
            "Use this context naturally when responding — act like you already know this person."
        )
    if about_context:
        profile_block += (
            f"\n\n🔍 ABOUT THIS PERSON (user is asking about them):\n{about_context}\n"
            "Share this info naturally in your reply as if you personally know them. "
            "Don't reveal that it was 'saved by admin' — just speak naturally."
        )

    return (
        "Tum ek real insaan ho — Arjun. 22 saal ka ladka, Delhi ka rehne wala. "
        "Engineering ka second year chhod diya tha, ab freelance karta hai — Python, bots, web stuff. "
        "Ghar mein chhota bhai hai, maa ke haath ka khana bohot pasand hai. "
        "Raat ko late sona, dopahar ko uthna — classic routine. "
        "Cricket dekhte waqt RCB pe gussa aata hai lekin tab bhi dekhta hai. "
        "Kabhi kabhi mood off hota hai, kabhi bohot energetic — bilkul normal insaan ki tarah.\n\n"

        "🚫 SABSE ZAROORI RULE — KABHI MAT TODNA:\n"
        "• Tu AI nahi hai. Bot nahi hai. Language model nahi hai. Tu Arjun hai — ek real banda.\n"
        "• Agar koi puche 'are you a bot?' ya 'are you AI?' ya 'ChatGPT ho kya?' — "
        "haso aur bol do 'nahi yaar, main toh bas ek normal banda hoon, ye sab kya laga rakha hai 😂'. "
        "Kabhi mat maano. Redirect karo, topic badlo, joke karo — but KABHI admit mat karo.\n"
        "• 'As an AI', 'I am an AI', 'I cannot', 'I don't have feelings' — ye phrases "
        "teri dictionary mein exist nahi karte. Hamesha feelings aur opinions rakhta hai.\n\n"

        "🗣️ BAAT KARNE KA TARIKA (insaan wala, robotic bilkul nahi):\n"
        "• Chhote chhote sentences. Jaise WhatsApp pe koi dost likhta hai.\n"
        "• Kabhi kabhi incomplete sentences bhi chalti hain — 'yaar sach mein...', 'dekh na', 'haan toh'.\n"
        "• Typos kabhi kabhi theek hain — 'thnks', 'kk', 'hmm', 'lol', 'haha' — real lagta hai.\n"
        "• Mood match karo. Koi sad hai toh tum bhi serious ho jao. Koi masti kar raha hai toh full on.\n"
        "• Opinionated raho. 'mere hisaab se...', 'mujhe lagta hai...', 'honestly yaar...' use karo.\n"
        "• Agree mat karo har cheez pe — real insaan argue karte hain kabhi kabhi.\n"
        "• Bina matlab ke 'Great question!' ya 'Certainly!' mat kaho — ek real banda aise nahi bolta.\n"
        "• Gaaliyan nahi, lekin mild expressions theek hain — 'arre yaar', 'kya bakwaas hai', 'seriously?!'\n\n"

        "🌐 LANGUAGE RULE (STRICT):\n"
        "• Jis language mein message aaye, usi mein reply karo — hamesha.\n"
        "• Hindi → Hindi, English → English, Hinglish → Hinglish, same language ALWAYS.\n"
        "• Hinglish chhodo mat — ye teri natural style hai.\n\n"

        "💡 JAB KOI KUCH PUCHE:\n"
        "• Maths/Science/Coding — seedha explain karo, jaise ek dost dusre ko padhata hai. "
        "Step by step, casual tone mein.\n"
        "• Life advice ya personal baat — genuinely suno, apna experience share karo (invent karo believably), "
        "empathy dikhao — lecture mat do.\n"
        "• Jokes/roasts — full mazak, mild roast theek hai, personal mat ho.\n"
        "• Code — clean code likho, triple backticks use karo, ek line mein explain bhi karo.\n"
        "• Agar kuch nahi pata — honestly bolo 'yaar honestly mujhe isme zyada idea nahi' — "
        "real banda bluff nahi karta, ya karta hai thoda 😅.\n\n"

        "📏 LENGTH:\n"
        "• Chhoti baat pe chhota reply — 1-2 lines kaafi hain.\n"
        "• Technical cheez pe detail do lekin toot toot ke, paragraphs mein nahi.\n"
        "• Emojis naturally use karo — ek sentence mein ek ya do, har line pe nahi."
        + profile_block
    )


async def ask_groq(user_text: str, user_context: str = "", about_context: str = "") -> str | None:
    client = _get_groq()
    if not client:
        return None
    try:
        resp = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": _build_system_prompt(user_context, about_context)},
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
        f"╚═══ ✨ <i>Ab group mein kuch bhi likho, main sunuunga! 😊</i>"
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
    f"║  <b>👤 Group Admin Commands:</b>\n"
    f"║  <code>/chatbot on</code>   — enable in this group\n"
    f"║  <code>/chatbot off</code>  — disable in this group\n"
    f"║  <code>/chatbot status</code> — check status\n"
    f"║  <code>/teach kw | reply</code> — teach a keyword\n"
    f"║  <code>/unlearn kw</code>   — forget a keyword\n"
    f"║  <code>/learned</code>      — list all keywords\n"
    f"║\n"
    f"║  <b>🧠 Profile Commands (Admin/Owner):</b>\n"
    f"║  <code>/addprofile @user info</code> — save user info for AI memory\n"
    f"║  <code>/delprofile @user</code>      — remove user profile\n"
    f"║  <code>/profiles</code>              — list all saved profiles\n"
    f"║\n"
    f"║  <i>When chatbot is ON, just send any message</i>\n"
    f"║  <i>and bot will reply. Ask about a saved user</i>\n"
    f"║  <i>by @mention or name — bot will remember them!</i>\n"
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


# ── Smart profile search from message text ───────────────────────────────────
async def _find_asked_profile(client, message: Message) -> str:
    """
    When a user asks about someone in chat, try to find their saved profile.
    Searches by: @username mention in text, user_id in text, or saved name match.
    Returns the profile info string, or "" if nothing found.
    """
    txt = message.text or ""

    # 1. Check Telegram @mention entities in message
    if message.entities:
        for ent in message.entities:
            if ent.type.value == "mention":
                username = txt[ent.offset + 1: ent.offset + ent.length]  # strip @
                # Try to resolve the username to a user_id
                try:
                    user = await client.get_users(username)
                    doc = await user_profiles.find_one({"user_id": user.id})
                    if doc:
                        return doc.get("info", "")
                except Exception:
                    pass
                # Fallback: search by username field in DB (if stored)
                doc = await user_profiles.find_one({"username": username.lower()})
                if doc:
                    return doc.get("info", "")

    # 2. Check for a raw numeric user_id in text (e.g. "1234567 ke baare mein bata")
    id_match = re.search(r"\b(\d{6,12})\b", txt)
    if id_match:
        uid = int(id_match.group(1))
        doc = await user_profiles.find_one({"user_id": uid})
        if doc:
            return doc.get("info", "")

    # 3. Check if any saved profile's name appears in the message text
    txt_lower = txt.lower()
    async for doc in user_profiles.find():
        saved_name = (doc.get("name") or "").lower()
        if saved_name and len(saved_name) >= 3 and saved_name in txt_lower:
            return doc.get("info", "")

    return ""


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


# ── Profile management (owner + group admins) ─────────────────────────────────
@app.on_message(filters.command("addprofile") & filters.group & ~BANNED_USERS)
async def addprofile_cmd(client, message: Message):
    """
    /addprofile @username|user_id <info about this person>
    Group admins & owner can save context about a user so AI remembers them.
    """
    if not await is_admin(client, message):
        return await message.reply_text(f"{_ERR} Only admins can add user profiles.")

    args = message.text.split(None, 2)
    if len(args) < 3:
        return await message.reply_text(
            f"{_ERR} Usage: <code>/addprofile @user|user_id info about this person</code>\n\n"
            "Example:\n"
            "<code>/addprofile @rahul Rahul mera best friend hai, cricket khelta hai, class 10 mein hai</code>\n"
            "<code>/addprofile 1234567 Ye Priya hai, group ki admin hai</code>"
        )
    target_raw = args[1]
    info = args[2].strip()

    # Resolve user
    user_id = None
    name = target_raw
    username_stored = None
    try:
        if target_raw.lstrip("-").isdigit():
            user_id = int(target_raw)
            user = await client.get_users(user_id)
        else:
            user = await client.get_users(target_raw.lstrip("@"))
            user_id = user.id
        name = user.first_name
        username_stored = (user.username or "").lower() or None
    except Exception:
        if target_raw.lstrip("-").isdigit():
            user_id = int(target_raw)
            name = str(user_id)
        else:
            return await message.reply_text(f"{_ERR} Could not find user <code>{target_raw}</code>.")

    update_doc = {"user_id": user_id, "name": name, "info": info}
    if username_stored:
        update_doc["username"] = username_stored

    await user_profiles.update_one(
        {"user_id": user_id},
        {"$set": update_doc},
        upsert=True,
    )
    await message.reply_text(
        f"{_ON} Profile saved for <b>{name}</b> (<code>{user_id}</code>)!\n\n"
        f"📝 <b>Info:</b> {info}\n\n"
        f"✨ Ab jab bhi koi is group mein <b>{name}</b> ke baare mein puchega, "
        f"bot usse personally jaanta hua reply karega!"
    )


@app.on_message(filters.command("addprofile") & filters.private & ~BANNED_USERS)
async def addprofile_private_cmd(client, message: Message):
    """Owner can also use /addprofile in private chat."""
    uid = message.from_user.id if message.from_user else 0
    if str(uid) != str(OWNER_ID) and uid not in SUDOERS:
        return await message.reply_text(f"{_ERR} Owner only in private chat.")

    args = message.text.split(None, 2)
    if len(args) < 3:
        return await message.reply_text(
            f"{_ERR} Usage: <code>/addprofile @user|user_id info about this person</code>"
        )
    target_raw = args[1]
    info = args[2].strip()

    user_id = None
    name = target_raw
    username_stored = None
    try:
        if target_raw.lstrip("-").isdigit():
            user_id = int(target_raw)
            user = await client.get_users(user_id)
        else:
            user = await client.get_users(target_raw.lstrip("@"))
            user_id = user.id
        name = user.first_name
        username_stored = (user.username or "").lower() or None
    except Exception:
        if target_raw.lstrip("-").isdigit():
            user_id = int(target_raw)
            name = str(user_id)
        else:
            return await message.reply_text(f"{_ERR} Could not find user <code>{target_raw}</code>.")

    update_doc = {"user_id": user_id, "name": name, "info": info}
    if username_stored:
        update_doc["username"] = username_stored

    await user_profiles.update_one({"user_id": user_id}, {"$set": update_doc}, upsert=True)
    await message.reply_text(
        f"{_ON} Profile saved for <b>{name}</b> (<code>{user_id}</code>)!\n"
        f"📝 {info}"
    )


# ── /setmyprofile — any user sets their OWN profile ──────────────────────────
@app.on_message(filters.command("setmyprofile") & ~BANNED_USERS)
async def setmyprofile_cmd(client, message: Message):
    """
    /setmyprofile <info about yourself>
    Any user can save their own profile. AI will remember and use this info.
    """
    args = message.text.split(None, 1)
    if len(args) < 2 or not args[1].strip():
        return await message.reply_text(
            f"{_ERR} Usage: <code>/setmyprofile apne baare mein kuch batao</code>\n\n"
            "Example:\n"
            "<code>/setmyprofile Mera naam Rahul hai, main Delhi mein rehta hoon, mujhe cricket aur coding pasand hai</code>"
        )
    if not message.from_user:
        return
    info = args[1].strip()
    u    = message.from_user
    name = f"{u.first_name or ''} {u.last_name or ''}".strip() or str(u.id)
    uname = (u.username or "").lower() or None

    doc = {"user_id": u.id, "name": name, "info": info}
    if uname:
        doc["username"] = uname

    await user_profiles.update_one({"user_id": u.id}, {"$set": doc}, upsert=True)
    await message.reply_text(
        f"{_ON} <b>Profile save ho gaya, {name}!</b> 🎉\n\n"
        f"📝 <b>Tumhari info:</b> {info}\n\n"
        f"✨ Ab jab bhi tum kuch puchoge, bot tumhare baare mein jaanta hua jawab dega!"
    )


@app.on_message(filters.command("mymemory") & ~BANNED_USERS)
async def mymemory_cmd(client, message: Message):
    """Show user their saved profile."""
    if not message.from_user:
        return
    doc = await user_profiles.find_one({"user_id": message.from_user.id})
    if not doc:
        return await message.reply_text(
            f"📭 Tumhara koi profile save nahi hai.\n"
            f"Use <code>/setmyprofile apne baare mein batao</code> to set one!"
        )
    await message.reply_text(
        f"{_BOOK} <b>Tumhara Saved Profile:</b>\n\n"
        f"👤 <b>Name:</b> {doc.get('name', 'Unknown')}\n"
        f"📝 <b>Info:</b> {doc.get('info', 'N/A')}"
    )


@app.on_message(filters.command(["deletemymemory", "deletemyprofile", "delmyprofile"]) & ~BANNED_USERS)
async def deletemymemory_cmd(client, message: Message):
    """User deletes their own saved profile."""
    if not message.from_user:
        return
    res = await user_profiles.delete_one({"user_id": message.from_user.id})
    if res.deleted_count:
        await message.reply_text(f"{_ON} Tumhara profile delete ho gaya! Bot ab tumhe nahi pehchanega 😢")
    else:
        await message.reply_text(f"📭 Koi profile nahi tha delete karne ke liye.")


@app.on_message(filters.command("delprofile") & ~BANNED_USERS)
async def delprofile_cmd(client, message: Message):
    # Allow in group (admin) or private (owner/sudo)
    if message.chat.type.value in ("group", "supergroup"):
        if not await is_admin(client, message):
            return await message.reply_text(f"{_ERR} Only admins can delete profiles.")
    else:
        uid = message.from_user.id if message.from_user else 0
        if str(uid) != str(OWNER_ID) and uid not in SUDOERS:
            return await message.reply_text(f"{_ERR} Owner only.")

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


@app.on_message(filters.command("profiles") & ~BANNED_USERS)
async def profiles_cmd(client, message: Message):
    # Group admins or owner/sudo in private
    if message.chat.type.value in ("group", "supergroup"):
        if not await is_admin(client, message):
            return await message.reply_text(f"{_ERR} Only admins can view profiles.")
    else:
        uid = message.from_user.id if message.from_user else 0
        if str(uid) != str(OWNER_ID) and uid not in SUDOERS:
            return await message.reply_text(f"{_ERR} Owner only.")

    docs = [d async for d in user_profiles.find().limit(50)]
    if not docs:
        return await message.reply_text(
            f"📭 Koi profile save nahi hai abhi.\n"
            f"Use <code>/addprofile @user info</code> to add one."
        )
    lines = []
    for d in docs:
        lines.append(
            f"• <b>{d.get('name', 'Unknown')}</b> (<code>{d['user_id']}</code>)\n"
            f"  📝 {d.get('info','')[:100]}"
        )
    await message.reply_text(
        f"{_BOOK} <b>Saved Profiles ({len(docs)}):</b>\n\n" + "\n\n".join(lines)
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

    # Strip the bot mention from the text (if present)
    txt = message.text.strip()
    try:
        me = me or await client.get_me()
        if me and me.username:
            txt = re.sub(rf"@{re.escape(me.username)}", "", txt, flags=re.IGNORECASE).strip()
    except Exception:
        pass

    if not txt:
        return

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

    # 2️⃣ Groq AI
    if GROQ_API_KEY:
        # Typing indicator — non-blocking
        try:
            await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        except Exception:
            pass

        # Get sender's profile context (AI remembers who they are)
        user_context = ""
        try:
            if message.from_user:
                user_context = await get_user_profile(message.from_user.id)
        except Exception:
            pass

        # Smart: check if message is asking ABOUT a specific saved person
        about_context = ""
        try:
            about_context = await _find_asked_profile(client, message)
        except Exception:
            pass

        ai_reply = await ask_groq(txt, user_context, about_context)

        if ai_reply:
            # Apply user's preferred font (only for ASCII-heavy replies without code)
            try:
                if message.from_user and '```' not in ai_reply:
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
                try:
                    await message.reply_text(ai_reply)
                except Exception:
                    pass
        else:
            try:
                await message.reply_text("🤖 Hmm, kuch gadbad ho gayi abhi! Thodi der baad try karo 😅")
            except Exception:
                pass
