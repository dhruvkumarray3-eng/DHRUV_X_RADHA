# NOBITA X PRIME MUSIC BOT

A feature-rich Telegram Music Bot that streams YouTube audio/video in group & channel voice chats. Built on Pyrogram + PyTgCalls.

## How to run

```
python3 -m SHUKLAMUSIC
```

The workflow **Start application** is configured and runs automatically when you press the Run button.

## Required secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `BOT_TOKEN` | From [@BotFather](https://t.me/BotFather) |
| `API_ID` | From [my.telegram.org](https://my.telegram.org) → Apps |
| `API_HASH` | From [my.telegram.org](https://my.telegram.org) → Apps |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `OWNER_ID` | Your Telegram numeric user ID |
| `STRING_SESSION` | Pyrogram session string for the VC assistant account |
| `LOGGER_ID` | Telegram group/channel ID for bot logs (use `0` to disable) |
| `GIT_TOKEN` | GitHub PAT — enables `/update` auto-push (optional) |

## Optional env vars (set in .replit `[userenv.shared]`)

| Variable | Default | Description |
|---|---|---|
| `UPSTREAM_REPO` | dhruvkumarray3-eng/DHRUV_X_RADHA | GitHub repo used by `/update` |
| `UPSTREAM_BRANCH` | `main` | Branch to pull/push |

## Stack

- **Python 3.12**
- **Pyrogram** — Telegram MTProto client
- **PyTgCalls / NTgCalls** — voice chat streaming
- **Motor / MongoDB** — async database
- **yt-dlp** — YouTube download backend
- **APScheduler** — nightmode & mongo-size jobs

## User preferences

- Keep the project's existing module structure (`SHUKLAMUSIC/` package).
- Do not migrate the database away from MongoDB.
