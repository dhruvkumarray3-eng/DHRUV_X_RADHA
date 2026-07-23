import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from config import BANNED_USERS

# nekos.best API — free anime GIF reactions
NEKOS_API = "https://nekos.best/api/v2/{action}"

ACTIONS = {
    "hug":       ("🤗", "{user} hugs {target}! 🤗"),
    "pat":       ("🥰", "{user} pats {target}! 🥰"),
    "slap":      ("👋", "{user} slaps {target}! 😤"),
    "kiss":      ("😘", "{user} kisses {target}! 💋"),
    "cuddle":    ("🫂", "{user} cuddles with {target}! 🫂"),
    "wave":      ("👋", "{user} waves at {target}! 👋"),
    "poke":      ("👉", "{user} pokes {target}! 👉"),
    "bite":      ("😬", "{user} bites {target}! 😬"),
    "punch":     ("👊", "{user} punches {target}! 💥"),
    "handshake": ("🤝", "{user} shakes hands with {target}! 🤝"),
    "thumbsup":  ("👍", "{user} gives 👍 to {target}!"),
    "smile":     ("😄", "{user} smiles at {target}! 😄"),
    "happy":     ("😊", "{user} is feeling happy! 😊"),
    "sad":       ("😢", "{user} is feeling sad 😢"),
    "blush":     ("😊", "{user} is blushing! 😊"),
    "dance":     ("💃", "{user} is dancing! 💃"),
}

# Actions that don't require a target
SOLO_ACTIONS = {"happy", "sad", "blush", "dance"}

# Map to nekos.best endpoint names (some differ)
NEKOS_MAP = {
    "thumbsup": "thumbsup",
    "handshake": "handshake",
}


async def fetch_nekos_gif(action: str) -> str | None:
    endpoint = NEKOS_MAP.get(action, action)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                NEKOS_API.format(action=endpoint),
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    results = data.get("results", [])
                    if results:
                        return results[0].get("url")
    except Exception:
        pass
    return None


def build_handler(action: str):
    emoji, template = ACTIONS[action]

    async def handler(client, message: Message):
        user = message.from_user.mention if message.from_user else "Someone"

        if action in SOLO_ACTIONS:
            target = ""
            text = template.format(user=user, target="").strip()
        elif message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user.mention
            text = template.format(user=user, target=target)
        elif len(message.command) > 1:
            raw = message.text.split(None, 1)[1]
            text = template.format(user=user, target=raw)
        else:
            return await message.reply_text(
                f"{emoji} **Reply to a user** or mention them!\n"
                f"Usage: `/{action} @username`"
            )

        gif_url = await fetch_nekos_gif(action)
        if gif_url:
            await message.reply_animation(gif_url, caption=f"**{text}**")
        else:
            await message.reply_text(f"**{text}**")

    handler.__name__ = f"feelings_{action}"
    return handler


# Register all handlers
for _action in ACTIONS:
    _handler = build_handler(_action)
    app.on_message(filters.command(_action) & ~BANNED_USERS)(_handler)
