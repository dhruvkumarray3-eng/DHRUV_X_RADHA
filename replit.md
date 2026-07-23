# SHUKLAMUSIC — Nobita X Prime Telegram Music Bot

A Pyrogram-based Telegram bot that streams music and video in group voice chats. Supports YouTube, Spotify, SoundCloud, and more, with queue management, admin controls, and up to 5 assistant accounts for simultaneous voice chats.

## Stack

- **Language:** Python 3.12
- **Telegram library:** Pyrogram + py-tgcalls + ntgcalls
- **Database:** MongoDB (via Motor async driver)
- **Media:** yt-dlp, ffmpeg

## How to run

```
python3 -m SHUKLAMUSIC
```

The run workflow is already configured as **Start application**.

## Required secrets (add via Replit Secrets)

| Secret | Description |
|--------|-------------|
| `BOT_TOKEN` | Telegram bot token from @BotFather — **required** |
| `MONGO_DB_URI` | MongoDB connection string — **required** |
| `STRING1` | Pyrogram session string for assistant account 1 — **required for voice chat streaming** |
| `STRING2`–`STRING5` | Additional assistant session strings — optional, for multiple simultaneous voice chats |
| `GIT_TOKEN` | GitHub personal access token — optional, used for the `/update` autopush command |

## Optional environment variables (already set in .replit)

| Variable | Value | Description |
|----------|-------|-------------|
| `OWNER_ID` | 8245258112 | Telegram user ID of the bot owner |
| `LOGGER_ID` | -1004458016685 | Telegram group ID where the bot logs events |
| `UPSTREAM_REPO` | github.com/dhruvkumarray3-eng/DHRUV_X_RADHA | Repo used for `/update` command |
| `UPSTREAM_BRANCH` | main | Branch for `/update` |

## Generating a Pyrogram session string (STRING1)

Run this locally and paste the output string as the `STRING1` secret:

```python
from pyrogram import Client
api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"
with Client("session", api_id=api_id, api_hash=api_hash) as app:
    print(app.export_session_string())
```

## Project structure

```
SHUKLAMUSIC/
├── core/          # Bot, userbot, and MongoDB client setup
├── plugins/       # All command handlers (music, admin, tools, misc)
├── platforms/     # Platform integrations (YouTube, Spotify, etc.)
├── mongo/         # MongoDB collection helpers
├── utils/         # Utilities (thumbnails, formatters, etc.)
├── assets/        # Static assets (fonts, images)
├── config.py      # Reads all config from environment variables
└── __main__.py    # Entry point
```
