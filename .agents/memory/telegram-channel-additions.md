---
name: Telegram channel additions
description: Telegram update behavior relevant to channel bot installation and setup flows.
---

Telegram channel bot installations may arrive as `my_chat_member` updates rather than `new_chat_members` messages. Treat the membership update as the reliable trigger for an in-channel setup message and an attempted private greeting to the installer.

**Why:** Channels do not consistently emit the same service message shape as groups, so a group-only add handler can miss the person who installed the bot.

**How to apply:** Keep channel-install handling separate from ordinary group welcome handling, and use a deep link that preserves the channel ID through the group setup flow.