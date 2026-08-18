# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
import os
import re
from asyncio import gather
from traceback import format_exc

from PIL import Image, UnidentifiedImageError
from pyrogram import filters
from pyrogram.errors import (
    PackShortNameInvalid,
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from SHUKLAMUSIC import app
from config import BOT_USERNAME
from SHUKLAMUSIC.utils.errors import capture_err

from SHUKLAMUSIC.utils.files import (
    get_document_from_file_id,
    resize_file_to_sticker_size,
    upload_document,
)

from SHUKLAMUSIC.utils.stickerset import (
    add_sticker_to_set,
    create_sticker,
    create_sticker_set,
    get_sticker_set_by_name,
)

# -----------

MAX_STICKERS = (
    120  # would be better if we could fetch this limit directly from telegram
)
SUPPORTED_TYPES = ["jpeg", "png", "webp"]


def _detect_image_type(file_path: str) -> str | None:
    """Return a Telegram-supported image type on Python versions without imghdr."""
    try:
        with Image.open(file_path) as image:
            image_type = (image.format or "").lower()
    except (OSError, UnidentifiedImageError):
        return None
    return image_type if image_type in SUPPORTED_TYPES else None


def _pack_short_name(user_id: int, bot_username: str, pack_number: int = 0) -> str:
    """Build a Telegram-valid sticker-set short name.

    Telegram requires a short name to start with a letter, contain only
    letters/numbers/underscores, have no consecutive underscores, and end in
    ``_by_<bot_username>``.  Keep the generated name below Telegram's 64
    character limit even when the username is long.
    """
    username = re.sub(r"[^A-Za-z0-9_]", "", bot_username or "").strip("_")
    username = re.sub(r"_+", "_", username)
    if not username:
        raise ValueError("The bot must have a valid Telegram username.")

    suffix = f"_by_{username}"
    prefix = f"k{user_id}" if pack_number == 0 else f"k{user_id}_{pack_number}"
    prefix = re.sub(r"_+", "_", prefix).strip("_")
    max_prefix_length = 64 - len(suffix)
    prefix = prefix[:max_prefix_length].rstrip("_")
    return f"{prefix}{suffix}"


# ------------------------------------------
@app.on_message(filters.command("get_sticker"))
@capture_err
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("Reply to a sticker.")

    if not r.sticker:
        return await message.reply("Reply to a sticker.")

    m = await message.reply("Sending..")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    os.remove(f)
#----------------
@app.on_message(filters.command("kang"))
@capture_err
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a sticker/image to kang it.")
    if not message.from_user:
        return await message.reply_text(
            "You are anon admin, kang stickers in my pm."
        )
    msg = await message.reply_text("Kanging Sticker..")

    # Find the proper emoji
    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif (
        message.reply_to_message.sticker
        and message.reply_to_message.sticker.emoji
    ):
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🤔"

    # Get the corresponding fileid, resize the file if necessary
    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(
                    message.reply_to_message.sticker.file_id
                ),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10000000:
                return await msg.edit("File size too large.")

            temp_file_path = await app.download_media(doc)
            image_type = _detect_image_type(temp_file_path)
            if image_type not in SUPPORTED_TYPES:
                return await msg.edit(
                    "Format not supported! ({})".format(image_type)
                )
            try:
                temp_file_path = await resize_file_to_sticker_size(
                    temp_file_path
                )
            except OSError as e:
                await msg.edit_text("Something wrong happened.")
                raise Exception(
                    f"Something went wrong while resizing the sticker (at {temp_file_path}); {e}"
                )
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("Nope, can't kang that.")
    except ShortnameOccupyFailed:
        await message.reply_text("Change Your Name Or Username")
        return

    except Exception as e:
        await message.reply_text(str(e))
        e = format_exc()
        return print(e)
#-------
    packnum = 0
    bot_username = getattr(client, "username", None)
    if not bot_username:
        bot_username = (await client.get_me()).username
    try:
        packname = _pack_short_name(message.from_user.id, bot_username, packnum)
    except ValueError as error:
        return await msg.edit_text(f"❌ {error}")
    limit = 0
    try:
        while True:
            # Prevent infinite rules
            if limit >= 50:
                return await msg.delete()

            # Telegram can return STICKERSET_INVALID for an old/deleted pack.
            # Treat it as missing so /kang recreates the pack instead of
            # exposing a traceback to the chat.
            try:
                stickerset = await get_sticker_set_by_name(client, packname)
            except Exception as error:
                if "STICKERSET_INVALID" in str(error):
                    stickerset = None
                else:
                    raise
            if not stickerset:
                try:
                    stickerset = await create_sticker_set(
                        client,
                        message.from_user.id,
                        f"{message.from_user.first_name[:32]}'s kang pack",
                        packname,
                        [sticker],
                    )
                except (PackShortNameInvalid, ShortnameOccupyFailed):
                    packnum += 1
                    packname = _pack_short_name(
                        message.from_user.id, bot_username, packnum
                    )
                    limit += 1
                    continue
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = _pack_short_name(
                    message.from_user.id, bot_username, packnum
                )
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[ERROR]: INVALID_EMOJI_IN_ARGUMENT")
            limit += 1
            break

        await msg.edit(
            "Sticker Kanged To [Pack](t.me/addstickers/{})\nEmoji: {}".format(
                packname, sticker_emoji
            )
        )
    except PackShortNameInvalid:
        await msg.edit(
            "❌ Telegram rejected the sticker-pack name. "
            "Please try `/kang` again."
        )
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Start", url=f"t.me/{BOT_USERNAME}")]]
        )
        await msg.edit(
            "You Need To Start A Private Chat With Me.",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await message.reply_text(
            "Stickers must be png files but the provided image was not a png"
        )
    except StickerPngDimensions:
        await message.reply_text("The sticker png dimensions are invalid.")