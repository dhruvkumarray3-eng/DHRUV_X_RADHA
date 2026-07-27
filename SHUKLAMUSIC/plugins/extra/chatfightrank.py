"""
ChatFightRank — Daily message leaderboard for groups.
Commands: /chatfightrank  /cfr  /topchatters
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.mongo.chatfightrankdb import increment_msg, get_top

MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


# ── Track every group message ─────────────────────────────────────────────────
@app.on_message(
    filters.group & ~filters.bot & ~filters.service,
    group=10,
)
async def _track_msg(client: Client, message: Message):
    if not message.from_user:
        return
    user = message.from_user
    name = (user.first_name or "") + (" " + user.last_name if user.last_name else "")
    name = name.strip() or "Unknown"
    await increment_msg(message.chat.id, user.id, name)


# ── Show leaderboard ──────────────────────────────────────────────────────────
@app.on_message(filters.command(["chatfightrank", "cfr", "topchatters"]) & filters.group)
async def show_rank(client: Client, message: Message):
    top = await get_top(message.chat.id, limit=10)
    if not top:
        await message.reply_text(
            "📊 Aaj abhi tak koi message nahi aaya is group mein!\n"
            "Baat karo, rank banegi 😄"
        )
        return

    lines = ["🏆 <b>ChatFight Rank — Aaj ke Top Chatters</b> 🏆\n"]
    for i, (uid, name, count) in enumerate(top):
        medal = MEDALS[i] if i < len(MEDALS) else f"{i+1}."
        lines.append(f"{medal} <b>{name}</b> — <code>{count}</code> msgs")

    lines.append("\n💬 <i>Jyada bolo, rank bado!</i>")
    await message.reply_text("\n".join(lines))


__help__ = """
📊 <b>ChatFightRank</b> — Dekhte hain aaj kaun sabse zyada bola!

<b>Commands:</b>
/chatfightrank — Aaj ke top 10 chatters dikhao
/cfr — Same (shortcut)
/topchatters — Same (shortcut)

Har message automatically count hota hai. Rank roz reset hoti hai.
"""

__mod_name__ = "ChatFightRank"
