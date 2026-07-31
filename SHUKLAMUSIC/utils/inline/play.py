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


def stream_markup_timer(_, chat_id, played, dur, videoid=None, autoplay=False):
    played_sec = 0
    duration_sec = 0
    try:
        played_sec = time_to_seconds(played)
        duration_sec = time_to_seconds(dur)
        _pct = (played_sec / duration_sec * 100) if duration_sec > 0 else 0
    except (ValueError, ZeroDivisionError, TypeError):
        pass

    # Sanitise display strings so the button never shows "-" or raw error text
    display_played = played if (played and played not in ("-", "")) else "0:00"
    display_dur = dur if (dur and dur not in ("-", "")) else "Live"

    # Bar fills proportionally: 12 steps across the full song duration so it
    # reaches NOBITAXPRIME❤️‍🔥 exactly at the end — works for any song length.
    # step 0 = just started, step 11 = song ≥ 11/12 done (bar fully filled).
    if duration_sec > 0:
        step = min(11, int(played_sec / duration_sec * 12))
    else:
        step = 0

    _BARS = [
        "𝚴❤️‍🔥···········",
        "𝚴𝐎❤️‍🔥··········",
        "𝚴𝐎𝐁❤️‍🔥·········",
        "𝚴𝐎𝐁𝚰❤️‍🔥········",
        "𝚴𝐎𝐁𝚰𝐓❤️‍🔥·······",
        "𝚴𝐎𝐁𝚰𝐓𝚲❤️‍🔥······",
        "𝚴𝐎𝐁𝚰𝐓𝚲𝐗❤️‍🔥·····",
        "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸❤️‍🔥····",
        "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑❤️‍🔥···",
        "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑𝐈❤️‍🔥··",
        "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑𝐈𝐌❤️‍🔥·",
        "𝚴𝐎𝐁𝚰𝐓𝚲𝐗𝚸𝐑𝐈𝐌𝐄❤️‍🔥",
    ]
    bar = _BARS[step]
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{display_played} {bar} {display_dur}",
                callback_data="GetTimer",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id=5204046146955153467
            )
        ],
        # Row: Back(green) | Pause(blue) | Resume(green) | Skip(blue)
        [
            InlineKeyboardButton(text="⏮ ʙᴀᴄᴋ", callback_data=f"ADMIN Back|{chat_id}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏸ ᴩᴀᴜsᴇ", callback_data=f"ADMIN Pause|{chat_id}", icon_custom_emoji_id=5409042015415448331, style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▶ ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}", icon_custom_emoji_id=5409222721869459068, style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏭ sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}", style=ButtonStyle.PRIMARY),
        ],
        # Row: Stop(red) | Autoplay(blue)
        [
            InlineKeyboardButton(text="⏹ sᴛᴏᴩ", callback_data=f"ADMIN Stop|{chat_id}", icon_custom_emoji_id=5408832111773757273, style=ButtonStyle.DANGER),
            InlineKeyboardButton(
                text="❤️‍🔥 ᴀᴜᴛᴏᴘʟᴀʏ",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                icon_custom_emoji_id=6271653280187684816,
                style=ButtonStyle.PRIMARY,
            ),
        ],
    ]
    # Download row for autoplay songs — preserved during timer ticks
    if autoplay and videoid and videoid not in {"telegram", "soundcloud"}:
        buttons.append([
            InlineKeyboardButton(
                text="⬇️ ᴛᴀᴘ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ",
                url=f"https://t.me/{app.username}?start=dl_{videoid}_a",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id=5309984423003823246,
            ),
        ])
    buttons += [
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


def _dl_buttons(app_username, videoid):
    """Return a [audio, video] download button row, or [] if videoid is invalid."""
    if not videoid or videoid in {"telegram", "soundcloud"}:
        return []
    return [[
        InlineKeyboardButton(
            text="🎵 ᴀᴜᴅɪᴏ",
            url=f"https://t.me/{app_username}?start=dl_{videoid}_a",
            style=ButtonStyle.SUCCESS,
            icon_custom_emoji_id=5309984423003823246,
        ),
        InlineKeyboardButton(
            text="🎬 ᴠɪᴅᴇᴏ",
            url=f"https://t.me/{app_username}?start=dl_{videoid}_v",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id=5404870433093048964,
        ),
    ]]


def stream_markup(_, chat_id, videoid=None, autoplay=False):
    """
    autoplay=True  → called from the autoplay engine; shows a single
                     full-width DM-download button below AUTOPLAY and
                     hides the regular audio/video split row.
    autoplay=False → regular play; shows audio + video split row.
    """
    buttons = [
        # Row: Back(green) | Pause(blue) | Resume(green) | Skip(blue)
        [
            InlineKeyboardButton(text="⏮ ʙᴀᴄᴋ", callback_data=f"ADMIN Back|{chat_id}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏸ ᴩᴀᴜsᴇ", callback_data=f"ADMIN Pause|{chat_id}", icon_custom_emoji_id=5409042015415448331, style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▶ ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}", icon_custom_emoji_id=5409222721869459068, style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏭ sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}", style=ButtonStyle.PRIMARY),
        ],
        # Row: Stop(red) | Autoplay(blue)
        [
            InlineKeyboardButton(text="⏹ sᴛᴏᴩ", callback_data=f"ADMIN Stop|{chat_id}", icon_custom_emoji_id=5408832111773757273, style=ButtonStyle.DANGER),
            InlineKeyboardButton(
                text="❤️‍🔥 ᴀᴜᴛᴏᴘʟᴀʏ",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                icon_custom_emoji_id=6271653280187684816,
                style=ButtonStyle.PRIMARY,
            ),
        ],
    ]
    # Download row — differs between autoplay and regular play
    if autoplay and videoid and videoid not in {"telegram", "soundcloud"}:
        # Single full-width "DM download" button for autoplay songs
        buttons.append([
            InlineKeyboardButton(
                text="⬇️ ᴛᴀᴘ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ",
                url=f"https://t.me/{app.username}?start=dl_{videoid}_a",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id=5309984423003823246,
            ),
        ])
    elif not autoplay and videoid and videoid not in {"telegram", "soundcloud"}:
        # Regular play: keep audio + video split
        buttons.append([
            InlineKeyboardButton(
                text="🎵 ᴀᴜᴅɪᴏ",
                url=f"https://t.me/{app.username}?start=dl_{videoid}_a",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id=5309984423003823246,
            ),
            InlineKeyboardButton(
                text="🎬 ᴠɪᴅᴇᴏ",
                url=f"https://t.me/{app.username}?start=dl_{videoid}_v",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id=5404870433093048964,
            ),
        ])
    buttons += [
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
