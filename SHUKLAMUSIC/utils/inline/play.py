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
# -------------------------------------

import math
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SHUKLAMUSIC import app
import config
from pyrogram.enums import ButtonStyle
from SHUKLAMUSIC.utils.formatters import time_to_seconds


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    
    umm = math.floor(percentage)
    if 0 <= umm < 8:
        bar = "𝚴❤️‍🔥···········"
    elif 8 <= umm < 17:
        bar = "𝚴𝐎❤️‍🔥··········"
    elif 17 <= umm < 25:
        bar = "𝚴𝐎𝐁❤️‍🔥·········"
    elif 25 <= umm < 33:
        bar = "𝚴𝐎𝐁𝚰❤️‍🔥········"
    elif 33 <= umm < 42:
        bar = "𝚴𝐎𝐁𝚰𝐓❤️‍🔥·······"
    elif 42 <= umm < 50:
        bar = "𝚴𝐎𝐁𝚰𝐓𝚲❤️‍🔥······"
    elif 50 <= umm < 58:
        bar = "𝚴𝐎𝐁𝚰𝐓𝚲𝐗❤️‍🔥·····"
    elif 58 <= umm < 67:
        bar = "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸❤️‍🔥····"
    elif 67 <= umm < 75:
        bar = "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑❤️‍🔥···"
    elif 75 <= umm < 83:
        bar = "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑𝐈❤️‍🔥··"
    elif 83 <= umm < 92:
        bar = "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑𝐈𝐌❤️‍🔥·"
    else:
        bar = "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑𝐈𝐌𝐄❤️‍🔥"
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id=5204046146955153467
            )
        ],
        [
            InlineKeyboardButton(text="", callback_data=f"ADMIN Resume|{chat_id}", icon_custom_emoji_id=5409222721869459068, style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Pause|{chat_id}", icon_custom_emoji_id=5409042015415448331, style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Stop|{chat_id}", icon_custom_emoji_id=5408832111773757273, style=ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(
                text="❤️‍🔥 ᴀᴜᴛᴏᴘʟᴀʏ",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                icon_custom_emoji_id=6271653280187684816,
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="✨ ᴜᴘᴅᴀᴛᴇ",
                url=config.SUPPORT_CHANNEL,
                icon_custom_emoji_id=5409025823388741707,
                style=ButtonStyle.SUCCESS
            ),
            InlineKeyboardButton(
                text="🌹 sᴜᴘᴘᴏꝛᴛ",
                url=config.SUPPORT_CHAT,
                icon_custom_emoji_id=5409194306365829029,
                style=ButtonStyle.PRIMARY
            )
        ],
        [InlineKeyboardButton(text="❤️‍🩹 ᴄʟᴏsᴇ ❤️‍🩹", callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id=5408832111773757273)],
    ]
    return buttons


def stream_markup(_, chat_id, videoid=None):
    buttons = [
        [
            InlineKeyboardButton(text="", callback_data=f"ADMIN Resume|{chat_id}", icon_custom_emoji_id=5409222721869459068, style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Pause|{chat_id}", icon_custom_emoji_id=5409042015415448331, style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Stop|{chat_id}", icon_custom_emoji_id=5408832111773757273, style=ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(
                text="❤️‍🔥 ᴀᴜᴛᴏᴘʟᴀʏ",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                icon_custom_emoji_id=6271653280187684816,
                style=ButtonStyle.PRIMARY,
            ),
        ],
        *(
            [
                [
                    InlineKeyboardButton(
                        text="⬇️ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜɪs sᴏɴɢ",
                        url=f"https://t.me/{app.username}?start=dl_{videoid}_a",
                        style=ButtonStyle.SUCCESS,
                    )
                ]
            ]
            if videoid and videoid not in {"telegram", "soundcloud"}
            else []
        ),
        [
            InlineKeyboardButton(
                text="✨ ᴜᴘᴅᴀᴛᴇ",
                url=config.SUPPORT_CHANNEL,
                icon_custom_emoji_id=5409025823388741707,
                style=ButtonStyle.SUCCESS
            ),
            InlineKeyboardButton(
                text="🌹 sᴜᴘᴘᴏꝛᴛ",
                url=config.SUPPORT_CHAT,
                icon_custom_emoji_id=5409194306365829029,
                style=ButtonStyle.PRIMARY
            )
        ],
        [InlineKeyboardButton(text="❤️‍🩹 ᴄʟᴏsᴇ ❤️‍🩹", callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id=5408832111773757273)],
    ]
    return buttons

def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"SHUKLAPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"SHUKLAPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons
