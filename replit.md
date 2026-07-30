# NOBITA X PRIME Music Bot

A Telegram music bot that streams YouTube audio in group voice chats, with Groq AI chatbot, Spotify/SoundCloud support, and an assistant userbot.

## Stack

- **Python 3.12** — Pyrogram (MTProto), PyTgCalls (voice chat), yt-dlp (download), Motor/MongoDB (database)
- **AI** — Groq LLaMA 3.3 70B for chatbot replies
- **Audio pipeline** — ShrutiAPI (primary) → yt-dlp fallback → ffmpeg WAV conversion → pytgcalls stream

## How to run

```
python3 -m SHUKLAMUSIC
```

The workflow "Start application" is already configured and will start it automatically.

## Required secrets (set as Replit Secrets)

| Key | Description |
|---|---|
| `API_HASH` | Telegram API hash from my.telegram.org |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `GROQ_API_KEY` | Groq API key (AI chatbot) |
| `GIT_TOKEN` | GitHub token (auto-update) |
| `STRING_SESSION` | Pyrogram string session (assistant userbot) |

## Required env vars (set via Replit env vars)

| Key | Description |
|---|---|
| `API_ID` | Telegram API ID from my.telegram.org |
| `OWNER_ID` | Your Telegram user ID |
| `LOGGER_ID` | Telegram group ID for bot logs |

## yt-dlp anti-bot configuration

All yt-dlp calls use `player_client: [android, ios]` with `skip: [webpage, configs]` to bypass YouTube bot-detection. Cookies are loaded automatically if `cookies.txt` exists in the project root or `SHUKLAMUSIC/assets/cookies.txt`.

## User preferences

- Keep yt-dlp at `>=2026.06.09` in requirements.txt
- Always use `android`/`ios` player clients for yt-dlp, never `android_embedded`/`web_creator`
- Cookie file: check root `cookies.txt` first, then `SHUKLAMUSIC/assets/cookies.txt`
