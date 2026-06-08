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
    if 0 < umm <= 10:
        bar = "▣—————————"
    elif 10 < umm < 20:
        bar = "—▣————————"
    elif 20 <= umm < 30:
        bar = "—▣———————"
    elif 30 <= umm < 40:
        bar = "——▣——————"
    elif 40 <= umm < 50:
        bar = "———▣—————"
    elif 50 <= umm < 60:
        bar = "————▣————"
    elif 60 <= umm < 70:
        bar = "—————▣———"
    elif 70 <= umm < 80:
        bar = "——————▣——"
    elif 80 <= umm < 95:
        bar = "———————▣—"
    else:
        bar = "————————▣"
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
            InlineKeyboardButton(text="", callback_data=f"ADMIN Resume|{chat_id}", icon_custom_emoji_id=5409222721869459068),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Pause|{chat_id}", icon_custom_emoji_id=5409042015415448331),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Stop|{chat_id}", icon_custom_emoji_id=5408832111773757273),
        ],
        [
            InlineKeyboardButton(
                text="ᴜᴘᴅᴀᴛᴇ",
                url="https://t.me/+Imyf3M9TO5k1ODRl",
                icon_custom_emoji_id=5409025823388741707,
                style=ButtonStyle.PRIMARY
                
            ),
            InlineKeyboardButton(
                text="ʜᴏϻє",
                url="https://t.me/+dv_rcq5uIXhmMWM1",
                icon_custom_emoji_id=5409194306365829029,
                style=ButtonStyle.PRIMARY
            
            )
        ],
            

        [InlineKeyboardButton(text=" ᴄʟᴏsᴇ ▣", callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id=5408832111773757273)],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="", callback_data=f"ADMIN Resume|{chat_id}", icon_custom_emoji_id=5409222721869459068),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Pause|{chat_id}", icon_custom_emoji_id=5409042015415448331),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Stop|{chat_id}", icon_custom_emoji_id=5408832111773757273),
        ],
        [
            InlineKeyboardButton(
                text="ᴜᴘᴅᴀᴛᴇ",
                url="https://t.me/+UMo3Ugi68FFkYzVl",
                 icon_custom_emoji_id=5409025823388741707,
                style=ButtonStyle.PRIMARY
                
            ),
            InlineKeyboardButton(
                text="ʜᴏϻє",
                url="https://t.me/ll_YOUR_ANIMExWORLD_ll",
                icon_custom_emoji_id=5409194306365829029,
                style=ButtonStyle.PRIMARY
            
            )
        ],
            

        [InlineKeyboardButton(text=" ᴄʟᴏsᴇ ▣", callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id=5408832111773757273)],
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
