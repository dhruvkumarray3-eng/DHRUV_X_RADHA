# NOBITA X PRIME Music Bot

A feature-rich Telegram Music Bot that streams YouTube music in group/channel voice chats, built on Pyrogram + PyTgCalls.

## How to run

```
python3 -m SHUKLAMUSIC
```

The **Start application** workflow runs this automatically.

## Required secrets (set in Replit Secrets)

| Secret | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram string session for the assistant account (needed for VC streaming) |
| `SESSION_SECRET` | Any random string (already set) |
| `GIT_TOKEN` | GitHub token for `/update` autopush command |

## Optional env vars (set in .replit [userenv.shared])

| Key | Default / Current |
|---|---|
| `OWNER_ID` | 8245258112 |
| `LOGGER_ID` | -1004458016685 (log group) |
| `LOG_GROUP_ID` | -1004458016685 |
| `UPSTREAM_REPO` | https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA |
| `UPSTREAM_BRANCH` | main |

## Stack

- **Python 3.12** + Pyrogram + PyTgCalls
- **MongoDB** (via Motor async driver)
- **yt-dlp** for YouTube audio/video fetching
- **APScheduler** for nightmode & MongoDB size checks
- **Heroku3, GitPython** for deployment/update features

## User preferences

- Include GIT_TOKEN when collecting secrets for this project (for `/update` autopush).
