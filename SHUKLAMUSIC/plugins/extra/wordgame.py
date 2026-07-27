"""
Word Chain Game (Antakshari style) — Akshar se nayi words banana.
Last letter of each word becomes the first letter of the next.
Commands: /startword  /stopword  /wordscore
"""
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.mongo.wordgamedb import start_game, get_game, stop_game, submit_word

# Starter words to kick off a game
STARTER_WORDS = [
    "apple", "orange", "elephant", "tiger", "rabbit",
    "mango", "ocean", "number", "rainbow", "kingdom",
    "night", "travel", "music", "diamond", "nature",
]

MEDALS = ["🥇", "🥈", "🥉"]


# ── /startword ────────────────────────────────────────────────────────────────
@app.on_message(filters.command("startword") & filters.group)
async def cmd_start_word(client: Client, message: Message):
    existing = await get_game(message.chat.id)
    if existing:
        cw = existing["current_word"]
        await message.reply_text(
            f"⚠️ Game pehle se chal raha hai!\n"
            f"Abhi ka word: <b>{cw}</b>\n"
            f"Agle word ka pehla letter: <b>{cw[-1].upper()}</b>\n\n"
            f"Game band karne ke liye /stopword use karo."
        )
        return

    import random
    starter = random.choice(STARTER_WORDS)
    await start_game(message.chat.id, starter)
    await message.reply_text(
        f"🎮 <b>Word Chain Game Shuru!</b>\n\n"
        f"Rules:\n"
        f"• Pichle word ke <b>aakhiri letter</b> se naaya word shuru karo\n"
        f"• Ek word ek baar hi use ho sakta hai\n"
        f"• Sirf English words valid hain\n\n"
        f"Pehla word: <b>{starter}</b>\n"
        f"Agle word ka pehla letter: <b>{starter[-1].upper()}</b>\n\n"
        f"Shuru karo! 🚀"
    )


# ── /stopword ─────────────────────────────────────────────────────────────────
@app.on_message(filters.command("stopword") & filters.group)
async def cmd_stop_word(client: Client, message: Message):
    scores = await stop_game(message.chat.id)
    if not scores:
        await message.reply_text("❌ Is group mein koi game chal nahi raha.")
        return

    sorted_scores = sorted(
        scores.items(), key=lambda x: x[1].get("score", 0), reverse=True
    )

    lines = ["🏁 <b>Word Chain Game Khatam!</b>\n\n🏆 <b>Final Scores:</b>\n"]
    for i, (uid, data) in enumerate(sorted_scores[:10]):
        medal = MEDALS[i] if i < len(MEDALS) else f"{i+1}."
        lines.append(f"{medal} <b>{data.get('name', 'Unknown')}</b> — {data.get('score', 0)} words")

    if not sorted_scores:
        lines.append("Kisi ne khelhi nahi! 😅")

    await message.reply_text("\n".join(lines))


# ── /wordscore ────────────────────────────────────────────────────────────────
@app.on_message(filters.command("wordscore") & filters.group)
async def cmd_word_score(client: Client, message: Message):
    game = await get_game(message.chat.id)
    if not game:
        await message.reply_text("❌ Abhi koi game nahi chal raha. /startword se shuru karo!")
        return

    scores = game.get("scores", {})
    cw = game.get("current_word", "")
    used = len(game.get("used_words", []))

    lines = [
        f"📊 <b>Word Chain — Live Scores</b>\n",
        f"🔤 Current word: <b>{cw}</b>",
        f"➡️ Next starts with: <b>{cw[-1].upper() if cw else '?'}</b>",
        f"📝 Words used: <b>{used}</b>\n",
    ]

    if scores:
        sorted_scores = sorted(scores.items(), key=lambda x: x[1].get("score", 0), reverse=True)
        lines.append("🏆 <b>Scores:</b>")
        for i, (uid, data) in enumerate(sorted_scores[:10]):
            medal = MEDALS[i] if i < len(MEDALS) else f"{i+1}."
            lines.append(f"{medal} <b>{data.get('name', 'Unknown')}</b> — {data.get('score', 0)} words")
    else:
        lines.append("Abhi tak kisi ne word nahi diya!")

    await message.reply_text("\n".join(lines))


# ── Message listener — validate submitted words ───────────────────────────────
@app.on_message(filters.group & filters.text & ~filters.command([""]), group=11)
async def _check_word(client: Client, message: Message):
    if not message.from_user:
        return

    text = message.text.strip()
    # Only process single-word messages (ignore multi-word messages / commands)
    if " " in text or not text.isalpha():
        return

    game = await get_game(message.chat.id)
    if not game:
        return

    user = message.from_user
    name = (user.first_name or "") + (" " + user.last_name if user.last_name else "")
    name = name.strip() or "Unknown"

    ok, reason = await submit_word(message.chat.id, user.id, name, text)

    if ok:
        new_word = text.lower()
        await message.reply_text(
            f"✅ <b>{name}</b> ne diya: <b>{new_word}</b>\n"
            f"➡️ Agle word ka pehla letter: <b>{new_word[-1].upper()}</b>"
        )
    elif reason == "used":
        await message.reply_text(
            f"❌ <b>{text.lower()}</b> pehle se use ho chuka hai! Doosra word do."
        )
    elif reason == "wrong_letter":
        cw = game.get("current_word", "")
        await message.reply_text(
            f"❌ Word <b>'{cw[-1].upper()}'</b> se shuru hona chahiye! "
            f"(Pichla word: <b>{cw}</b>)"
        )


__help__ = """
🎮 <b>Word Chain Game</b> — Antakshari style English word game!

Pichle word ke aakhiri letter se naya word shuru karo.

<b>Commands:</b>
/startword — Nayi game shuru karo
/stopword  — Game band karo aur winner batao
/wordscore — Live scores dekho

<b>Rules:</b>
• Pichle word ka aakhiri letter = agle word ka pehla letter
• Ek word sirf ek baar use ho sakta hai
• Sirf English alphabet words valid hain
• Har valid word = 1 point
"""

__mod_name__ = "WordGame"
