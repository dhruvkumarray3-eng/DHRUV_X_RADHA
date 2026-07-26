# NOBITA X PRIME — Telegram Music Bot

A feature-rich Telegram Music Bot that streams YouTube audio into Telegram group voice chats using Pyrogram and py-tgcalls.

## How to run

```
python3 -m SHUKLAMUSIC
```

The **Start application** workflow runs this automatically on Replit.

## Required secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `API_ID` | Telegram API ID — from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API hash — from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Bot token — from [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram userbot string session — from [@StringFetchBot](https://t.me/StringFetchBot) |
| `LOGGER_ID` | Telegram group/channel ID where the bot sends startup logs |
| `OWNER_ID` | Your Telegram user ID |

## Optional secrets

| Secret | Description |
|---|---|
| `GIT_TOKEN` | GitHub personal access token — enables `/update` autopush to your fork |
| `GROQ_API_KEY` | Groq API key — enables AI chatbot mode |

## Key environment variables (set in Replit env)

| Variable | Default | Description |
|---|---|---|
| `UPSTREAM_REPO` | github.com/dhruvkumarray3-eng/DHRUV_X_RADHA | Repo for `/update` command |
| `UPSTREAM_BRANCH` | `main` | Branch to pull from |

## Tech stack

- **Python 3.12**
- **Pyrogram** — Telegram MTProto client
- **py-tgcalls / ntgcalls** — Voice chat streaming
- **yt-dlp** — YouTube audio downloading
- **Motor / MongoDB** — Async database
- **APScheduler** — Nightmode & cleanup jobs
- **Groq** — AI chatbot (optional)

## User preferences

- Keep existing project structure intact.
- GitHub auto-push via GIT_TOKEN is configured (used by `/update` command).
