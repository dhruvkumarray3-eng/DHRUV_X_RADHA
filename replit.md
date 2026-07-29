# NOBITA X PRIME Music Bot (SHUKLAMUSIC)

A Telegram voice-chat music bot built with Pyrogram, PyTgCalls, yt-dlp, MongoDB, and Groq AI.

## How to run

```
python3 -m SHUKLAMUSIC
```

The "Start application" workflow runs this automatically.

## Required secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `API_ID` | Telegram API ID from https://my.telegram.org |
| `API_HASH` | Telegram API Hash from https://my.telegram.org |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `LOGGER_ID` | Telegram group/channel ID for bot logs (negative number) |
| `OWNER_ID` | Owner's Telegram user ID |
| `STRING_SESSION` | Pyrogram session string for the userbot (joins voice chats) |

## Optional secrets

| Secret | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for the AI chatbot feature (LLaMA 3.3 70B) |
| `GIT_TOKEN` | GitHub token for auto-update (`/update` command) |
| `STRING_SESSION2`–`STRING_SESSION7` | Additional userbot session strings |

## Keep-alive endpoint

The bot runs a lightweight HTTP server on port 8080. Use `/ping` with an uptime monitor (e.g. UptimeRobot) to keep the bot alive:

```
https://<your-replit-domain>/ping
```

Returns `{"status": "ok", "bot": "NOBITA X PRIME"}`.

## User preferences

<!-- Add user preferences here -->
