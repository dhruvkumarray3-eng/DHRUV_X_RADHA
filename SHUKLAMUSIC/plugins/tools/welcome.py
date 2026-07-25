# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shukla (https://github.com/itzshukla)
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
from SHUKLAMUSIC import app
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops
import random
import asyncio
import os
import time
from logging import getLogger
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode, ChatMemberStatus
from SHUKLAMUSIC.utils.database import add_served_chat, get_assistant, is_active_chat
from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.mongo.afkdb import PROCESS
from SHUKLAMUSIC.utils.Shukla_ban import admin_filter
from SHUKLAMUSIC.utils.branding import BRAND_EMOJIS, WELCOME_BACKGROUND_URL

LOGGER = getLogger(__name__)

# ── Statusvideobytaraxd pack IDs ──
_TX_HEART  = 6298356878573307709   # ❤️
_TX_OK     = 6296501388276926215   # ✅
_TX_CROWN  = 6219549292458150316   # 👑
_TX_BOOM   = 6298644001432012664   # 💥
_TX_HUG    = 6298454498884978957   # 🫶
_TX_LOVE   = 6298335558355651118   # 😍
_TX_GEM    = 6244241334320762892   # 💎
_TX_ROSE   = 6102617459204822706   # 🌹

def tx(eid, fb):
    return f'<emoji id={eid}>{fb}</emoji>'

# ── Welcome background (catbox) ──
WEL_BG_URL  = WELCOME_BACKGROUND_URL
# A new cache name makes sure the requested Catbox artwork replaces any old
# imported welcome card that happened to be present in the workspace.
WEL_BG_PATH = "SHUKLAMUSIC/assets/welcome_catbox.png"

# ── Emojis palette ──
EMOJIS = BRAND_EMOJIS

# ── Default fallback photos ──
random_photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
    "https://i.ibb.co/rRXc8MGR/image.jpg",
]

# ─────────────────────────────────────────────────────────────────────────────

async def _ensure_wel_bg():
    """Ensure the exact Catbox welcome template is available locally."""
    import aiohttp
    if not os.path.exists(WEL_BG_PATH):
        os.makedirs(os.path.dirname(WEL_BG_PATH), exist_ok=True)
        try:
            async with aiohttp.ClientSession(
                headers={"User-Agent": "Mozilla/5.0"}
            ) as s:
                async with s.get(WEL_BG_URL, timeout=aiohttp.ClientTimeout(total=15)) as r:
                    if r.status == 200:
                        with open(WEL_BG_PATH, "wb") as f:
                            f.write(await r.read())
        except Exception as e:
            LOGGER.warning(f"Failed to download welcome bg: {e}")


class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        if chat_id not in self.data:
            self.data[chat_id] = {"state": "on"}

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

wlcm = WelDatabase()

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None


def circle(pfp, size=(500, 500), brightness_factor=1.0):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    pfp = ImageEnhance.Brightness(pfp).enhance(brightness_factor)
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


def welcomepic(pic, user, chatname, id, uname, brightness_factor=1.3):
    if not os.path.exists(WEL_BG_PATH):
        raise FileNotFoundError(
            f"Welcome template is missing: {WEL_BG_PATH}"
        )

    # Keep the Catbox template pixel-perfect.  It already contains the
    # welcome artwork, title and member-profile frame; only the PFP and ID
    # are dynamic overlays.
    background = Image.open(WEL_BG_PATH).convert("RGBA")
    width, height = background.size

    pfp = Image.open(pic).convert("RGBA")
    pfp_size = round(min(width * 0.125, height * 0.225))
    pfp = circle(pfp, size=(pfp_size, pfp_size), brightness_factor=brightness_factor)
    draw = ImageDraw.Draw(background)

    try:
        id_font = ImageFont.truetype(
            "SHUKLAMUSIC/assets/font.ttf",
            size=round(height * 0.052),
        )
    except Exception:
        id_font = ImageFont.load_default()

    # Cover only the template placeholder and write the member's real ID in
    # the same lower profile strip.  The rest of the source image is untouched.
    id_box = (
        round(width * 0.225),
        round(height * 0.755),
        round(width * 0.515),
        round(height * 0.855),
    )
    draw.rounded_rectangle(id_box, radius=8, fill=(42, 42, 42, 255))
    draw.text(
        (round(width * 0.245), round(height * 0.775)),
        f"ID {id}",
        fill=(225, 190, 100, 255),
        font=id_font,
    )

    # Paste the user's PFP inside the template's circular frame.
    pfp_position = (
        round(width * 0.066),
        round(height * 0.69),
    )
    background.paste(pfp, pfp_position, pfp)

    out_path = f"downloads/welcome#{id}.png"
    background.convert("RGB").save(out_path, optimize=True)
    return out_path


@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "**ᴜsᴀɢᴇ:**\n**⦿ /welcome [on|off]**"
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)
    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        A = await wlcm.find_one(chat_id)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "off":
            if A:
                await message.reply_text("**ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !**")
            else:
                await wlcm.add_wlcm(chat_id)
                await message.reply_text(f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ** {message.chat.title}")
        elif state == "on":
            if not A:
                await message.reply_text("**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ.**")
            else:
                await wlcm.rm_wlcm(chat_id)
                await message.reply_text(f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ** {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ!**")


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    count = await app.get_chat_members_count(chat_id)
    A = await wlcm.find_one(chat_id)
    if A:
        return

    if member.new_chat_member and not member.old_chat_member and member.new_chat_member.status != "kicked":
        user = member.new_chat_member.user

        # Ensure welcome background is downloaded
        await _ensure_wel_bg()

        try:
            pic = await app.download_media(user.photo.big_file_id, file_name=f"pp{user.id}.png")
        except AttributeError:
            pic = "SHUKLAMUSIC/assets/upic.png"

        if temp.MELCOW.get(f"welcome-{chat_id}") is not None:
            try:
                await temp.MELCOW[f"welcome-{chat_id}"].delete()
            except Exception as e:
                LOGGER.error(e)

        # Keep the welcome copy free from star/spark symbols.
        welcome_emojis = [
            emoji for emoji in EMOJIS
            if emoji not in {"✨", "☄️"}
        ]
        e1, e2, e3, e4 = random.choices(welcome_emojis, k=4)

        try:
            welcomeimg = welcomepic(pic, user.first_name, member.chat.title, user.id, user.username)

            deep_link = f"tg://openmessage?user_id={user.id}"
            add_link  = f"https://t.me/{app.username}?startgroup=true"

            caption = (
                f"{tx(_TX_BOOM,'💥')} <b>ᴡᴇʟᴄᴏᴍᴇ</b> {tx(_TX_BOOM,'💥')}\n\n"
                f"❤️‍🔥 <b>▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬</b> ❤️‍🔥\n\n"
                f"{tx(_TX_CROWN,'👑')} <b>ɴᴀᴍᴇ :</b> {user.mention}\n"
                f"{tx(_TX_OK,'✅')} <b>ɪᴅ :</b> <code>{user.id}</code>\n"
                f"{tx(_TX_ROSE,'🌹')} <b>ᴜ_ɴᴀᴍᴇ :</b> @{user.username if user.username else 'None'}\n"
                f"{tx(_TX_OK,'✅')} <b>ᴍᴇᴍʙᴇʀs :</b> {count}\n\n"
                f"🤗😇 <b>▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬</b> 😇🤗\n\n"
                f"🌚 <i>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ! ᴍᴀᴋᴇ ʏᴏᴜʀsᴇʟғ ᴀᴛ ʜᴏᴍᴇ ᴀɴᴅ ʜᴀᴠᴇ ᴀ ɢʀᴇᴀᴛ ᴛɪᴍᴇ!</i> {e1}\n\n"
                f"{tx(_TX_HEART,'❤️')} {tx(_TX_GEM,'💎')} 👀 🌹 👻"
            )

            msg = await app.send_photo(
                chat_id,
                photo=welcomeimg,
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "๏ ᴠɪᴇᴡ ɴᴇᴡ ᴍᴇᴍʙᴇʀ ๏",
                            url=deep_link,
                            style=ButtonStyle.PRIMARY,
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "✙ ᴋɪᴅɴᴀᴘ ᴍᴇ ✙",
                            url=add_link,
                            style=ButtonStyle.DANGER,
                        )
                    ],
                ])
            )

            temp.MELCOW[f"welcome-{chat_id}"] = msg

            # Auto-delete in 5 minutes
            await asyncio.sleep(300)
            try:
                await msg.delete()
            except Exception:
                pass

        except Exception as e:
            LOGGER.error(e)
