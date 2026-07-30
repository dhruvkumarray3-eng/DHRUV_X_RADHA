# NOBITA X PRIME MUSIC BOT (SHUKLAMUSIC)

A Telegram music bot that streams audio/video in voice chats, with an AI chatbot powered by Groq.

## Stack
- **Python 3.12** — Pyrogram (MTProto), PyTgCalls (voice), Motor/MongoDB, yt-dlp, Groq LLaMA
- **MongoDB** — persistent storage (playlists, sudoers, settings, etc.)
- **Keep-alive server** — aiohttp on port 8080, `/ping` returns `{"status":"ok","bot":"NOBITA X PRIME"}`

## How to run
```
python3 -m SHUKLAMUSIC
```
Workflow: **Start application** (configured as console output)

## Required secrets (set in Replit Secrets)
| Key | Description |
|-----|-------------|
| `API_ID` | Telegram API ID (my.telegram.org) |
| `API_HASH` | Telegram API Hash |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB connection string |
| `STRING_SESSION` | Pyrogram userbot session string (for voice calls) |
| `OWNER_ID` | Your Telegram user ID |

## Optional secrets
| Key | Description |
|-----|-------------|
| `GROQ_API_KEY` | Groq API key for AI chatbot (LLaMA 3.3 70B) |
| `GIT_TOKEN` | GitHub token for git-based update commands |
| `STRING_SESSION2`–`STRING_SESSION7` | Additional assistant accounts |
| `HEROKU_API_KEY` / `HEROKU_APP_NAME` | Only needed if deploying to Heroku |
| `LOGGER_ID` / `LOG_GROUP_ID` | Telegram group ID for logging |

## Non-secret env vars (set in .replit userenv)
- `UPSTREAM_REPO` — GitHub repo for `/update` command
- `UPSTREAM_BRANCH` — branch to pull from (default: `main`)

## User preferences
- Keep existing project structure; do not restructure or migrate.
