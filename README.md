<div align="center">

<img src="https://files.catbox.moe/ky6ln3.jpg" width="200" height="200" style="border-radius:50%"/>

# 🎵 NOBITA X PRIME MUSIC BOT

**A powerful, feature-rich Telegram Music Bot — stream YouTube music directly in your group & channel voice chats.**

[![Telegram](https://img.shields.io/badge/Support-Telegram-blue?logo=telegram)](https://t.me/II_NOBITA_X_PRIME_II)
[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-Educational-orange)](#license)
[![Uptime](https://img.shields.io/badge/Uptime-24%2F7-green)](#uptime-monitoring)

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
| 🌐 Multilingual | 180+ country language support, auto-detected per group |
| 🤖 ChatBot | Groq AI chatbot — human-like replies in any language |
| 📡 Traffic Control | Owner-only remote flood guard & rate limiter |
| 💓 Uptime | Built-in `/ping` endpoint for 24/7 uptime monitoring |

---

## 🚀 Deployment

### Prerequisites

| Requirement | Where to get |
|---|---|
| `API_ID` | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | [MongoDB Atlas](https://cloud.mongodb.com) |
| `STRING_SESSION` | [@StringFetchBot](https://t.me/StringFetchBot) or `/genstring` |
| `LOGGER_ID` | Your Telegram group/channel ID |
| `OWNER_ID` | Your Telegram user ID |

### Deploy on Replit *(Recommended)*

1. Import this repo into Replit.
2. Go to **Tools → Secrets** and add:

```
API_ID           = your telegram api id
API_HASH         = your telegram api hash
BOT_TOKEN        = your bot token
MONGO_DB_URI     = your mongodb atlas uri
STRING_SESSION   = your pyrogram string session
LOGGER_ID        = your logger group/channel id
OWNER_ID         = your telegram user id
```

3. **Optional but recommended:**

```
GIT_TOKEN        = github personal access token (for /update autopush)
GROQ_API_KEY     = groq api key (for AI chatbot)
```

4. Click **Run** — the bot starts automatically.

### Deploy on VPS / Railway

```bash
git clone https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA
cd DHRUV_X_RADHA
pip3 install -r requirements.txt
cp .env.example .env   # fill in your values
python3 -m SHUKLAMUSIC
```

---

## 💓 Uptime Monitoring

The bot runs a built-in HTTP server on port **8080**.

Use the following URL in [UptimeRobot](https://uptimerobot.com), [BetterStack](https://betterstack.com), or any uptime monitor:

```
https://<your-replit-app-name>.<your-username>.repl.co/ping
```

> **How to find your URL:** In Replit, click **Webview** (the browser icon) → copy the URL shown → append `/ping`.

Set the monitor to ping every **5 minutes**. This keeps the bot alive 24/7 on Replit's free tier.

---

## 🌐 Language System (180+ Countries)

Every group can set its own language:

```
/lang              → show all 17 supported languages
/lang hindi        → search by language name
/lang india        → search by country name
/lang russia       → set Russian (Русский)
/lang arabic       → set Arabic
```

**Supported languages:** English, Hindi, Arabic, Russian, French, Spanish, Turkish, Indonesian, Bengali, Punjabi, Telugu, Tamil, Marathi, Gujarati, Malayalam, Kannada, Urdu — with 180+ country→language mappings.

When a language is set, **all bot messages** (including "Powered by" and start messages) are shown in that language.

---

## 🤖 AI ChatBot

Powered by **Groq LLaMA 3.3 70B** — responds like a real human friend.

```
/chatbot on        → enable in your group
/chatbot off       → disable
/chatbot status    → check current status
/teach hi | Hello! → teach a keyword reply
/unlearn hi        → forget a keyword
/learned           → list all keywords
/chatbothelp       → full help
```

**Owner-only — User Profiles (AI memory for specific users):**

```
/addprofile @username This is my best friend Rahul, he loves cricket
/delprofile @username
/profiles
```

When a user with a saved profile chats with the bot, the AI automatically uses that context for personalised replies.

---

## 📡 Traffic Control *(Owner Only)*

Protect your groups from Telegram flood limits:

```
/traffic                      → stats for current chat
/traffic global               → stats for all chats
/traffic <chat_id>            → stats for specific chat
/floodctrl on                 → enable flood guard (this chat)
/floodctrl on <chat_id>       → enable remotely
/floodctrl off <chat_id>      → disable remotely
/setflood 20 60               → max 20 msg per 60 seconds
/setfloodaction warn|slow     → action when limit hit
```

---

## 🔄 Auto-Update via GitHub

If `GIT_TOKEN` is set, use `/update` to:
1. Pull latest code from `UPSTREAM_REPO`
2. Push changes to your GitHub fork
3. Restart the bot automatically

Environment variables for update:

```
UPSTREAM_REPO    = https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA
UPSTREAM_BRANCH  = main
GIT_TOKEN        = your github personal access token
```

---

## 🎵 Music Features

### Autoplay (YouTube Radio)

```
/autoplay    → toggle on/off
```

When ON, the bot auto-fetches related songs from YouTube Radio when the queue ends — streams indefinitely.

### Channel Play Setup

1. Add the bot to your **channel** as admin
2. Add the bot to your **group** as admin
3. In the group, use `/channelplay` to link the channel
4. Play music — streams to the **channel's voice chat**

### Commands

| Command | Description |
|---|---|
| `/play <song>` | Play audio in voice chat |
| `/vplay <song>` | Play video in voice chat |
| `/pause` | Pause stream |
| `/resume` | Resume stream |
| `/skip` | Skip to next track |
| `/stop` / `/end` | Stop and clear queue |
| `/queue` | View current queue |
| `/loop enable/disable` | Loop current track |
| `/shuffle` | Shuffle queue |
| `/seek <seconds>` | Seek forward |
| `/seekback <seconds>` | Seek backward |
| `/song <name>` | Download MP3/MP4 |

---

## 🛡️ Owner Commands

| Command | Description |
|---|---|
| `/addsudo @user` | Add sudo user |
| `/delsudo @user` | Remove sudo user |
| `/sudolist` | View sudo list (owner only) |
| `/broadcast <msg>` | Broadcast to all chats |
| `/gban @user` | Global ban |
| `/ungban @user` | Remove global ban |
| `/maintenance enable/disable` | Toggle maintenance mode |
| `/logs` | Get bot logs |
| `/traffic` | Traffic control panel |
| `/addprofile @user <info>` | Add AI user profile |
| `/update` | Pull latest code & restart |

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `API_ID` | ✅ | — | Telegram API ID |
| `API_HASH` | ✅ | — | Telegram API Hash |
| `BOT_TOKEN` | ✅ | — | Bot Token |
| `MONGO_DB_URI` | ✅ | — | MongoDB connection string |
| `STRING_SESSION` | ✅ | — | Pyrogram userbot session |
| `LOGGER_ID` | ✅ | — | Log group/channel ID |
| `OWNER_ID` | ✅ | `6670240589` | Bot owner's Telegram ID |
| `GIT_TOKEN` | ⚙️ | — | GitHub token for auto-push |
| `GROQ_API_KEY` | ⚙️ | — | Groq API key for AI chatbot |
| `DURATION_LIMIT` | ⚙️ | `17000` | Max song duration (minutes) |
| `SUPPORT_CHANNEL` | ⚙️ | Nobita channel | Support channel URL |
| `SUPPORT_CHAT` | ⚙️ | Nobita group | Support group URL |

---

## 📚 Tech Stack

- **Python 3.12**
- **Pyrogram** — Telegram MTProto client
- **py-tgcalls / ntgcalls** — Voice chat streaming engine
- **yt-dlp** — YouTube audio/video downloader
- **Motor / MongoDB** — Async database
- **APScheduler** — Nightmode & scheduled tasks
- **Groq LLaMA 3.3 70B** — AI chatbot engine
- **aiohttp** — Built-in keep-alive web server

---

## 📜 License

Based on [StrangerMusic](https://github.com/itzshukla) and [ShrutiMusic](https://github.com/NoxxOP/ShrutiMusic).  
Open for **educational and non-commercial use only**.  
You must retain all credit headers in source files.  
Commercial use or removal of credits is **strictly prohibited**.

---

<div align="center">

**Made with ❤️ — Powered by NOBITA X PRIME**

[![Channel](https://img.shields.io/badge/Updates-Channel-blue?logo=telegram)](https://t.me/II_NOBITA_X_PRIME_II)

</div>
