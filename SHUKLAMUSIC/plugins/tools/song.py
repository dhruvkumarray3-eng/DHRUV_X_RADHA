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
from pyrogram import filters
from pyrogram.enums import ButtonStyle, ChatAction
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from SHUKLAMUSIC import app, YouTube
from SHUKLAMUSIC.platforms.Youtube import download_song, download_video
from config import (
    BANNED_USERS,
    SONG_DOWNLOAD_DURATION,
    SONG_DOWNLOAD_DURATION_LIMIT,
)
from SHUKLAMUSIC.utils.decorators.language import language, languageCB
from SHUKLAMUSIC.utils.errors import capture_err, capture_callback_err
from SHUKLAMUSIC.utils.formatters import time_to_seconds
from SHUKLAMUSIC.utils.inline.song import song_markup

SONG_COMMAND = ["song"]


@app.on_message(filters.command(SONG_COMMAND) & filters.group & ~BANNED_USERS)
@capture_err
@language
async def song_command_group(client, message: Message, lang):
    await message.reply_text(
        lang["song_1"],
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                lang["SG_B_1"],
                url=f"https://t.me/{app.username}?start=song",
                style=ButtonStyle.PRIMARY,
            )]]
        ),
    )


@app.on_message(filters.command(SONG_COMMAND) & filters.private & ~BANNED_USERS)
@capture_err
@language
async def song_command_private(client, message: Message, lang):
    await message.delete()
    mystic = await message.reply_text(lang["play_1"])

    url = await YouTube.url(message)
    query = url or (message.text.split(None, 1)[1] if len(message.command) > 1 else None)
    if not query:
        return await mystic.edit_text(lang["song_2"])

    if url and not await YouTube.exists(url):
        return await mystic.edit_text(lang["song_5"])

    try:
        title, dur_min, dur_sec, thumb, vidid = await YouTube.details(query)
    except Exception:
        return await mystic.edit_text(lang["play_3"])

    if not dur_min:
        return await mystic.edit_text(lang["song_3"])
    if int(dur_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(lang["play_4"].format(SONG_DOWNLOAD_DURATION, dur_min))

    await mystic.delete()
    await message.reply_photo(
        thumb,
        caption=lang["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(song_markup(lang, vidid)),
    )


@app.on_callback_query(filters.regex(r"song_back") & ~BANNED_USERS)
@capture_callback_err
@languageCB
async def songs_back_helper(client, cq, lang):
    _ignored, req = cq.data.split(None, 1)
    stype, vidid = req.split("|")
    await cq.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(song_markup(lang, vidid))
    )


@app.on_callback_query(filters.regex(r"song_helper") & ~BANNED_USERS)
@capture_callback_err
@languageCB
async def song_helper_cb(client, cq, lang):
    _ignored, req = cq.data.split(None, 1)
    stype, vidid = req.split("|")

    try:
        await cq.answer(lang["song_6"], show_alert=True)
    except Exception:
        pass

    buttons = [
        [InlineKeyboardButton(
            text="⬇️ ᴅᴏᴡɴʟᴏᴀᴅ",
            callback_data=f"song_download {stype}|direct|{vidid}",
            style=ButtonStyle.SUCCESS,
        )],
        [
            InlineKeyboardButton(
                lang["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                lang["CLOSE_BUTTON"],
                callback_data="close",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]
    await cq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"song_download") & ~BANNED_USERS)
@capture_callback_err
@languageCB
async def song_download_cb(client, cq, lang):
    try:
        await cq.answer("⬇️ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ…")
    except Exception:
        pass

    _ignored, req = cq.data.split(None, 1)
    stype, fmt_id, vidid = req.split("|")
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    # Download the thumbnail from the photo FIRST before we touch the message
    thumb = None
    try:
        thumb = await cq.message.download()
    except Exception:
        pass

    # Update caption only (keep the photo intact)
    try:
        await cq.message.edit_caption(lang["song_8"])
    except Exception:
        pass

    file_path = None
    try:
        info, _v = await YouTube.track(yturl)
        title = re.sub(r"\W+", " ", info["title"])
        duration_sec = time_to_seconds(info.get("duration_min")) if info.get("duration_min") else None
        uploader = info.get("uploader", "YouTube")

        if stype == "audio":
            file_path = await download_song(yturl)
            if not file_path:
                try:
                    await cq.message.edit_caption(lang["song_10"])
                except Exception:
                    pass
                return

            try:
                await cq.message.edit_caption(lang["song_11"])
            except Exception:
                pass
            await app.send_chat_action(cq.message.chat.id, ChatAction.UPLOAD_AUDIO)
            await app.send_audio(
                chat_id=cq.message.chat.id,
                audio=file_path,
                caption=f"🎵 <b>{title}</b>\n\n<emoji id=5409235997613372119>©</emoji> ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href=https://t.me/II_NOBITA_X_PRIME_II>𝚴 𝐎 𝐁 𝚰 𝐓 𝚲 ❤️‍🔥</a>",
                title=title,
                performer=uploader,
                thumb=thumb,
                reply_to_message_id=cq.message.id,
            )
        else:
            file_path = await download_video(yturl)
            if not file_path:
                try:
                    await cq.message.edit_caption(lang["song_10"])
                except Exception:
                    pass
                return

            try:
                await cq.message.edit_caption(lang["song_11"])
            except Exception:
                pass
            await app.send_chat_action(cq.message.chat.id, ChatAction.UPLOAD_VIDEO)
            await app.send_video(
                chat_id=cq.message.chat.id,
                video=file_path,
                duration=duration_sec,
                caption=f"🎬 <b>{title}</b>\n\n<emoji id=5409235997613372119>©</emoji> ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href=https://t.me/II_NOBITA_X_PRIME_II>𝚴 𝐎 𝐁 𝚰 𝐓 𝚲 ❤️‍🔥</a>",
                thumb=thumb,
                supports_streaming=True,
                reply_to_message_id=cq.message.id,
            )

    except Exception as err:
        print(f"[SONG] download error: {err}")
        try:
            await cq.message.edit_caption(lang["song_10"])
        except Exception:
            pass
    finally:
        # Cleanup temp files
        for f in [file_path, thumb]:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except Exception:
                    pass
