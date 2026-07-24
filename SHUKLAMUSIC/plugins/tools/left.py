# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
from SHUKLAMUSIC import app
from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
import asyncio
import random

# ── Emoji palette (same as welcome) ──
EMOJIS = ["🫠", "❤️‍🩹", "❤️‍🔥", "🌚", "👀", "✨", "👻", "😇", "🌹", "🤗", "✨", "☄️"]

# ─────────────────────────────────────────────────────────────────────────────

get_font   = lambda sz, fp: ImageFont.truetype(fp, sz)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

# ─────────────────────────────────────────────────────────────────────────────

async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path).convert("RGBA")
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)
        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)
    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path

# ─────────────────────────────────────────────────────────────────────────────

bg_path   = "SHUKLAMUSIC/assets/userinfo.png"
font_path = "SHUKLAMUSIC/assets/hiroko.ttf"

# ─────────────────────────────────────────────────────────────────────────────

@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {"banned", "left", "restricted"}
        and member.old_chat_member
    ):
        pass
    else:
        return

    user = (
        member.old_chat_member.user
        if member.old_chat_member
        else member.from_user
    )

    # Pick random emojis
    e1, e2, e3 = random.choices(EMOJIS, k=3)

    if user.photo and user.photo.big_file_id:
        try:
            photo = await app.download_media(user.photo.big_file_id)

            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )

            caption = (
                f"❅─────✧❅✦❅✧─────❅\n\n"
                f"🌚 {e1} <b>ᴀ ᴍᴇᴍʙᴇʀ ʟᴇғᴛ ᴛʜᴇ ɢʀᴏᴜᴘ</b> 🥀\n\n"
                f"☄️ <b>➻</b> {member.old_chat_member.user.mention}\n\n"
                f"❤️‍🩹 <b>▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬</b> ❤️‍🔥\n\n"
                f"👀 ✨ <b>ᴏᴋ ʙʏᴇ ᴅᴇᴀʀ ᴀɴᴅ ʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ ᴀɢᴀɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅs</b> ✨ 👀\n\n"
                f"👻 {e2} <b>▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬</b> {e3} 😇\n\n"
                f"🌹 <b>ㅤ•─╼⃝𖠁 ʙʏᴇ ♡︎ ʙᴀʙʏ 𖠁⃝╾─•</b> 🌹"
            )

            deep_link = f"tg://openmessage?user_id={user.id}"

            message = await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "๏ ᴠɪᴇᴡ ᴜsᴇʀ ๏",
                            url=deep_link,
                            style=ButtonStyle.DANGER,
                        )
                    ]
                ])
            )

            # Auto-delete after 30 seconds
            async def delete_message():
                await asyncio.sleep(30)
                try:
                    await message.delete()
                except Exception:
                    pass

            asyncio.create_task(delete_message())

        except RPCError as e:
            print(e)
            return
    else:
        # No profile photo — send text-only message
        e1, e2 = random.choices(EMOJIS, k=2)
        try:
            deep_link = f"tg://openmessage?user_id={user.id}"
            msg = await client.send_message(
                chat_id=member.chat.id,
                text=(
                    f"🌚 {e1} <b>ᴀ ᴍᴇᴍʙᴇʀ ʟᴇғᴛ ᴛʜᴇ ɢʀᴏᴜᴘ</b> 🥀\n\n"
                    f"☄️ <b>➻</b> {user.mention}\n\n"
                    f"👻 ✨ <b>ᴏᴋ ʙʏᴇ ᴅᴇᴀʀ, ʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ ᴀɢᴀɪɴ!</b> ✨ 😇\n\n"
                    f"🌹 <b>ʙʏᴇ ♡ ʙᴀʙʏ</b> 🌹 {e2}"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("๏ ᴠɪᴇᴡ ᴜsᴇʀ ๏", url=deep_link, style=ButtonStyle.DANGER)]
                ])
            )
            asyncio.create_task(_auto_delete(msg, 30))
        except Exception:
            pass


async def _auto_delete(msg, delay: int):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except Exception:
        pass
