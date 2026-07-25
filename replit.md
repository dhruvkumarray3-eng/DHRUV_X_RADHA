# NOBITA X PRIME MUSIC BOT

A powerful Telegram Music Bot that streams YouTube audio into Telegram group voice chats, with moderation, welcome messages, games, and more.

## How to Run

The bot starts automatically via the **Start application** workflow:

```
python3 -m SHUKLAMUSIC
```

## Required Secrets

Set these in Replit → Tools → Secrets:

| Secret | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram string session (via @StringFetchBot) |
| `LOGGER_ID` | Telegram chat ID for bot logs |
| `SESSION_SECRET` | Random secret string |
| `GIT_TOKEN` | GitHub personal access token (for `/update` auto-push) |

## Stack

- **Python 3.12**
- **Pyrogram** — Telegram bot framework
- **py-tgcalls / PyTgCalls** — Voice chat streaming
- **Motor / PyMongo** — MongoDB async driver
- **yt-dlp** — YouTube audio download
- **APScheduler** — Scheduled tasks (nightmode, etc.)

## Configuration

All config is in `config.py` — reads from environment variables with sensible defaults. Key optional vars:

- `OWNER_ID` — your Telegram user ID
- `UPSTREAM_REPO` — GitHub repo for `/update` command
- `LOGGER_ID` — group/channel for VC and bot event logs

## User Preferences

- Keep existing project structure; do not migrate or restructure.
- GIT_TOKEN is set for GitHub auto-push via the `/update` command.
