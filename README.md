<div align="center">

<img src="https://files.catbox.moe/ky6ln3.jpg" width="200" height="200" style="border-radius:50%"/>

# 🎵 NOBITA X PRIME MUSIC BOT

**A powerful, feature-rich Telegram Music Bot — stream YouTube music directly in your group & channel voice chats.**

[![Telegram](https://img.shields.io/badge/Support-Telegram-blue?logo=telegram)](https://t.me/II_NOBITA_X_PRIME_II)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-Educational-orange)](#license)

</div>

---

## ✨ Features

| Category | Features |
|---|---|
| 🎵 Music | Play, Pause, Resume, Skip, Stop, Seek, Loop, Shuffle |
| 📻 Autoplay | YouTube Radio — auto-queues related songs when queue ends |
| 📢 Channel Play | Link a channel to your group for VC streaming |
| 🛡️ Moderation | Ban, Mute, Kick, Warn, Promote, Demote, Purge |
| 📌 Tags | TagAll, HiTag, GmTag, LifeTag, Mention |
| 👋 Welcome | Custom welcome messages & nightmode auto-lock |
| 💑 Fun | Couple of the Day, Truth & Dare, Group Games |
| 📋 Utility | Notes, Filters, AFK, User Info, Crypto & UPI tools |
| 🔊 VC Logger | Log VC join/leave events to a dedicated chat |
| 🌐 Multilingual | Language support per group |
| 🤖 ChatBot | Integrated AI chat mode |

---

## 🚀 Deployment

### Prerequisites

| Requirement | Where to get |
|---|---|
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | [MongoDB Atlas](https://cloud.mongodb.com) |
| `STRING1` | Generate via `/genstring` command or [@StringFetchBot](https://t.me/StringFetchBot) |
| `SESSION_SECRET` | Any random secret string |

### Deploy on Replit

1. Fork this repo or import it to Replit.
2. Add the following **Secrets** in Replit → Tools → Secrets:

```
BOT_TOKEN       = your bot token
MONGO_DB_URI    = your MongoDB URI
STRING1         = your Pyrogram string session
SESSION_SECRET  = any random string
```

3. Click **Run** — the workflow `Start application` will launch automatically.

### Deploy on VPS / Railway

```bash
git clone https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA
cd DHRUV_X_RADHA
pip3 install -r requirements.txt
cp .env.example .env   # fill in your values
python3 -m SHUKLAMUSIC
```

---

## ⚙️ Configuration

Edit `config.py` or set the following environment variables:

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | ✅ | Telegram Bot Token |
| `MONGO_DB_URI` | ✅ | MongoDB connection URI |
| `STRING1` | ✅ | Pyrogram assistant session string |
| `SESSION_SECRET` | ✅ | Flask/webhook session secret |
| `OWNER_ID` | ✅ | Your Telegram user ID |
| `OWNER_USERNAME` | ✅ | Your Telegram username (without @) |
| `SUPPORT_CHAT` | ✅ | Support group username |
| `LOG_GROUP_ID` | ✅ | Chat ID for bot logs |
| `UPSTREAM_REPO` | ✅ | GitHub repo URL for `/update` |
| `GITHUB_TOKEN` | ⭐ | GitHub PAT for auto-push via `/update` |
| `API_URL` | ❌ | External download API (default: ShrutiBots) |
| `API_KEY` | ❌ | API key for external download API |

---

## 📋 Commands

### 🎵 Music

| Command | Description |
|---|---|
| `/play [song]` | Play a song in VC |
| `/cplay [song]` | Play in linked channel VC |
| `/vplay [song]` | Play video in VC |
| `/pause` | Pause the stream |
| `/resume` | Resume the stream |
| `/skip` | Skip to next track |
| `/stop` | Stop and leave VC |
| `/seek [seconds]` | Seek forward/backward |
| `/loop [count]` | Loop current track |
| `/shuffle` | Shuffle the queue |
| `/queue` | Show current queue |
| `/autoplay` | Toggle YouTube autoplay |
| `/song [name]` | Download song as file |

### 🛡️ Moderation

| Command | Description |
|---|---|
| `/ban` | Ban a user |
| `/unban` | Unban a user |
| `/mute` | Mute a user |
| `/unmute` | Unmute a user |
| `/tmute [time]` | Temporarily mute |
| `/kick` | Kick a user |
| `/promote` | Promote to admin |
| `/demote` | Demote admin |
| `/warn` | Warn a user (3 warns = ban) |
| `/purge` | Purge messages |

### 📌 Tags

| Command | Description |
|---|---|
| `/tagall` | Tag all members |
| `/admintag` | Tag all admins |
| `/hitag` | Tag one-by-one with delay |
| `/mention [msg]` | Tag all with custom message |
| `/cancel` | Stop ongoing tag |

### 🔧 Settings & Tools

| Command | Description |
|---|---|
| `/settings` | Open bot settings panel |
| `/channelplay` | Link channel to group |
| `/welcome on/off` | Toggle welcome message |
| `/nightmode on/off` | Toggle night auto-lock |
| `/afk [reason]` | Set AFK status |
| `/info` | Get user info |
| `/id` | Get user/chat ID |
| `/truth` | Random truth question |
| `/dare` | Random dare challenge |
| `/couples` | Couple of the day |
| `/ton` | Live TON price |
| `/usdt` | Live USDT price |
| `/balance [wallet]` | TON wallet balance |
| `/setupi [upi-id]` | Save UPI ID |
| `/gen [amount]` | Generate UPI QR code |
| `/vclogger on/off` | Toggle VC logging |

### 📝 Notes & Filters

| Command | Description |
|---|---|
| `/save [name] [content]` | Save a note |
| `/get [name]` or `#name` | Get a note |
| `/notes` | List all notes |
| `/filter [keyword]` | Set auto-reply filter |
| `/filters` | List all filters |
| `/stopfilter [keyword]` | Remove a filter |

### 👑 Sudo Only

| Command | Description |
|---|---|
| `/broadcast` | Broadcast to all chats |
| `/gban` | Globally ban a user |
| `/update` | Pull latest code from GitHub & restart |
| `/logs` | Get bot logs |
| `/stats` | Bot statistics |
| `/maintenance on/off` | Toggle maintenance mode |

---

## 🤖 Autoplay (YouTube Radio)

When autoplay is enabled (`/autoplay`), once the queue runs out the bot automatically fetches a **related song** from YouTube's Radio/Mix system — the same technology YouTube uses for autoplay. No manual searching required.

```
/autoplay    → toggle on/off
```

When ON, the bot will:
1. Detect when the queue is about to end
2. Fetch a related song from YouTube Radio (`RD{videoId}`)
3. Automatically queue and stream it
4. Continue indefinitely until stopped

---

## 📢 Channel Play Setup

1. Add the bot to your **channel** as admin
2. Add the bot to your **group** as admin  
3. In the group, use `/channelplay` to link the channel
4. Play music in the group — it streams to the **channel's voice chat**

---

## 🔄 Auto-Update via GitHub

If `GITHUB_TOKEN` is set, the `/update` command will:
1. Pull latest code from `UPSTREAM_REPO`
2. Push any local changes to your GitHub fork
3. Restart the bot automatically

---

## 📜 License

This project is based on [StrangerMusic](https://github.com/itzshukla) and [ShrutiMusic](https://github.com/NoxxOP/ShrutiMusic).  
Open for **educational and non-commercial use only**.  
You must retain all credit headers in source files.  
Commercial use or removal of credits is **strictly prohibited**.

---

<div align="center">

**Made with ❤️ — Powered by NOBITA X PRIME**

[![Channel](https://img.shields.io/badge/Updates-Channel-blue?logo=telegram)](https://t.me/II_NOBITA_X_PRIME_II)

</div>
