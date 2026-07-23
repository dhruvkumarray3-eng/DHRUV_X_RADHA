from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb
from config import BANNED_USERS

relation_db = mongodb["user_relations"]


# ─── Brother ──────────────────────────────────────────────────────────────────

@app.on_message(filters.command(["brother"]) & ~BANNED_USERS)
async def set_brother(client, message: Message):
    target = None
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            target = await client.get_users(message.command[1])
        except Exception:
            return await message.reply_text("❌ User not found.")

    if not target:
        return await message.reply_text(
            "👬 **Brother / Bro Setup**\n\nReply to a user or use `/brother @username`"
        )
    if target.id == message.from_user.id:
        return await message.reply_text("😅 You can't set yourself as your own brother!")
    if target.is_bot:
        return await message.reply_text("🤖 Bots can't be family!")

    await relation_db.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"brother": target.id, "brother_name": target.first_name}},
        upsert=True,
    )
    await message.reply_text(
        f"👬 {target.mention} is now your **ʙʀᴏᴛʜᴇʀ**! 🎉\n\n"
        f"Use `/bro` to see your brother anytime."
    )


@app.on_message(filters.command(["bro"]) & ~BANNED_USERS)
async def show_brother(client, message: Message):
    data = await relation_db.find_one({"user_id": message.from_user.id})
    if data and data.get("brother"):
        try:
            user = await client.get_users(data["brother"])
            name = user.mention
        except Exception:
            name = data.get("brother_name", "Unknown")
        return await message.reply_text(f"👬 Your **ʙʀᴏᴛʜᴇʀ**: {name}")
    await message.reply_text(
        "You haven't set a brother yet.\nUse `/brother @username` to set one!"
    )


# ─── Sister ───────────────────────────────────────────────────────────────────

@app.on_message(filters.command(["sister"]) & ~BANNED_USERS)
async def set_sister(client, message: Message):
    target = None
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            target = await client.get_users(message.command[1])
        except Exception:
            return await message.reply_text("❌ User not found.")

    if not target:
        return await message.reply_text(
            "👭 **Sister / Sis Setup**\n\nReply to a user or use `/sister @username`"
        )
    if target.id == message.from_user.id:
        return await message.reply_text("😅 You can't set yourself as your own sister!")
    if target.is_bot:
        return await message.reply_text("🤖 Bots can't be family!")

    await relation_db.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"sister": target.id, "sister_name": target.first_name}},
        upsert=True,
    )
    await message.reply_text(
        f"👭 {target.mention} is now your **sɪsᴛᴇʀ**! 🎉\n\n"
        f"Use `/sis` to see your sister anytime."
    )


@app.on_message(filters.command(["sis"]) & ~BANNED_USERS)
async def show_sister(client, message: Message):
    data = await relation_db.find_one({"user_id": message.from_user.id})
    if data and data.get("sister"):
        try:
            user = await client.get_users(data["sister"])
            name = user.mention
        except Exception:
            name = data.get("sister_name", "Unknown")
        return await message.reply_text(f"👭 Your **sɪsᴛᴇʀ**: {name}")
    await message.reply_text(
        "You haven't set a sister yet.\nUse `/sister @username` to set one!"
    )


# ─── Family overview ──────────────────────────────────────────────────────────

@app.on_message(filters.command(["family", "myrelations", "relations"]) & ~BANNED_USERS)
async def show_family(client, message: Message):
    data = await relation_db.find_one({"user_id": message.from_user.id})
    if not data or (not data.get("brother") and not data.get("sister")):
        return await message.reply_text(
            f"👨‍👩‍👧‍👦 **{message.from_user.first_name}'s Family**\n\n"
            "No relations set yet!\n\n"
            "• `/brother @user` — set brother\n"
            "• `/sister @user` — set sister"
        )

    text = f"👨‍👩‍👧‍👦 **{message.from_user.first_name}'s Family**\n\n"
    if data.get("brother"):
        try:
            bro = await client.get_users(data["brother"])
            bro_name = bro.mention
        except Exception:
            bro_name = data.get("brother_name", "Unknown")
        text += f"👬 **Brother:** {bro_name}\n"

    if data.get("sister"):
        try:
            sis = await client.get_users(data["sister"])
            sis_name = sis.mention
        except Exception:
            sis_name = data.get("sister_name", "Unknown")
        text += f"👭 **Sister:** {sis_name}\n"

    await message.reply_text(text)
