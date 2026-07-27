# NOBITA X PRIME — Telegram Music Bot

A Telegram music/voice-chat bot with AI chatbot, MongoDB persistence, and a built-in keep-alive web server.

## Stack
- **Python 3.12** + Pyrogram (MTProto bot client)
- **PyTgCalls / ntgcalls** — voice chat streaming
- **yt-dlp** — YouTube/Spotify/SoundCloud audio download
- **Motor / MongoDB** — async database
- **Groq LLaMA 3.3 70B** — AI chatbot
- **aiohttp** — keep-alive web server (port 8080 → external port 80)

## How to run
```
python3 -m SHUKLAMUSIC
```
The workflow **Start application** handles this automatically.

## Required secrets (set in Replit Secrets)
| Key | Purpose |
|---|---|
| `API_ID` | Telegram API ID |
| `API_HASH` | Telegram API Hash |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB connection string |
| `LOGGER_ID` | Telegram chat ID for bot logs |
| `OWNER_ID` | Telegram user ID of bot owner |
| `STRING_SESSION` | Pyrogram session for assistant/userbot |
| `GROQ_API_KEY` | Groq AI chatbot (optional) |
| `GIT_TOKEN` | GitHub token for push support (optional) |

## Keep-alive endpoint
The bot runs an HTTP server at port 8080. Hit `/ping` to keep it alive:
```
GET https://<your-replit-domain>/ping
→ {"status": "ok", "bot": "NOBITA X PRIME"}
```

## Entry point
`SHUKLAMUSIC/__main__.py` — starts keep-alive server, loads all plugin modules, starts bot + userbot + PyTgCalls.

## Config
`config.py` at project root — reads all secrets from environment variables via `python-dotenv`.

## User preferences
