# NOBITA X PRIME MUSIC BOT

A feature-rich Telegram Music Bot that streams YouTube music in group/channel voice chats, with moderation, fun commands, AI chatbot, and more.

## Stack

- **Language:** Python 3.12
- **Telegram framework:** kurigram (pyrogram fork — installed as `pyrogram`)
- **Voice calls:** py-tgcalls / PyTgCalls
- **Database:** MongoDB (via motor/pymongo)
- **Task scheduler:** APScheduler

## How to run

```
python3 -m SHUKLAMUSIC
```

Workflow `Start application` runs this automatically.

## Required secrets (set in Replit Secrets)

| Secret | Purpose |
|---|---|
| `BOT_TOKEN` | From @BotFather |
| `API_ID` | From my.telegram.org |
| `API_HASH` | From my.telegram.org |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram user session (assistant account for VC) |
| `LOGGER_ID` | Telegram chat ID for bot logs (bot must be admin there) |
| `SESSION_SECRET` | Random secret string |

## Optional secrets

| Secret | Purpose |
|---|---|
| `GROQ_API_KEY` | Enables AI chatbot mode |
| `GIT_TOKEN` | GitHub token for `/update` autopush command |

## Notes

- `kurigram` must be installed **without** standard `pyrogram` alongside it. kurigram is a drop-in fork that installs itself as the `pyrogram` package and adds `ButtonStyle` enum support.
- `LOGGER_ID` must be a valid Telegram chat ID (e.g. `-1001234567890`). The bot must be an admin in that group/channel before starting.
- `STRING_SESSION` is the Pyrogram string session for the assistant user account that joins voice chats.

## User preferences

- Wants GitHub autopush via `/update` command (GIT_TOKEN configured).
