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

# Keep the presentation styles and custom button icons when the installed
# Pyrogram build supports them. Older builds need those optional fields
# removed, otherwise constructing a keyboard raises a TypeError.
import inspect
import pyrogram.enums as _pyrogram_enums
import pyrogram.errors as _pyrogram_errors
from pyrogram.types import InlineKeyboardButton as _InlineKeyboardButton


if not hasattr(_pyrogram_enums, "ButtonStyle"):
    class _ButtonStyle:
        PRIMARY = None
        SECONDARY = None
        SUCCESS = None
        DANGER = None

    _pyrogram_enums.ButtonStyle = _ButtonStyle
if not hasattr(_pyrogram_errors, "GroupcallForbidden"):
    _pyrogram_errors.GroupcallForbidden = _pyrogram_errors.GroupCallInvalid
if not hasattr(_pyrogram_errors, "GroupcallInvalid"):
    _pyrogram_errors.GroupcallInvalid = _pyrogram_errors.GroupCallInvalid

_button_parameters = inspect.signature(_InlineKeyboardButton).parameters
_unsupported_button_fields = {
    field for field in ("style", "icon_custom_emoji_id")
    if field not in _button_parameters
}
if _unsupported_button_fields:
    _button_init = _InlineKeyboardButton.__init__

    def _compatible_button_init(self, *args, **kwargs):
        for field in _unsupported_button_fields:
            kwargs.pop(field, None)
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
