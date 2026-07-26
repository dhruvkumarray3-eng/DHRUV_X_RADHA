# -----------------------------------------------
# 🔸 Song History — per-chat last-played stack
# Stores recently played songs so the Back button can replay them.
# -----------------------------------------------

_MAX_HISTORY = 6
_history: dict[int, list] = {}


def push_history(chat_id: int, song: dict) -> None:
    """Push a completed song into this chat's history stack."""
    if not song:
        return
    h = _history.setdefault(chat_id, [])
    # Avoid double-pushing the exact same song back-to-back
    if h and h[-1].get("vidid") == song.get("vidid") and h[-1].get("file") == song.get("file"):
        return
    h.append(dict(song))
    if len(h) > _MAX_HISTORY:
        h.pop(0)


def pop_history(chat_id: int) -> dict | None:
    """Pop the most recently played song from history (returns None if empty)."""
    h = _history.get(chat_id)
    if h:
        return h.pop()
    return None


def peek_history(chat_id: int) -> dict | None:
    """Peek at the most recent history entry without removing it."""
    h = _history.get(chat_id)
    return h[-1] if h else None


def clear_history(chat_id: int) -> None:
    _history.pop(chat_id, None)
