"""
ChatFightRank — Daily / Weekly / Monthly message leaderboard with image card.
Commands: /chatfightrank  /cfr  /topchatters
Callback: cfr_<period>_<chat_id>
"""
import os
import io
import asyncio
import aiohttp
from PIL import Image, ImageDraw, ImageFont

from pyrogram import Client, filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, InputMediaPhoto,
)

from SHUKLAMUSIC import app
from SHUKLAMUSIC.mongo.chatfightrankdb import increment_msg, get_top

FONT_PATH  = "SHUKLAMUSIC/assets/font.ttf"
FONT2_PATH = "SHUKLAMUSIC/assets/font2.ttf"

BANNER_URL   = "https://files.catbox.moe/ow4kf1.png"
BANNER_CACHE = "cache/cfr_banner.png"
BOT_PFP_CACHE = "cache/bot_pfp_cfr.jpg"
os.makedirs("cache", exist_ok=True)

PERIOD_LABELS = {
    "today": "📅  TODAY",
    "week":  "📆  THIS WEEK",
    "month": "🗓  THIS MONTH",
}
BTN_LABELS = {
    "today": "🟢 Today",
    "week":  "🔵 Week",
    "month": "🔴 Monthly",
}

BAR_PALETTE = [
    (255, 215,   0),   # gold
    (192, 192, 192),   # silver
    (205, 127,  50),   # bronze
    (100, 180, 255),
    (160, 255, 160),
    (255, 140, 255),
    (255, 200,  80),
    ( 80, 255, 220),
    (255, 120, 120),
    (180, 180, 255),
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _circle_crop(img: Image.Image, size: int) -> Image.Image:
    img = img.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, mask=mask)
    return out


async def _get_banner() -> Image.Image | None:
    """Download & cache the top banner image."""
    if os.path.exists(BANNER_CACHE):
        try:
            return Image.open(BANNER_CACHE).convert("RGBA")
        except Exception:
            pass
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(BANNER_URL, timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 200:
                    data = await r.read()
                    with open(BANNER_CACHE, "wb") as f:
                        f.write(data)
                    return Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception:
        pass
    return None


async def _get_bot_pfp() -> Image.Image | None:
    """Download & cache bot profile photo."""
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


# ── Card generator ────────────────────────────────────────────────────────────

async def _make_card(chat_title: str, period: str, top: list) -> io.BytesIO:
    W = 800

    # ── 1. Top banner ──────────────────────────────────────────────────────
    banner = await _get_banner()
    if banner:
        bw, bh = banner.size
        banner_h = int(bh * W / bw)       # keep aspect ratio
        banner_h = min(banner_h, 260)      # cap at 260px
        banner = banner.resize((W, banner_h), Image.LANCZOS)
    else:
        # fallback purple gradient banner
        banner_h = 200
        banner = Image.new("RGB", (W, banner_h))
        for y in range(banner_h):
            t = y / banner_h
            r = int(72 + (10 - 72) * t)
            g = int(12 + (5 - 12) * t)
            b = int(110 + (25 - 110) * t)
            banner.paste((r, g, b), [0, y, W, y + 1])
        banner = banner.convert("RGBA")

    # ── 2. Rankings section height ─────────────────────────────────────────
    row_h   = 44
    rows    = max(len(top), 1)
    header_h = 70     # period label + group name
    footer_h = 28
    rank_h  = header_h + rows * row_h + footer_h + 10
    H = banner_h + rank_h

    # ── 3. Compose canvas ──────────────────────────────────────────────────
    canvas = Image.new("RGBA", (W, H), (12, 5, 28, 255))
    canvas.paste(banner, (0, 0), banner)

    # Dark overlay on lower half for readability
    overlay = Image.new("RGBA", (W, rank_h), (8, 3, 20, 220))
    canvas.paste(overlay, (0, banner_h), overlay)

    draw = ImageDraw.Draw(canvas)

    # Top accent line
    draw.rectangle([(0, 0), (W, 4)], fill=(180, 80, 255))

    # ── 4. Bot PFP circle straddling banner / rank boundary ───────────────
    pfp_size = 80
    pfp_x = W // 2 - pfp_size // 2
    pfp_y = banner_h - pfp_size // 2

    pfp_img = await _get_bot_pfp()
    if pfp_img:
        circ = _circle_crop(pfp_img, pfp_size)
        # Glow ring
        ring_size = pfp_size + 8
        ring = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse((0, 0, ring_size - 1, ring_size - 1),
                                     outline=(200, 100, 255), width=3)
        canvas.paste(ring, (pfp_x - 4, pfp_y - 4), ring)
        canvas.paste(circ, (pfp_x, pfp_y), circ)

    # ── 5. Period label + group name ───────────────────────────────────────
    f_period  = _load_font(FONT_PATH,  19)
    f_chat    = _load_font(FONT2_PATH, 14)
    f_rank    = _load_font(FONT_PATH,  15)
    f_name    = _load_font(FONT2_PATH, 16)
    f_count   = _load_font(FONT_PATH,  15)
    f_footer  = _load_font(FONT2_PATH, 13)

    label_y = banner_h + pfp_size // 2 + 6
    period_txt = PERIOD_LABELS.get(period, "📅 TODAY")
    pw = draw.textlength(period_txt, font=f_period)
    draw.text(((W - pw) / 2, label_y), period_txt, font=f_period, fill=(255, 210, 80))

    chat_disp = (chat_title[:42] + "…") if len(chat_title) > 42 else chat_title
    cw = draw.textlength(chat_disp, font=f_chat)
    draw.text(((W - cw) / 2, label_y + 26), chat_disp, font=f_chat, fill=(170, 145, 210))

    # Separator
    sep_y = label_y + 50
    draw.rectangle([(40, sep_y), (W - 40, sep_y + 1)], fill=(100, 50, 170))

    # ── 6. Leaderboard rows ────────────────────────────────────────────────
    row_start = sep_y + 6
    row_bg    = [(32, 12, 55), (24, 8, 44)]

    if not top:
        msg = "Koi messages nahi aaye abhi! Start chatting 😄"
        mw = draw.textlength(msg, font=f_name)
        draw.text(((W - mw) / 2, row_start + 14), msg, font=f_name, fill=(180, 160, 210))
    else:
        max_count = max(top[0][2], 1)
        for i, (uid, name, count) in enumerate(top):
            ry = row_start + i * row_h
            # Row background
            draw.rectangle([(36, ry + 2), (W - 36, ry + row_h - 2)],
                           fill=row_bg[i % 2], outline=(80, 35, 130), width=1)

            # Rank number
            rank_txt = f"{i + 1}."
            draw.text((46, ry + 13), rank_txt, font=f_rank, fill=(210, 170, 255))

            # Color bar (thin, at bottom of row)
            bar_x  = 72
            bar_end = W - 160
            bar_len = int((count / max_count) * (bar_end - bar_x))
            bc = BAR_PALETTE[i] if i < len(BAR_PALETTE) else (150, 150, 200)
            draw.rectangle([(bar_x, ry + row_h - 6), (bar_x + bar_len, ry + row_h - 3)], fill=bc)

            # Name
            disp_name = (name[:28] + "…") if len(name) > 28 else name
            draw.text((72, ry + 10), disp_name, font=f_name, fill=(240, 228, 255))

            # Count (right side)
            count_txt = f"{count:,} msgs"
            ctw = draw.textlength(count_txt, font=f_count)
            draw.text((W - 44 - ctw, ry + 13), count_txt, font=f_count, fill=bc)

    # ── 7. Footer ──────────────────────────────────────────────────────────
    draw.rectangle([(0, H - 4), (W, H)], fill=(180, 80, 255))
    footer_txt = "🎵  t.me/II_NOBITA_X_PRIME_II"
    fw = draw.textlength(footer_txt, font=f_footer)
    draw.text(((W - fw) / 2, H - 22), footer_txt, font=f_footer, fill=(150, 120, 200))

    buf = io.BytesIO()
    canvas.convert("RGB").save(buf, format="JPEG", quality=92)
    buf.seek(0)
    return buf


# ── Keyboard ──────────────────────────────────────────────────────────────────

_BTN_STYLES = {
    "today": ButtonStyle.SUCCESS,   # green
    "week":  ButtonStyle.PRIMARY,   # blue
    "month": ButtonStyle.DANGER,    # red
}

def _keyboard(chat_id: int, active: str) -> InlineKeyboardMarkup:
    def btn(p: str):
        label = BTN_LABELS[p]
        text  = f"✅ {label}" if p == active else label
        return InlineKeyboardButton(
            text,
            callback_data=f"cfr_{p}_{chat_id}",
            style=_BTN_STYLES[p],
        )
    return InlineKeyboardMarkup([[btn("today"), btn("week"), btn("month")]])


# ── Track every group message ─────────────────────────────────────────────────

@app.on_message(filters.group & ~filters.bot & ~filters.service, group=10)
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
    period     = "today"
    top        = await get_top(message.chat.id, period=period)
    chat_title = message.chat.title or "This Group"

    try:
        buf = await _make_card(chat_title, period, top)
        caption = (
            f"🏆 <b>Chat Fight Rank — Today</b>\n"
            f"📍 <b>{chat_title}</b>"
        )
        await wait.delete()
        await message.reply_photo(
            photo=buf,
            caption=caption,
            reply_markup=_keyboard(message.chat.id, period),
        )
    except Exception as e:
        await wait.edit_text(f"❌ Card error: {e}")


# ── Callback — Today / Week / Monthly ─────────────────────────────────────────

@app.on_callback_query(filters.regex(r"^cfr_(today|week|month)_(-?\d+)$"))
async def cfr_callback(client: Client, callback: CallbackQuery):
    parts = callback.data.split("_", 2)
    period = parts[1]
    cid_str = parts[2]
    chat_id = int(cid_str)

    # Detect already-active period to avoid redundant regeneration (prevents glitch)
    current_markup = callback.message.reply_markup
    active_label = BTN_LABELS.get(period, "")
    expected_active = f"✅ {active_label}"
    if current_markup:
        for row in current_markup.inline_keyboard:
            for btn in row:
                if btn.text == expected_active:
                    await callback.answer(f"Already showing {PERIOD_LABELS.get(period, period)}")
                    return

    await callback.answer(f"Loading {PERIOD_LABELS.get(period, period)} …")

    try:
        chat = await client.get_chat(chat_id)
        chat_title = chat.title or "This Group"
    except Exception:
        chat_title = "This Group"

    top = await get_top(chat_id, period=period)
    buf = await _make_card(chat_title, period, top)

    caption = (
        f"🏆 <b>Chat Fight Rank — {PERIOD_LABELS.get(period, period)}</b>\n"
        f"📍 <b>{chat_title}</b>"
    )

    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=buf, caption=caption),
            reply_markup=_keyboard(chat_id, period),
        )
    except Exception:
        try:
            await callback.message.edit_caption(
                caption=caption,
                reply_markup=_keyboard(chat_id, period),
            )
        except Exception:
            pass


__help__ = """
📊 <b>ChatFightRank</b> — Kaun sabse zyada bolta hai? Ab pata chalega! 🔥

<b>Commands:</b>
/cfr — Leaderboard card dikhao
/chatfightrank — Same
/topchatters — Same

Buttons pe tap karo:
🔵 <b>Today</b> — Aaj ke top chatters
🟣 <b>Week</b> — Is hafte ke top chatters
🟠 <b>Monthly</b> — Is mahine ke top chatters

Har message count hota hai. Roz midnight reset.
"""

__mod_name__ = "ChatFightRank"
