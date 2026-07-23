# NOBITA X PRIME Music Bot

A feature-rich Telegram Music Bot that streams YouTube music directly into group and channel voice chats. Built on Pyrogram + PyTgCalls.

## How to run

```
python3 -m SHUKLAMUSIC
```

The **Start application** workflow runs this automatically on startup.

## Required Secrets (Replit → Tools → Secrets)

| Secret | Description |
|---|---|
| `BOT_TOKEN` | From [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram string session for assistant account |
| `SESSION_SECRET` | Any random string (already set) |
| `GIT_TOKEN` | GitHub personal access token (for `/update` auto-push) |

## Stack

- **Python 3.12**
- **Pyrogram** — Telegram MTProto client (bot)
- **PyTgCalls / ntgcalls** — Voice chat streaming
- **MongoDB / Motor** — Async database
- **yt-dlp** — YouTube audio downloading
- **APScheduler** — Scheduled tasks (nightmode, DB cleanup)

## Key configuration

Edit `config.py` or set environment variables for optional tuning:

- `LOGGER_ID` — Telegram chat ID for bot logs
- `OWNER_ID` — Your Telegram user ID
- `DURATION_LIMIT` — Max song duration in minutes (default: 17000)
- `UPSTREAM_REPO` / `GIT_TOKEN` — GitHub repo for `/update` auto-push

## User preferences

- GitHub token (`GIT_TOKEN`) should be set so every code change can be auto-pushed via the `/update` command.
