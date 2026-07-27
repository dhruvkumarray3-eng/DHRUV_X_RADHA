from datetime import datetime, timezone
from SHUKLAMUSIC.utils.mongo import db

cfr_col = db.chatfightrank


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


async def increment_msg(chat_id: int, user_id: int, name: str):
    today = _today()
    await cfr_col.update_one(
        {"chat_id": chat_id, "date": today},
        {
            "$inc": {f"users.{user_id}.count": 1},
            "$set": {f"users.{user_id}.name": name},
        },
        upsert=True,
    )


async def get_top(chat_id: int, limit: int = 10):
    today = _today()
    doc = await cfr_col.find_one({"chat_id": chat_id, "date": today})
    if not doc or "users" not in doc:
        return []
    users = doc["users"]
    sorted_users = sorted(users.items(), key=lambda x: x[1].get("count", 0), reverse=True)
    return [(uid, d.get("name", "Unknown"), d.get("count", 0)) for uid, d, in sorted_users[:limit]]
