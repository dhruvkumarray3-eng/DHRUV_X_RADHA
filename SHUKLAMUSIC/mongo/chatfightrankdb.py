from datetime import datetime, timezone
from SHUKLAMUSIC.utils.mongo import db

cfr_col = db.chatfightrank


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _week() -> str:
    d = datetime.now(timezone.utc)
    return f"{d.year}-W{d.isocalendar()[1]:02d}"


def _month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


async def increment_msg(chat_id: int, user_id: int, name: str):
    """Increment message count for daily, weekly, and monthly buckets."""
    uid = str(user_id)
    for key, val in [("date", _today()), ("week", _week()), ("month", _month())]:
        await cfr_col.update_one(
            {"chat_id": chat_id, key: val},
            {
                "$inc": {f"users.{uid}.count": 1},
                "$set": {f"users.{uid}.name": name},
            },
            upsert=True,
        )


async def get_top(chat_id: int, period: str = "today", limit: int = 10):
    """
    period: 'today' | 'week' | 'month'
    Returns list of (user_id, name, count) sorted desc.
    """
    if period == "week":
        query = {"chat_id": chat_id, "week": _week()}
    elif period == "month":
        query = {"chat_id": chat_id, "month": _month()}
    else:
        query = {"chat_id": chat_id, "date": _today()}

    doc = await cfr_col.find_one(query)
    if not doc or "users" not in doc:
        return []
    users = doc["users"]
    sorted_users = sorted(
        users.items(), key=lambda x: x[1].get("count", 0), reverse=True
    )
    return [
        (uid, d.get("name", "Unknown"), d.get("count", 0))
        for uid, d in sorted_users[:limit]
    ]
