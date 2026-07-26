# SHUKLAMUSIC — Nobita X Prime Music Bot

A feature-rich Telegram Music Bot that streams YouTube audio in group/channel voice chats, with moderation, AI chatbot, welcome messages, and more.

## Tech Stack
- **Python 3.12**
- **Pyrogram** — Telegram MTProto client
- **py-tgcalls / ntgcalls** — Voice chat streaming
- **yt-dlp** — YouTube audio/video downloader
- **Motor / MongoDB** — Async database
- **APScheduler** — Nightmode & scheduled tasks
- **Groq LLaMA 3.3 70B** — AI chatbot engine
- **aiohttp** — Built-in keep-alive web server (port 8080)

## How to Run

```
python3 -m SHUKLAMUSIC
```

The workflow **"Start application"** handles this automatically.

## Required Secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `API_ID` | Telegram API ID from my.telegram.org |
| `API_HASH` | Telegram API Hash from my.telegram.org |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram userbot string session |
| `LOGGER_ID` | Telegram group/channel ID for logs |
| `OWNER_ID` | Your Telegram user ID |
| `GIT_TOKEN` | GitHub token for auto-push (optional) |
| `GROQ_API_KEY` | Groq API key for AI chatbot (optional) |

## Entry Points
- `SHUKLAMUSIC/__main__.py` — main startup (calls `init()`)
- `config.py` — all environment variable definitions
- `SHUKLAMUSIC/plugins/` — all bot command handlers

## User Preferences
- Keep Heroku-related code as-is (it gracefully no-ops on Replit)
- GIT_TOKEN and GROQ_API_KEY are configured for GitHub push and AI chatbot
