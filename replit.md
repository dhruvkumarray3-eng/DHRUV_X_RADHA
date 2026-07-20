# SHUKLAMUSIC — Telegram Music Bot

A Telegram group voice-chat music streaming bot built with Pyrogram and py-tgcalls.

## How to run

The workflow **"Start application"** runs the bot:

```
python3 -m SHUKLAMUSIC
```

## Required secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB connection string |
| `STRING_SESSION` | Pyrogram user session string (assistant account) |
| `GIT_TOKEN` | GitHub personal access token (for git push) |

## Required env vars (set in .replit userenv)

| Variable | Description |
|---|---|
| `LOGGER_ID` | Telegram group/channel ID for bot logs |
| `OWNER_ID` | Your Telegram user ID |

## Stack

- Python 3.12
- [Pyrogram](https://pyrogram.org/) — Telegram MTProto client
- [py-tgcalls](https://pytgcalls.github.io/) / ntgcalls — Voice chat streaming
- MongoDB / Motor — async database
- yt-dlp — YouTube audio/video download
- APScheduler — scheduled jobs (night mode, etc.)

## User preferences

- Credentials stored securely as Replit Secrets, never hardcoded
