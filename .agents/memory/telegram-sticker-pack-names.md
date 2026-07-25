---
name: Telegram sticker pack names
description: Telegram's strict short-name rules for sticker packs created by /kang.
---

Telegram sticker-set short names must start with a letter, use only letters,
numbers, and underscores, avoid consecutive underscores, stay within Telegram's
length limit, and end with `_by_<actual_bot_username>`. The username should
come from the running bot identity (`get_me()`/client username), not an
unvalidated configuration fallback.

**Why:** Telegram returns `PACK_SHORT_NAME_INVALID` when a configured username
contains invalid characters, is stale, or the required `_by_` suffix is not
formed exactly.

**How to apply:** Sanitize and truncate the username/prefix before
`CreateStickerSet`, and retry with a numbered pack name when a name is already
occupied or a previous pack is full.