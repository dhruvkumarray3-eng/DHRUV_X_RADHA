# NOBITA X PRIME Music Bot

A Telegram music bot that streams YouTube/Spotify/SoundCloud audio into Telegram voice chats. Includes an AI chatbot powered by Groq (LLaMA 3.3 70B).

## Stack
- **Python 3.12** — runtime
- **Pyrogram** — Telegram MTProto client (bot + userbot assistant)
- **PyTgCalls / NTgCalls** — voice chat streaming
- **yt-dlp** — YouTube audio/video downloading
- **MongoDB (Motor)** — async database
- **Groq** — AI chatbot
- **aiohttp** — built-in keep-alive web server on port 8080

## How to run
```
python3 -m SHUKLAMUSIC
```
Workflow: **Start application** (already configured)

## Required secrets (Replit Secrets)
| Key | Description |
|-----|-------------|
| `API_ID` | Telegram API ID from my.telegram.org |
| `API_HASH` | Telegram API Hash from my.telegram.org |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB connection string |
| `STRING_SESSION` | Pyrogram session string for the assistant userbot |
| `OWNER_ID` | Your Telegram user ID |
| `LOGGER_ID` | Log group/channel ID (negative number) |
| `GROQ_API_KEY` | Groq API key for AI chatbot |
| `GIT_TOKEN` | GitHub token for auto-updates |

## Keep-alive
The bot runs a lightweight HTTP server on port 8080. Ping `/ping` to keep it alive:
```
https://<your-replit-domain>/ping
```
Returns `{"status": "ok", "bot": "NOBITA X PRIME"}`.

## User preferences
- Keep the project's existing structure and stack — do not restructure or migrate it.
