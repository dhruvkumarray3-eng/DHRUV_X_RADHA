from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
import requests
import os

@app.on_message(filters.command("vid"))
async def video_downloader(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a video URL.\n\nExample:\n/vid Any_video_url")

    video_url = message.text.split(None, 1)[1]

    msg = await message.reply("🔍 Fetching video...")

    # Step 1: Call API
    payload = {
        "url": video_url,
        "token": "c99f113fab0762d216b4545e5c3d615eefb30f0975fe107caab629d17e51b52d"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14)",
    }

    try:
        r = requests.post("https://allvideodownloader.cc/wp-json/aio-dl/video-data/", data=payload, headers=headers)
        data = r.json()

        if "medias" not in data or not data["medias"]:
            return await msg.edit("❌ No downloadable video found.")

        # Step 2: Get best HD quality video URL (prefer 1080p > 720p > highest available)
        def _quality_rank(m):
            q = (m.get("quality") or m.get("extension") or "").lower()
            if "1080" in q: return 100
            if "720" in q:  return 90
            if "480" in q:  return 70
            if "360" in q:  return 50
            try:
                return int("".join(filter(str.isdigit, q)) or "0")
            except Exception:
                return 0
        best_video = sorted(data["medias"], key=_quality_rank, reverse=True)[0]
        video_link = best_video["url"]

        # Step 3: Download the video to temp file
        await msg.edit("⬇️ Downloading video...")

        file_name = "video.mp4"
        with requests.get(video_link, stream=True) as v:
            with open(file_name, "wb") as f:
                for chunk in v.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Step 4: Send video to user
        await app.send_video(
            chat_id=message.chat.id,
            video=file_name,
            caption=f"🎬 {data.get('title', 'Video')}\n\n✅ ",
            supports_streaming=True
        )

        await msg.delete()
        os.remove(file_name)

    except Exception as e:
        await msg.edit(f"❌ Error: {str(e)}")
