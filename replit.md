# NOBITA X PRIME Music Bot

A feature-rich Telegram Music Bot built with Pyrogram and PyTgCalls. Streams audio/video in Telegram voice chats, with group admin tools, queue management, and more.

## Stack
- **Language:** Python 3.12
- **Framework:** Pyrogram (Telegram bot) + PyTgCalls (voice chat streaming)
- **Database:** MongoDB (via Motor async driver)
- **Media:** yt-dlp, ffmpeg, Spotify API

## How to Run
The workflow `Start application` runs:
```
python3 -m SHUKLAMUSIC
```

## Required Secrets (Replit Secrets)
| Secret | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB connection string |
| `STRING_SESSION` | Pyrogram string session for the assistant/userbot account |
| `GIT_TOKEN` | GitHub personal access token (for git push via `/update`) |

## Required Env Vars (set in .replit)
| Variable | Description |
|---|---|
| `OWNER_ID` | Your Telegram user ID |
| `LOGGER_ID` | Telegram group/channel ID for bot logs |
| `LOG_GROUP_ID` | Same as LOGGER_ID (alias) |
| `UPSTREAM_REPO` | GitHub repo URL for `/update` command |
| `UPSTREAM_BRANCH` | Branch to pull from (default: `main`) |

## User Preferences
- Keep existing project structure intact
- GIT_TOKEN stored as secret for git push support
