# SHUKLA MUSIC — Telegram Music Bot

A feature-rich Telegram Music Bot built with Pyrogram + PyTgCalls. Streams audio/video in Telegram group voice chats, supports YouTube, Spotify, Apple Music, SoundCloud, and more.

## How to run

```
python3 -m SHUKLAMUSIC
```

The workflow **"Start application"** is already configured and runs this command automatically.

## Required secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB connection string |
| `LOGGER_ID` | Telegram group/channel ID for bot logs (bot must be admin there) |
| `STRING_SESSION` | Pyrogram string session for the assistant account |
| `OWNER_ID` | Your Telegram user ID |
| `GIT_TOKEN` | GitHub personal access token (for pushing to GitHub) |

## Stack

- **Python 3.11**
- **Pyrogram 2.x** — Telegram MTProto client
- **PyTgCalls** — Voice chat streaming
- **MongoDB / Motor** — Async database
- **APScheduler** — Night mode scheduler
- **yt-dlp** — YouTube downloading
- **Spotipy** — Spotify API

## User preferences

- Keep the existing project structure unchanged.
