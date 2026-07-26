<div align="center">

<img src="https://files.catbox.moe/ky6ln3.jpg" width="200" height="200" style="border-radius:50%"/>

# 🎵 NOBITA X PRIME MUSIC BOT

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&pause=1000&color=FF6B6B&center=true&vCenter=true&width=600&lines=🎵+Nobita+X+Prime+Music+Bot;🚀+Stream+YouTube+in+Voice+Chats;🤖+Groq+AI+ChatBot+Powered;🎶+Auto-Play+%7C+Skip+%7C+Back+%7C+Pause;24%2F7+Music+%7C+Always+On" alt="Typing SVG" />
</p>

<p align="center">
  <a href="https://t.me/II_NOBITA_X_PRIME_II">
    <img src="https://img.shields.io/badge/Channel-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&labelColor=0A0A0A" alt="Telegram Channel"/>
  </a>
  <a href="https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA">
    <img src="https://img.shields.io/github/stars/dhruvkumarray3-eng/DHRUV_X_RADHA?style=for-the-badge&logo=github&color=FFD700&labelColor=0A0A0A" alt="Stars"/>
  </a>
  <a href="https://github.com/dhruvkumarray3-eng/DHRUV_X_RADHA/fork">
    <img src="https://img.shields.io/github/forks/dhruvkumarray3-eng/DHRUV_X_RADHA?style=for-the-badge&logo=git&color=FF6B6B&labelColor=0A0A0A" alt="Forks"/>
  </a>
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0A0A0A" alt="Python"/>
  <img src="https://img.shields.io/badge/License-Educational-orange?style=for-the-badge&labelColor=0A0A0A" alt="License"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/▶%20Play-Music-00C851?style=flat-square&labelColor=1a1a1a" />
  <img src="https://img.shields.io/badge/⏸%20Pause-Resume-2196F3?style=flat-square&labelColor=1a1a1a" />
  <img src="https://img.shields.io/badge/⏭%20Skip-Next-9C27B0?style=flat-square&labelColor=1a1a1a" />
  <img src="https://img.shields.io/badge/⏮%20Back-Previous-FF5722?style=flat-square&labelColor=1a1a1a" />
  <img src="https://img.shields.io/badge/🤖%20AI-ChatBot-FF6B6B?style=flat-square&labelColor=1a1a1a" />
</p>

</div>

---

## ✨ Features

<table>
<tr>
<td>

| 🎵 Music Controls | Description |
|---|---|
| ▶️ Play | YouTube, Spotify, Apple Music, SoundCloud |
| ⏸ Pause / ▶ Resume | Inline buttons on every Now Playing card |
| ⏭ Skip / Next | Skip current — queue advances automatically |
| ⏮ Back / Previous | Return to the song that was just playing |
| 🔁 Autoplay | Auto-queues related songs when queue ends |
| 🔄 Loop | Loop current track N times |
| ⚡ Seek | Jump to any timestamp |

</td>
<td>

| 🛡️ Admin Tools | Description |
|---|---|
| 📊 Moderation | Ban, Mute, Kick, Warn, Promote |
| 📌 TagAll | Mention all members |
| 👋 Welcome | Custom welcome messages |
| 🌙 Nightmode | Auto-lock at night |
| 💑 Fun | Couple of the Day, Games |
| 📋 Notes & Filters | Group note system |
| 🔊 VC Logger | Log VC events |

</td>
</tr>
</table>

| 🤖 ChatBot (Groq AI) | Features |
|---|---|
| Auto-reply | Turns on per-group with `/chatbot on` (admin only) |
| User Profiles | Admins save user info: `/addprofile @user info` — bot remembers them |
| Smart Lookup | Ask about a saved user by @mention, ID, or name — bot replies with saved info |
| Keyword Mode | Teach custom replies: `/teach keyword \| response` |
| Language | Detects and replies in any language |

---

## 🎮 Now Playing Buttons

Every music card shows these inline buttons:

```
[ ⏮ Back ]  [ ⏸ Pause ]  [ ▶ Resume ]  [ ⏭ Skip ]
[    ⏹ Stop    ] [  ❤️‍🔥 Autoplay  ]
[ 🎵 Audio ] [ 🎬 Video ]
[ ✨ Update ] [ 🌹 Support ]
```

> Works in both **regular play** and **autoplay** mode.
> **Back** button plays the previously played song from history.
> **Skip** in autoplay mode queues the next related YouTube song automatically.

---

## 🚀 Deployment — Deploy on Replit

[![Run on Replit](https://img.shields.io/badge/Run%20on-Replit-667881?style=for-the-badge&logo=replit&logoColor=white)](https://replit.com)

1. Import this repo into Replit.
2. Go to **Tools → Secrets** and add the required variables (see below).
3. Hit **Run** — the workflow starts automatically.

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `API_ID` | ✅ | — | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | — | Telegram API Hash |
| `BOT_TOKEN` | ✅ | — | Bot token from [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | ✅ | — | MongoDB Atlas connection string |
| `STRING_SESSION` | ✅ | — | Pyrogram userbot session |
| `LOGGER_ID` | ✅ | — | Log group/channel ID |
| `OWNER_ID` | ✅ | `6670240589` | Your Telegram user ID |
| `GIT_TOKEN` | ⚙️ | — | GitHub token for `/update` auto-push |
| `GROQ_API_KEY` | ⚙️ | — | Groq API key for AI chatbot |
| `UPSTREAM_REPO` | ⚙️ | This repo | GitHub repo URL for updates |
| `UPSTREAM_BRANCH` | ⚙️ | `main` | Branch to pull updates from |
| `DURATION_LIMIT` | ⚙️ | `17000` | Max song duration (minutes) |
| `SUPPORT_CHANNEL` | ⚙️ | Nobita channel | Support channel URL |
| `SUPPORT_CHAT` | ⚙️ | Nobita group | Support group URL |

---

## 💡 ChatBot Usage

```
/chatbot on          — Enable AI chatbot in this group (admin)
/chatbot off         — Disable chatbot
/chatbot status      — Check current status
/addprofile @user info about them    — Save user profile for AI memory
/delprofile @user    — Remove saved profile
/profiles            — List all saved profiles
/teach keyword | reply               — Teach keyword response
/unlearn keyword     — Forget a keyword
/learned             — List all learned keywords
/chatbothelp         — Show full help
```

---

## 📚 Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pyrogram-MTProto-00AFF0?style=flat-square&logo=telegram" />
  <img src="https://img.shields.io/badge/PyTgCalls-VoiceChat-9C27B0?style=flat-square" />
  <img src="https://img.shields.io/badge/yt--dlp-Downloader-FF0000?style=flat-square&logo=youtube&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB-Motor-47A248?style=flat-square&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=flat-square" />
  <img src="https://img.shields.io/badge/aiohttp-KeepAlive-009688?style=flat-square" />
</p>

---

## 🔗 Uptime Monitoring

The bot runs a built-in keep-alive web server. You can use this `/ping` endpoint with any uptime monitor (UptimeRobot, BetterUptime, etc.):

```
https://<your-replit-domain>/ping
```

Returns `{"status": "ok", "bot": "NOBITA X PRIME"}` when the bot is alive.

---

## 📜 License

Based on [StrangerMusic](https://github.com/itzshukla) and [ShrutiMusic](https://github.com/NoxxOP/ShrutiMusic).  
Open for **educational and non-commercial use only**.  
You must retain all credit headers in source files.  
Commercial use or removal of credits is **strictly prohibited**.

---

<div align="center">

**Made with ❤️ — Powered by NOBITA X PRIME**

[![Channel](https://img.shields.io/badge/Updates-@II__NOBITA__X__PRIME__II-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/II_NOBITA_X_PRIME_II)

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer&animation=twinkling" width="100%"/>

</div>
