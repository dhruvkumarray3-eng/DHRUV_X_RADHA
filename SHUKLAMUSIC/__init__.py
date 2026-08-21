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

import asyncio

# Pyrogram's sync helpers inspect the current loop during import. Newer
# Python/uvloop combinations do not create one automatically.
try:
    import uvloop

    uvloop.install()
    asyncio.set_event_loop(uvloop.new_event_loop())
except ImportError:
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

from SHUKLAMUSIC.core.bot import SHUKLA

# Newer Pyrogram builds do not expose the presentation-only ButtonStyle and
# custom emoji arguments used by this bot's keyboard helpers.
import pyrogram.enums as _pyrogram_enums
import pyrogram.errors as _pyrogram_errors
from pyrogram.types import InlineKeyboardButton as _InlineKeyboardButton


class _ButtonStyle:
    PRIMARY = None
    SECONDARY = None
    SUCCESS = None
    DANGER = None


if not hasattr(_pyrogram_enums, "ButtonStyle"):
    _pyrogram_enums.ButtonStyle = _ButtonStyle
if not hasattr(_pyrogram_errors, "GroupcallForbidden"):
    _pyrogram_errors.GroupcallForbidden = _pyrogram_errors.GroupCallInvalid
if not hasattr(_pyrogram_errors, "GroupcallInvalid"):
    _pyrogram_errors.GroupcallInvalid = _pyrogram_errors.GroupCallInvalid

_button_init = _InlineKeyboardButton.__init__


def _compatible_button_init(self, *args, **kwargs):
    kwargs.pop("style", None)
    kwargs.pop("icon_custom_emoji_id", None)
    return _button_init(self, *args, **kwargs)


_InlineKeyboardButton.__init__ = _compatible_button_init
from SHUKLAMUSIC.core.dir import dirr
from SHUKLAMUSIC.core.git import git
from SHUKLAMUSIC.core.userbot import Userbot
from SHUKLAMUSIC.misc import dbb, heroku
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = SHUKLA()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

APP = "InflexOwnerBot"
