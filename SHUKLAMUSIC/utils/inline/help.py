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
from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from SHUKLAMUSIC import app

# ── Premium emoji IDs ──
_E_SHIELD  = 4958900559139570572   # 🛡  Admin
_E_BELL    = 4956290155326473271   # 🔔  Auth
_E_MEGA    = 4958686613933655185   # 📣  G-Cast
_E_BAN     = 4956337889593000947   # 🚫  Bl-Chat
_E_SKULL   = 4958642964181025908   # 💀  Bl-Users
_E_PLAY    = 4956250031741993892   # ▶️  C-Play
_E_XSKULL  = 4956461073550017373   # ☠️  G-Ban
_E_LOOP    = 4956371914323920049   # 🔄  Loop
_E_CHART   = 4958506272551863292   # 📊  Log
_E_BOLT    = 4958479549265347295   # ⚡️  Ping
_E_MUSIC   = 4958562566688211974   # 🎶  Play
_E_HAT     = 4956564307383944011   # 🎩  Shuffle
_E_SEARCH  = 4958587679361991667   # 🔍  Seek
_E_MIC     = 4956441587283395517   # 🎤  Song
_E_CAR     = 4958801766301828295   # 🚗  Speed
_E_CLOSE   = 4958526153955476488   # ❌  Close
_E_BACK    = 4956282853882069908   # ➡️  Back
_E_BULB    = 4958665796227171144   # 💡  Help DM
_E_FIGHT   = 5978869985299142389   # 🤕  ChatFight
_E_GITHUB  = 5208748315805499400   # ✅  GitHub
_E_CHATBOT = 6073117703965511893   # 💐  ChatBot
_E_GAMES   = 6271653280187684816   # 🌟  Games
_E_KEY     = 6269140848873574815   # ❤️  String Gen
_E_SWORD   = 4958900559139570572   # ⚔️  Bans
_E_PIN     = 4956232383721374836   # 📌  Tags
_E_WAVE    = 4956290155326473271   # 👋  Welcome
_E_HEART   = 4958597497657230624   # 💑  Couple
_E_INFO    = 4958529074533238201   # ℹ️  User Info
_E_TRUTH   = 4958479549265347295   # ⚡  Truth-Dare
_E_NOTES   = 4958506272551863292   # 📋  Notes
_E_AFK     = 4956564307383944011   # 💤  AFK
_E_CRYPTO  = 4958665796227171144   # 💰  Crypto
_E_VC      = 4958562566688211974   # 🔊  VC Logs


def _nav_row(_, prev_cb: str, back_cb: str, next_cb: str, is_start: bool):
    return [
        InlineKeyboardButton(text="⬅️", callback_data=prev_cb, style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(
            text=_["BACK_BUTTON"] if is_start else _["CLOSE_BUTTON"],
            callback_data=back_cb,
            style=ButtonStyle.SUCCESS,
            icon_custom_emoji_id=_E_BACK,
        ),
        InlineKeyboardButton(text="➡️", callback_data=next_cb, style=ButtonStyle.PRIMARY),
    ]


# ─── PAGE 1 : hb1 – hb12 ────────────────────────────────────────────────────
def help_pannel_page1(_, START: Union[bool, int] = None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=_["H_B_1"],  callback_data="help_callback hb1",  style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_SHIELD),
            InlineKeyboardButton(text=_["H_B_2"],  callback_data="help_callback hb2",  style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_BELL),
            InlineKeyboardButton(text=_["H_B_3"],  callback_data="help_callback hb3",  style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_MEGA),
        ],
        [
            InlineKeyboardButton(text=_["H_B_4"],  callback_data="help_callback hb4",  style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_BAN),
            InlineKeyboardButton(text=_["H_B_5"],  callback_data="help_callback hb5",  style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_SKULL),
            InlineKeyboardButton(text=_["H_B_6"],  callback_data="help_callback hb6",  style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_PLAY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_7"],  callback_data="help_callback hb7",  style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_XSKULL),
            InlineKeyboardButton(text=_["H_B_8"],  callback_data="help_callback hb8",  style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_LOOP),
            InlineKeyboardButton(text=_["H_B_9"],  callback_data="help_callback hb9",  style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_CHART),
        ],
        [
            InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_BOLT),
            InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11", style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_MUSIC),
            InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12", style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_HAT),
        ],
        _nav_row(_, "help_page_3", "settingsback_helper" if START else "close", "help_page_2", bool(START)),
    ])


# ─── PAGE 2 : hb13 – hb21 ───────────────────────────────────────────────────
def help_pannel_page2(_, START: Union[bool, int] = None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_SEARCH),
            InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_MIC),
            InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_CAR),
        ],
        [
            InlineKeyboardButton(text="🤕 ᴄʜᴀᴛғɪɢʜᴛ",   callback_data="help_callback hb16", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_FIGHT),
            InlineKeyboardButton(text="🫡 ɢɪᴛʜᴜʙ",        callback_data="help_callback hb17", style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_GITHUB),
            InlineKeyboardButton(text="🫠 ᴄʜᴀᴛʙᴏᴛ",       callback_data="help_callback hb18", style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_CHATBOT),
        ],
        [
            InlineKeyboardButton(text="🦁 ɢᴀᴍᴇs",         callback_data="help_callback hb19", style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_GAMES),
            InlineKeyboardButton(text="❤️‍🩹 sᴛʀɪɴɢ ɢᴇɴ",  callback_data="help_callback hb20", style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_KEY),
            InlineKeyboardButton(text="✨ ǫᴜɪᴄᴋ ɢᴀᴍᴇs",   callback_data="help_callback hb21", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_GAMES),
        ],
        _nav_row(_, "help_page_1", "settingsback_helper" if START else "close", "help_page_3", bool(START)),
    ])


# ─── PAGE 3 : hb22 – hb31  (new sections) ───────────────────────────────────
def help_pannel_page3(_, START: Union[bool, int] = None):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="⚔️ ʙᴀɴs",          callback_data="help_callback hb22", style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_SWORD),
            InlineKeyboardButton(text="📌 ᴛᴀɢs",           callback_data="help_callback hb23", style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_PIN),
            InlineKeyboardButton(text="👋 ᴡᴇʟᴄᴏᴍᴇ",       callback_data="help_callback hb24", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_WAVE),
        ],
        [
            InlineKeyboardButton(text="💑 ᴄᴏᴜᴘʟᴇ",        callback_data="help_callback hb25", style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_HEART),
            InlineKeyboardButton(text="ℹ️ ᴜsᴇʀ ɪɴғᴏ",     callback_data="help_callback hb26", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_INFO),
            InlineKeyboardButton(text="⚡ ᴛʀᴜᴛʜ-ᴅᴀʀᴇ",    callback_data="help_callback hb27", style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_TRUTH),
        ],
        [
            InlineKeyboardButton(text="📋 ɴᴏᴛᴇs",          callback_data="help_callback hb28", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_NOTES),
            InlineKeyboardButton(text="💤 ᴀғᴋ",            callback_data="help_callback hb29", style=ButtonStyle.DANGER,    icon_custom_emoji_id=_E_AFK),
            InlineKeyboardButton(text="💰 ᴄʀʏᴘᴛᴏ & ᴜᴘɪ",  callback_data="help_callback hb30", style=ButtonStyle.SUCCESS,   icon_custom_emoji_id=_E_CRYPTO),
        ],
        [
            InlineKeyboardButton(text="🔊 ᴠᴄ ʟᴏɢs",       callback_data="help_callback hb31", style=ButtonStyle.PRIMARY,   icon_custom_emoji_id=_E_VC),
        ],
        _nav_row(_, "help_page_2", "settingsback_helper" if START else "close", "help_page_1", bool(START)),
    ])


# ─── Legacy alias (page 1 is the default) ───────────────────────────────────
def help_pannel(_, START: Union[bool, int] = None):
    return help_pannel_page1(_, START)


def help_back_markup(_, page: int = 1):
    page_cb = f"help_page_{page}"
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=page_cb,
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id=_E_BACK,
            )
        ]
    ])


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id=_E_BULB,
            ),
        ],
    ]
