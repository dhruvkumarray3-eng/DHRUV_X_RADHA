from SHUKLAMUSIC.utils.mongo import db

wg_col = db.wordgame


async def start_game(chat_id: int, first_word: str):
    await wg_col.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "active": True,
                "current_word": first_word.lower(),
                "used_words": [first_word.lower()],
                "scores": {},
            }
        },
        upsert=True,
    )


async def get_game(chat_id: int):
    return await wg_col.find_one({"chat_id": chat_id, "active": True})


async def stop_game(chat_id: int):
    doc = await wg_col.find_one({"chat_id": chat_id})
    scores = doc.get("scores", {}) if doc else {}
    await wg_col.update_one({"chat_id": chat_id}, {"$set": {"active": False}})
    return scores


async def submit_word(chat_id: int, user_id: int, name: str, word: str):
    """Returns (ok: bool, reason: str). Updates state if ok."""
    word = word.lower().strip()
    doc = await get_game(chat_id)
    if not doc:
        return False, "no_game"

    used = doc.get("used_words", [])
    current = doc.get("current_word", "")

    if word in used:
        return False, "used"
    if current and word[0] != current[-1]:
        return False, "wrong_letter"
    if not word.isalpha():
        return False, "invalid"

    uid_str = str(user_id)
    scores = doc.get("scores", {})
    if uid_str not in scores:
        scores[uid_str] = {"name": name, "score": 0}
    scores[uid_str]["name"] = name
    scores[uid_str]["score"] = scores[uid_str].get("score", 0) + 1

    await wg_col.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "current_word": word,
                "scores": scores,
            },
            "$push": {"used_words": word},
        },
    )
    return True, "ok"
