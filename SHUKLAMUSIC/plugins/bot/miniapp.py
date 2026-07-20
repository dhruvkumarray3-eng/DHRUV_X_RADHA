# -----------------------------------------------
# 🔸 SHUKLAMUSIC — Mini App (Web App) Handler
# 🔹 Receives data from the Nobita Music mini app
#    and sends the requested song to the user.
# -----------------------------------------------
import json
import os

import aiohttp
from pyrogram import filters
from pyrogram.types import Message

from SHUKLAMUSIC import app
from config import BANNED_USERS

_API_URL = "https://api01.shrutibots.site"
_API_KEY = "ShrutiBots2knm7tCsnIVesZt50Lwb"
_POWERED = (
    "✦ ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/II_NOBITA_X_PRIME_II'>"
    "𝚴 𝐎 𝐁 𝚰 𝐓 𝚲 𝐗 𝚸 𝐑 𝐈 𝐌 𝐄❤️‍🔥</a>"
)


def _extract_vid(raw: str) -> str | None:
    """
    Parse the video ID from whatever the mini app sends.

    Accepted formats (sent by the mini app):
      • JSON  {"url": "https://youtu.be/XXXX"} or {"vidid": "XXXX"} or {"title": "..."}
      • Plain YouTube URL  https://www.youtube.com/watch?v=XXXX
      • Plain 11-char video ID  XXXX
    """
    raw = raw.strip()

    # Try JSON first
    try:
        data = json.loads(raw)
        for key in ("vidid", "video_id", "id"):
            if data.get(key):
                return str(data[key]).strip()
        for key in ("url", "link", "youtube_url"):
            url = data.get(key, "")
            if url:
                raw = url
                break
        if data.get("title"):
            return None  # title-only — handled separately below
    except (json.JSONDecodeError, AttributeError):
        pass

    # Try URL extraction
    if "v=" in raw:
        return raw.split("v=")[-1].split("&")[0].strip()
    if "youtu.be/" in raw:
        return raw.split("youtu.be/")[-1.split("?")[0].strip() if "?" in raw else -1].strip()

    # Bare 11-char ID
    if raw and 8 <= len(raw) <= 12 and " " not in raw:
        return raw

    return None


async def _download_and_send(chat_id: int, vidid: str, status_msg):
    """Download audio via ShrutiAPI and send to user."""
    os.makedirs("downloads", exist_ok=True)
    out_file = f"downloads/{vidid}_miniapp.mp3"
    tmp_file = out_file + ".tmp"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{_API_URL}/download",
                params={"url": vidid, "type": "audio", "api_key": _API_KEY},
                timeout=aiohttp.ClientTimeout(total=300),
            ) as resp:
                if resp.status != 200:
                    await status_msg.edit_text("❌ Song download fail ho gayi. Dobara try karo.")
                    return
                with open(tmp_file, "wb") as f:
                    async for chunk in resp.content.iter_chunked(131072):
                        f.write(chunk)

        if not (os.path.exists(tmp_file) and os.path.getsize(tmp_file) > 0):
            await status_msg.edit_text("❌ Song download fail ho gayi. Dobara try karo.")
            return

        os.replace(tmp_file, out_file)
        await status_msg.delete()
        await app.send_audio(
            chat_id=chat_id,
            audio=out_file,
            caption=f"🎵 <b>ɴᴏʙɪᴛᴀ 𝗫 ᴘʀɪᴍᴇ ᴍᴜsɪᴄ — ᴍɪɴɪ ᴀᴘᴘ ᴅᴏᴡɴʟᴏᴀᴅ</b>\n\n{_POWERED}",
        )
    except Exception as e:
        try:
            await status_msg.edit_text("❌ Song download fail ho gayi. Dobara try karo.")
        except Exception:
            pass
    finally:
        for f in (tmp_file, out_file):
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass


# ── Filter: fires only when a message has web_app_data ──
_has_web_app_data = filters.create(lambda _, __, m: bool(getattr(m, "web_app_data", None)))


@app.on_message(_has_web_app_data & filters.private & ~BANNED_USERS)
async def handle_mini_app_data(client, message: Message):
    """
    Receives data submitted from the Nobita Music mini app and
    downloads + sends the requested song to the user.
    """
    raw = message.web_app_data.data if message.web_app_data else ""
    if not raw:
        return

    status = await message.reply_text("🎵 ᴍɪɴɪ ᴀᴘᴘ sᴇ sᴏɴɢ ʟᴀ ʀʜᴀ ʜᴏᴏɴ... ❤️‍🔥")

    vidid = _extract_vid(raw)

    if not vidid:
        # Title-only: try to extract from JSON
        try:
            data = json.loads(raw)
            title = data.get("title", "").strip()
        except Exception:
            title = raw.strip()

        if not title:
            await status.edit_text("❌ Mini app se koi song info nahi aayi.")
            return

        # Search YouTube for the title via py_yt and pick first result
        try:
            from py_yt import VideosSearch
            results = VideosSearch(title, limit=1)
            entries = (await results.next()).get("result", [])
            if not entries:
                await status.edit_text("❌ Song nahi mila. Dobara try karo.")
                return
            vidid = entries[0]["id"]
        except Exception:
            await status.edit_text("❌ Song search fail ho gayi.")
            return

    await _download_and_send(message.chat.id, vidid, status)
