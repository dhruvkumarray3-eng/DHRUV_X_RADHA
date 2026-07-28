# NOBITA X PRIME MUSIC BOT

A Telegram music bot that streams YouTube, Spotify, SoundCloud, and Apple Music into Telegram voice chats. Includes a Groq-powered AI chatbot, MongoDB persistence, and a keep-alive web server.

## Stack

- **Python 3.12** — main runtime
- **Pyrogram** — Telegram MTProto client (bot + userbot assistant)
- **PyTgCalls / ntgcalls** — voice chat streaming
- **yt-dlp** — YouTube/audio downloading
- **Motor (MongoDB)** — async database via MongoDB Atlas
- **Groq (LLaMA 3.3 70B)** — AI chatbot
- **aiohttp** — keep-alive web server on port 8080

## How to run

```
python3 -m SHUKLAMUSIC
```

The workflow **Start application** handles this automatically.

## Required secrets (Replit Secrets)

| Key | Description |
|-----|-------------|
| `API_HASH` | Telegram API hash from my.telegram.org |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram session string for the userbot assistant |
| `GROQ_API_KEY` | Groq API key for AI chatbot |
| `GIT_TOKEN` | GitHub token for auto-update feature |

## Environment variables (already set)

| Key | Value |
|-----|-------|
| `API_ID` | 38987335 |
| `OWNER_ID` | 8245258112 |
| `LOGGER_ID` | -1004458016685 |
| `LOG_GROUP_ID` | -1004458016685 |
| `UPSTREAM_REPO` | https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA |
| `UPSTREAM_BRANCH` | main |

## Keep-alive endpoint

The bot exposes a `/ping` endpoint on port 8080:
```
GET https://<your-replit-domain>/ping
→ {"status": "ok", "bot": "NOBITA X PRIME"}
```
Use this with UptimeRobot or BetterUptime to keep the bot alive 24/7.

## User preferences

- Keep the project's existing structure and stack.
