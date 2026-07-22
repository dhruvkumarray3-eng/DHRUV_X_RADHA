# SHUKLA MUSIC — Telegram Music Bot

A feature-rich Telegram Music Bot built with Pyrogram + PyTgCalls. Streams audio/video in Telegram group voice chats, supports YouTube, Spotify, Apple Music, SoundCloud, and more.

## How to run

```
python3 -m SHUKLAMUSIC
```

The workflow **"Start application"** is already configured and runs this command automatically.

## Push to GitHub

Run this from the Shell tab to commit and push your changes:

```bash
bash gitpush.sh "your commit message"
```

Requires `GIT_TOKEN` secret to be set. Pushes to `main` branch of the GitHub repo.

## Required secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB connection string |
| `STRING_SESSION` | Pyrogram string session for the assistant account |
| `GIT_TOKEN` | GitHub personal access token (for pushing to GitHub) |

## Environment variables (already configured)

| Variable | Value |
|---|---|
| `LOGGER_ID` | Your log group/channel ID |
| `LOG_GROUP_ID` | Same as LOGGER_ID |
| `UPSTREAM_REPO` | GitHub repo URL |
| `UPSTREAM_BRANCH` | `main` |

## Stack

- **Python 3.12** — Runtime
- **Pyrogram 2.x** — Telegram MTProto client
- **PyTgCalls / py-tgcalls** — Voice chat streaming
- **MongoDB / Motor** — Async database
- **APScheduler** — Night mode auto scheduler
- **yt-dlp** — YouTube downloading
- **Spotipy** — Spotify API

## User preferences

- Keep the existing project structure unchanged.
- Auto-push to GitHub via `gitpush.sh` using `GIT_TOKEN`.
