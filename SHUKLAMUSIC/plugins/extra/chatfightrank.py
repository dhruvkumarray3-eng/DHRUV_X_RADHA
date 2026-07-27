"""
ChatFightRank — Daily / Weekly / Monthly message leaderboard with image card.
Commands: /chatfightrank  /cfr  /topchatters
Callback: cfr_<period>_<chat_id>
"""
import os
import io
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from SHUKLAMUSIC import app
from SHUKLAMUSIC.mongo.chatfightrankdb import increment_msg, get_top

FONT_PATH  = "SHUKLAMUSIC/assets/font.ttf"
FONT2_PATH = "SHUKLAMUSIC/assets/font2.ttf"

BOT_PFP_CACHE = "cache/bot_pfp.jpg"
os.makedirs("cache", exist_ok=True)

MEDALS = ["🥇", "🥈", "🥉", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]

PERIOD_LABELS = {
    "today": ("📅 TODAY", "🔵 Today"),
    "week":  ("📆 THIS WEEK", "🟣 This Week"),
    "month": ("🗓 THIS MONTH", "🟠 This Month"),
}

# ── Gradient helpers ──────────────────────────────────────────────────────────

def _make_gradient(w: int, h: int) -> Image.Image:
    """Dark purple → near-black vertical gradient."""
    img = Image.new("RGB", (w, h))
    top    = (72, 12, 110)   # deep violet
    bottom = (10,  5,  25)   # almost black
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        img.paste((r, g, b), [0, y, w, y + 1])
    return img


def _circle_crop(img: Image.Image, size: int) -> Image.Image:
    img = img.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, mask=mask)
    return out


def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


# ── Bot PFP download ──────────────────────────────────────────────────────────

async def _get_bot_pfp() -> Image.Image | None:
    if os.path.exists(BOT_PFP_CACHE):
        try:
            return Image.open(BOT_PFP_CACHE).convert("RGBA")
        except Exception:
            pass
    try:
        photos = [p async for p in app.get_chat_photos("me", limit=1)]
        if photos:
            path = await app.download_media(photos[0].file_id, file_name=BOT_PFP_CACHE)
            return Image.open(path).convert("RGBA")
    except Exception:
        pass
    return None


# ── Card generation ───────────────────────────────────────────────────────────

async def _make_card(
    chat_title: str,
    period: str,
    top: list,
) -> bytes:
    W, H = 800, 560
    bg = _make_gradient(W, H)
    draw = ImageDraw.Draw(bg)

    # Decorative accent line at top
    draw.rectangle([(0, 0), (W, 4)], fill=(180, 80, 255))

    # ── Bot PFP circle ────────────────────────────────────────────────────────
    pfp_size = 90
    pfp_x, pfp_y = W // 2 - pfp_size // 2, 14
    pfp_img = await _get_bot_pfp()
    if pfp_img:
        circ = _circle_crop(pfp_img, pfp_size)
        # Glow ring
        ring = Image.new("RGBA", (pfp_size + 8, pfp_size + 8), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse((0, 0, pfp_size + 7, pfp_size + 7), outline=(180, 80, 255), width=3)
        bg.paste(ring, (pfp_x - 4, pfp_y - 4), ring)
        bg.paste(circ, (pfp_x, pfp_y), circ)

    # ── Title ─────────────────────────────────────────────────────────────────
    title_y = pfp_y + pfp_size + 8
    f_brand = _load_font(FONT_PATH, 22)
    f_period = _load_font(FONT_PATH, 18)
    f_chat   = _load_font(FONT2_PATH, 15)
    f_name   = _load_font(FONT2_PATH, 17)
    f_count  = _load_font(FONT_PATH, 17)
    f_medal  = _load_font(FONT_PATH, 18)

    brand_txt = "🏆  NOBITA X PRIME — CHAT FIGHT RANK"
    bw = draw.textlength(brand_txt, font=f_brand)
    draw.text(((W - bw) / 2, title_y), brand_txt, font=f_brand, fill=(230, 180, 255))

    period_lbl, _ = PERIOD_LABELS.get(period, ("📅 TODAY", "🔵 Today"))
    pw = draw.textlength(period_lbl, font=f_period)
    draw.text(((W - pw) / 2, title_y + 28), period_lbl, font=f_period, fill=(255, 210, 100))

    # Chat name
    chat_display = chat_title[:40] + ("…" if len(chat_title) > 40 else "")
    cw = draw.textlength(chat_display, font=f_chat)
    draw.text(((W - cw) / 2, title_y + 52), chat_display, font=f_chat, fill=(160, 140, 200))

    # Separator
    sep_y = title_y + 80
    draw.rectangle([(40, sep_y), (W - 40, sep_y + 1)], fill=(120, 60, 180))

    # ── Leaderboard rows ──────────────────────────────────────────────────────
    if not top:
        msg = "No messages recorded yet!"
        mw = draw.textlength(msg, font=f_name)
        draw.text(((W - mw) / 2, sep_y + 60), msg, font=f_name, fill=(180, 160, 210))
    else:
        max_count = top[0][2] if top else 1
        row_h = 38
        row_y = sep_y + 10

        # Row colors alternate slightly
        row_colors = [(35, 15, 60), (28, 10, 50)]

        for i, (uid, name, count) in enumerate(top):
            ry = row_y + i * row_h
            # Row bg
            rc = row_colors[i % 2]
            draw.rectangle([(38, ry + 2), (W - 38, ry + row_h - 2)], fill=rc, outline=(90, 40, 140), width=1)

            # Medal / rank
            medal_txt = str(i + 1) + "."
            draw.text((48, ry + 9), medal_txt, font=f_medal, fill=(220, 180, 255))

            # Progress bar (behind name)
            bar_x, bar_y_pos = 80, ry + row_h - 8
            bar_w = int((count / max_count) * 340)
            bar_colors = [
                (255, 215,   0),   # gold
                (192, 192, 192),   # silver
                (205, 127,  50),   # bronze
                (100, 180, 255),
                (150, 255, 150),
                (255, 150, 255),
                (255, 200, 100),
                (100, 255, 220),
                (255, 130, 130),
                (200, 200, 255),
            ]
            bc = bar_colors[i] if i < len(bar_colors) else (150, 150, 200)
            draw.rectangle([(bar_x, bar_y_pos - 3), (bar_x + bar_w, bar_y_pos)], fill=bc + (120,) if len(bc) == 3 else bc)

            # Name
            disp_name = name[:26] + ("…" if len(name) > 26 else "")
            draw.text((82, ry + 8), disp_name, font=f_name, fill=(240, 230, 255))

            # Count (right-aligned)
            count_txt = f"{count:,} msgs"
            ctw = draw.textlength(count_txt, font=f_count)
            draw.text((W - 50 - ctw, ry + 9), count_txt, font=f_count, fill=(255, 210, 100))

    # ── Footer ────────────────────────────────────────────────────────────────
    draw.rectangle([(0, H - 4), (W, H)], fill=(180, 80, 255))
    footer_txt = "t.me/II_NOBITA_X_PRIME_II"
    fw = draw.textlength(footer_txt, font=f_chat)
    draw.text(((W - fw) / 2, H - 22), footer_txt, font=f_chat, fill=(160, 130, 200))

    buf = io.BytesIO()
    bg.convert("RGB").save(buf, format="JPEG", quality=92)
    buf.seek(0)
    return buf.read()


# ── Keyboard helper ───────────────────────────────────────────────────────────

def _keyboard(chat_id: int, active: str) -> InlineKeyboardMarkup:
    def btn(period: str):
        _, label = PERIOD_LABELS[period]
        # Put a ✅ tick on active button
        text = f"✅ {label}" if period == active else label
        return InlineKeyboardButton(text, callback_data=f"cfr_{period}_{chat_id}")
    return InlineKeyboardMarkup([[btn("today"), btn("week"), btn("month")]])


# ── Track every group message ─────────────────────────────────────────────────
@app.on_message(
    filters.group & ~filters.bot & ~filters.service,
    group=10,
)
async def _track_msg(client: Client, message: Message):
    if not message.from_user:
        return
    u = message.from_user
    name = f"{u.first_name or ''} {u.last_name or ''}".strip() or "Unknown"
    await increment_msg(message.chat.id, u.id, name)


# ── /cfr command ──────────────────────────────────────────────────────────────
@app.on_message(
    filters.command(["chatfightrank", "cfr", "topchatters"]) & filters.group
)
async def show_rank(client: Client, message: Message):
    wait = await message.reply_text("⏳ Generating leaderboard card...")
    period = "today"
    top = await get_top(message.chat.id, period=period)
    chat_title = message.chat.title or "This Group"

    try:
        img_bytes = await _make_card(chat_title, period, top)
        caption = (
            f"🏆 <b>Chat Fight Rank</b>\n"
            f"📅 <b>Today's top chatters in {chat_title}</b>\n\n"
            f"{'No messages yet! Start chatting! 😄' if not top else ''}"
        )
        await wait.delete()
        await message.reply_photo(
            photo=img_bytes,
            caption=caption,
            reply_markup=_keyboard(message.chat.id, period),
        )
    except Exception as e:
        await wait.edit_text(f"❌ Error generating card: {e}")


# ── Callback — Today / Week / Month buttons ───────────────────────────────────
@app.on_callback_query(filters.regex(r"^cfr_(today|week|month)_(-?\d+)$"))
async def cfr_callback(client: Client, callback: CallbackQuery):
    parts = callback.data.split("_")
    period   = parts[1]          # today | week | month
    chat_id  = int(parts[2])

    await callback.answer(f"Loading {PERIOD_LABELS[period][0]} …")

    try:
        chat = await client.get_chat(chat_id)
        chat_title = chat.title or "This Group"
    except Exception:
        chat_title = "This Group"

    top = await get_top(chat_id, period=period)
    img_bytes = await _make_card(chat_title, period, top)

    caption = (
        f"🏆 <b>Chat Fight Rank — {PERIOD_LABELS[period][0]}</b>\n"
        f"<b>{chat_title}</b>\n\n"
        f"{'No messages yet! Start chatting! 😄' if not top else ''}"
    )

    try:
        await callback.message.edit_media(
            media=__import__("pyrogram.types", fromlist=["InputMediaPhoto"]).InputMediaPhoto(
                media=img_bytes,
                caption=caption,
            ),
            reply_markup=_keyboard(chat_id, period),
        )
    except Exception:
        # Fallback: send new photo
        await callback.message.reply_photo(
            photo=img_bytes,
            caption=caption,
            reply_markup=_keyboard(chat_id, period),
        )


__help__ = """
📊 <b>ChatFightRank</b> — Kaun sabse zyada bolta hai? Ab pata chalega! 🔥

<b>Commands:</b>
/cfr — Aaj ka leaderboard card dikhao
/chatfightrank — Same
/topchatters — Same

Buttons pe tap karo:
🔵 <b>Today</b> — Aaj ke top chatters
🟣 <b>This Week</b> — Is hafte ke top chatters
🟠 <b>This Month</b> — Is mahine ke top chatters

Har message count hota hai. Bot ka PFP card pe lagega. 🎖️
"""

__mod_name__ = "ChatFightRank"
