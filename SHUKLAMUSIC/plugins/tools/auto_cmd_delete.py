# -----------------------------------------------
# 🔸 NOBITA X PRIME — Auto Command Delete
# Runs at handler group -1 (before all other handlers).
# Silently deletes every bot command message sent in a group,
# so every plugin gets clean chat regardless of its decorator.
# -----------------------------------------------
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from SHUKLAMUSIC import app


def _is_bot_command(_, __, message: Message) -> bool:
    """True when the message is a bot command sent in a group/supergroup."""
    if message.chat and message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return False
    return bool(message.command)


_bot_cmd_filter = filters.create(_is_bot_command, name="BotCommandFilter")


@app.on_message(_bot_cmd_filter, group=-1)
async def _auto_delete_command(_, message: Message):
    """Delete the command message before any handler processes it."""
    try:
        await message.delete()
    except Exception:
        # Bot lacks 'Delete Messages' permission — nothing we can do silently.
        pass
