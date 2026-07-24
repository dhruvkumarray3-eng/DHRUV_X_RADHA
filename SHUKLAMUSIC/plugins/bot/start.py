import asyncio
import os
import random
import html
import time
import json as _json
import urllib.request
import aiohttp
from pyrogram import filters, enums
from pyrogram.enums import ButtonStyle, ChatType
from pyrogram.types import (
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
import yt_dlp

import config
from SHUKLAMUSIC import app
from SHUKLAMUSIC.misc import _boot_
from SHUKLAMUSIC.plugins.sudo.sudoers import sudoers_list
from SHUKLAMUSIC.utils import bot_sys_stats
from SHUKLAMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)

# --- DATABASE FIX (Ping Jaisa) ---
try:
    from SHUKLAMUSIC.core.mongo import mongodb as db
except ImportError:
    try:
        from SHUKLAMUSIC.utils.database import mongodb as db
    except ImportError:
        from SHUKLAMUSIC.core.mongo import mongodb
        db = mongodb

from SHUKLAMUSIC.utils.decorators.language import LanguageStart
from SHUKLAMUSIC.utils.formatters import get_readable_time
from SHUKLAMUSIC.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string
from SHUKLAMUSIC.utils.branding import BRAND_NAME, BRAND_LINK

# ================================
#        DATABASE SETUP
# ================================
welcome_db = db.welcome_config 

YUMI_PICS = [
    "https://files.catbox.moe/ky6ln3.jpg",
    "https://files.catbox.moe/booqz5.jpg",
    "https://files.catbox.moe/qlq89x.jpg",
    "https://files.catbox.moe/ifgkkl.jpg",
    "https://files.catbox.moe/qm6b0n.jpg",
    "https://files.catbox.moe/ap3m1t.png",
    "https://files.catbox.moe/0k863e.png",
    "https://files.catbox.moe/vp5hg5.png",
]

GREET = [
    "💞", "🥂", "🔍", "🧪", "🥂", "⚡️", "🔥",
]

async def delete_sticker_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()

# ================================
#      SET WELCOME COMMANDS
# ================================
# Yahan maine filter change karke aapki ID laga di hai (Ping jaisa)
@app.on_message(filters.command(["setwelcome_dm", "setwelcome_grp"]) & filters.user(7553434931))
async def set_welcome_msg(client, message):
    cmd = message.command[0].lower()
    msg_type = "welcome_dm" if "dm" in cmd else "welcome_group"

    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            f"❌ <b>Usage:</b>\n<code>/{cmd} [Your HTML Message]</code>\n\n"
            "<b>Variables:</b>\n"
            "<code>{name}</code> - First Name\n"
            "<code>{mention}</code> - User Link\n"
            "<code>{username}</code> - @Username\n"
            "<code>{bot_name}</code> - Bot Name\n"
            "<code>{chat_name}</code> - Chat Name (Group only)"
        )
        return

    # Extract Text (Preserving HTML for Premium Emojis)
    try:
        if message.reply_to_message:
            new_msg = message.reply_to_message.text.html or message.reply_to_message.caption.html
        else:
            new_msg = message.text.html.split(None, 1)[1]
    except (IndexError, AttributeError):
         return await message.reply_text("❌ Text extract nahi kar paya. Dobara try karein.")

    # Save to Database
    await welcome_db.update_one(
        {"_id": msg_type},
        {"$set": {"message": new_msg}},
        upsert=True
    )
    
    await message.reply_text(f"✅ <b>{msg_type.replace('_', ' ').upper()} message has been set!</b>")


@app.on_message(filters.command(["resetwelcome"]) & filters.user(7553434931))
async def reset_welcome_msg(client, message):
    cmd_args = message.command
    msg_type = "welcome_dm"
    if len(cmd_args) > 1 and cmd_args[1].lower() in ("grp", "group"):
        msg_type = "welcome_group"
    result = await welcome_db.delete_one({"_id": msg_type})
    if result.deleted_count:
        await message.reply_text(
            f"✅ <b>{msg_type.replace('_', ' ').upper()} reset!</b>\n"
            "<i>Bot will now use the default start message from en.yml (with new Crypto & UPI features).</i>"
        )
    else:
        await message.reply_text(
            f"ℹ️ <b>No custom {msg_type.replace('_', ' ')} was saved.</b>\n"
            "<i>Already using the default message.</i>"
        )

# Helper to get welcome text
async def get_welcome_caption(msg_type, default_text, user, bot, chat=None):
    data = await welcome_db.find_one({"_id": msg_type})
    
    if data and "message" in data:
        text = data["message"]
        # Replace Placeholders
        text = text.replace("{name}", user.first_name)
        text = text.replace("{mention}", user.mention)
        text = text.replace("{username}", f"@{user.username}" if user.username else "No Username")
        text = text.replace("{bot_name}", bot.first_name)
        if chat:
            text = text.replace("{chat_name}", chat.title)
        return text
    
    return default_text

# ================================
#        START COMMAND (DM)
# ================================
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    
    # --- REACTION START ---
    try:
        await message.react(emoji="❤️‍🔥")
    except Exception:
        pass
    # --- REACTION END ---

    # --- ANIMATION START ---
    await add_served_user(message.from_user.id)
    try:
        # Step 1 — Send premium emojis splash
        emoji_splash = await message.reply_text(
            '<emoji id=5857427272448876539>🤩</emoji>  <emoji id=5854711294044677474>🤩</emoji>'
        )
        await asyncio.sleep(0.5)
        await emoji_splash.delete()

        # Step 2 — Writing animation (0.3s between edits to respect Telegram rate limits)
        loading_1 = await message.reply_text(random.choice(GREET))
        await asyncio.sleep(0.3)
        await loading_1.edit_text("<b>ᴅɪηɢ ᴅᴏηɢ.❤️‍🔥</b>")
        await asyncio.sleep(0.3)
        await loading_1.edit_text("<b>ᴅɪηɢ ᴅᴏηɢ..❤️‍🔥</b>")
        await asyncio.sleep(0.3)
        await loading_1.edit_text("<b>ᴅɪηɢ ᴅᴏηɢ...❤️‍🔥</b>")
        await asyncio.sleep(0.3)
        await loading_1.edit_text("<b>ɴᴏʙɪᴛᴀ</b>")
        await asyncio.sleep(0.3)
        await loading_1.edit_text("<b>ɴᴏʙɪᴛᴀ ꭙ</b>")
        await asyncio.sleep(0.3)
        await loading_1.edit_text("<b>ɴᴏʙɪᴛᴀ ꭙ ϻᴜsɪᴄ ♪</b>")
        await asyncio.sleep(0.3)
        await loading_1.edit_text("<b>sᴛᴀʀᴛᴇᴅ!✨</b>")
        await asyncio.sleep(0.3)
        await loading_1.delete()
    except Exception:
        # If animation fails (flood wait, etc.) just continue to show menu
        try:
            await loading_1.delete()
        except Exception:
            pass
    # --- ANIMATION END ---

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name in {"chatfight", "wordplay", "wordgame"}:
            from SHUKLAMUSIC.plugins.tools.chatfight import start_word_game
            await start_word_game(message.chat.id)
        elif name.startswith("channelplay_"):
            channel_id = name.split("_", 1)[1]
            await message.reply_text(
                f"🔗 <b>ᴄᴏɴɴᴇᴄᴛ {BRAND_NAME}</b>\n\n"
                "Add me to your group with the button below, then I will connect "
                "this channel automatically when you send /start.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔗 ᴀᴅᴅ ᴍᴇ & ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ",
                        url=f"https://t.me/{app.username}?startgroup=channelplay_{channel_id}",
                        style=ButtonStyle.SUCCESS,
                    )
                ], [
                    InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT, style=ButtonStyle.DANGER)
                ]]),
            )
        elif name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_photo(
                random.choice(YUMI_PICS),
                has_spoiler=True,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        elif name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
        elif name[0:3] == "inf":
            # ── Info handler: uses oEmbed (no auth needed) ──
            m = await message.reply_text("🔎")
            vidid = str(name).replace("info_", "", 1)
            video_url = f"https://www.youtube.com/watch?v={vidid}"
            try:
                loop = asyncio.get_event_loop()
                def _oembed_fetch():
                    oe_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
                    with urllib.request.urlopen(oe_url, timeout=8) as r:
                        return _json.loads(r.read())
                oembed = await loop.run_in_executor(None, _oembed_fetch)
                title     = oembed.get("title") or "Unknown"
                channel   = oembed.get("author_name") or "Unknown"
                thumbnail = oembed.get("thumbnail_url") or ""
                channellink = f"https://www.youtube.com/results?search_query={vidid}"
                duration  = "N/A"
                views     = "N/A"
                published = "N/A"
                searched_text = _["start_6"].format(
                    title, duration, views, published, channellink, channel, app.mention
                )
                key = InlineKeyboardMarkup([[
                    InlineKeyboardButton(text=_["S_B_8"], url=video_url),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                ]])
                await m.delete()
                try:
                    await app.send_photo(
                        chat_id=message.chat.id,
                        photo=thumbnail,
                        caption=searched_text,
                        reply_markup=key,
                    )
                except Exception:
                    await message.reply_text(searched_text, reply_markup=key, disable_web_page_preview=True)
            except Exception:
                await m.edit_text("❌ Song info nahi mili. Dobara try karo.")
        elif name.startswith("dl_"):
            # ── Download handler via ShrutiAPI (bypasses YouTube bot-check) ──
            m = await message.reply_text("⏬ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ sᴏɴɢ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ... ❤️‍🔥")
            try:
                parts   = name[3:].rsplit("_", 1)
                vidid   = parts[0]
                dl_type = parts[1] if len(parts) == 2 else "a"
                os.makedirs("downloads", exist_ok=True)
                powered  = "✦ ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/II_NOBITA_X_PRIME_II'>𝚴 𝐎 𝐁 𝚰 𝐓 𝚲 𝐗 𝚸 𝐑 𝐈 𝐌 𝐄❤️‍🔥</a>"
                api_url  = "https://api01.shrutibots.site"
                api_key  = "ShrutiBots2knm7tCsnIVesZt50Lwb"
                api_type = "video" if dl_type == "v" else "audio"
                ext      = "mp4" if dl_type == "v" else "mp3"
                out_file = f"downloads/{vidid}_dl_{dl_type}.{ext}"
                tmp_file = out_file + ".tmp"

                # Download from ShrutiAPI
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{api_url}/download",
                        params={"url": vidid, "type": api_type, "api_key": api_key},
                        timeout=aiohttp.ClientTimeout(total=300),
                    ) as resp:
                        if resp.status != 200:
                            await m.edit_text("❌ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ. ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
                            return
                        with open(tmp_file, "wb") as f:
                            async for chunk in resp.content.iter_chunked(131072):
                                f.write(chunk)

                if not (os.path.exists(tmp_file) and os.path.getsize(tmp_file) > 0):
                    await m.edit_text("❌ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ. ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
                    return
                os.replace(tmp_file, out_file)

                await m.delete()
                if dl_type == "v":
                    await app.send_video(
                        chat_id=message.chat.id,
                        video=out_file,
                        caption=f"🎬 <b>HD ᴠɪᴅᴇᴏ — ɴᴏʙɪᴛᴀ 𝗫 ᴘʀɪᴍᴇ ᴍᴜsɪᴄ ʙᴏᴛ</b>\n\n{powered}",
                        supports_streaming=True,
                    )
                else:
                    await app.send_audio(
                        chat_id=message.chat.id,
                        audio=out_file,
                        caption=f"🎵 <b>HD ᴀᴜᴅɪᴏ 320kbps — ɴᴏʙɪᴛᴀ 𝗫 ᴘʀɪᴍᴇ ᴍᴜsɪᴄ ʙᴏᴛ</b>\n\n{powered}",
                    )
                try:
                    os.remove(out_file)
                except Exception:
                    pass
            except Exception:
                try:
                    await m.edit_text("❌ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ. ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
                except Exception:
                    pass
    else:
        out = private_panel(_)
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        
        # --- GET CUSTOM OR DEFAULT CAPTION ---
        default_caption = _["start_2"].format(
            message.from_user.mention, app.mention, UP, DISK, CPU, RAM, served_users, served_chats
        )
        
        # Checking DB for Custom DM Message
        final_caption = await get_welcome_caption(
            "welcome_dm", 
            default_caption, 
            message.from_user, 
            await client.get_me()
        )

        await message.reply_photo(
            random.choice(YUMI_PICS),
            has_spoiler=True,
            caption=final_caption,
            reply_markup=InlineKeyboardMarkup(out),
        )
        
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )

# ================================
#        START COMMAND (GROUP)
# ================================
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    # --- REACTION START ---
    try:
        await message.react(emoji="❤️‍🔥")
    except Exception:
        pass
    # --- REACTION END ---
    
    payload = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""
    if payload.startswith("channelplay_"):
        channel_id = payload.split("_", 1)[1]
        try:
            from SHUKLAMUSIC.utils.database import set_cmode
            await set_cmode(message.chat.id, int(channel_id))
            await message.reply_text(
                f"✅ <b>ᴄʜᴀɴɴᴇʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ!</b>\n\n"
                f"🎵 {BRAND_NAME} will now stream in the selected channel.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎵 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", url=f"https://t.me/{app.username}?start=help", style=ButtonStyle.PRIMARY),
                    InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT, style=ButtonStyle.DANGER),
                ]]),
            )
        except Exception:
            await message.reply_text("❌ Channel connect failed. Make sure I am an admin in the channel and group.")
        return
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    
    # --- GET CUSTOM OR DEFAULT CAPTION ---
    default_caption = _["start_1"].format(app.mention, get_readable_time(uptime))
    
    final_caption = await get_welcome_caption(
        "welcome_group", 
        default_caption, 
        message.from_user, 
        await client.get_me(),
        message.chat
    )

    await message.reply_photo(
        random.choice(YUMI_PICS),
        caption=final_caption,
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

# ================================
#        NEW MEMBER WELCOME
# ================================
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                # ── CHANNEL: stay, send connect-channel message, DM adder ──
                if message.chat.type == ChatType.CHANNEL:
                    await add_served_chat(message.chat.id)
                    channel_buttons = InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                text="🔗 ᴄᴏɴɴᴇᴄᴛ ᴛʜɪs ᴄʜᴀɴɴᴇʟ",
                                url=f"https://t.me/{app.username}?start=channelplay_{message.chat.id}",
                                style=ButtonStyle.SUCCESS,
                            ),
                            InlineKeyboardButton(
                                text="🎵 sᴜᴘᴘᴏʀᴛ",
                                url=f"https://t.me/{config.SUPPORT_CHAT}",
                                style=ButtonStyle.DANGER,
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="📖 ʜᴏᴡ ᴛᴏ ᴜsᴇ",
                                url=f"https://t.me/{app.username}?start=help",
                            ),
                        ],
                    ])
                    try:
                        await message.reply_photo(
                            random.choice(YUMI_PICS),
                            caption=_["start_channel_1"].format(message.chat.title),
                            reply_markup=channel_buttons,
                        )
                    except Exception:
                        try:
                            await app.send_message(
                                message.chat.id,
                                _["start_channel_1"].format(message.chat.title),
                                reply_markup=channel_buttons,
                            )
                        except Exception:
                            pass
                    # DM the adder (channel) with connect-channel button
                    try:
                        if message.from_user:
                            ch_id = message.chat.id
                            ch_username = message.chat.username
                            # The payload survives the add-to-group flow and is
                            # consumed by start_gp to connect this channel.
                            connect_url = f"https://t.me/{app.username}?startgroup=channelplay_{ch_id}"
                            await app.send_message(
                                message.from_user.id,
                                _["start_dm_ch_1"].format(
                                    message.from_user.mention,
                                    message.chat.title,
                                ),
                                reply_markup=InlineKeyboardMarkup([
                                    [
                                        InlineKeyboardButton(
                                            "🔗 ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ",
                                             url=connect_url,
                                        ),
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            "📖 ʜᴏᴡ ᴛᴏ sᴇᴛᴜᴘ",
                                            url=f"https://t.me/{app.username}?start=help",
                                        ),
                                        InlineKeyboardButton(
                                            "💬 sᴜᴘᴘᴏʀᴛ",
                                            url=f"https://t.me/{config.SUPPORT_CHAT}",
                                        ),
                                    ],
                                ]),
                            )
                    except Exception:
                        pass
                    return await message.stop_propagation()

                # ── BASIC GROUP: tell to convert to supergroup ──
                if message.chat.type not in (ChatType.SUPERGROUP, ChatType.CHANNEL):
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                # ── BLACKLISTED ──
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                # ── SUPERGROUP: welcome in group + DM adder ──
                out = start_panel(_)
                
                default_caption = _["start_3"].format(
                    message.from_user.mention,
                    app.mention,
                    message.chat.title,
                    app.mention,
                )
                
                final_caption = await get_welcome_caption(
                    "welcome_group", 
                    default_caption, 
                    member,
                    await client.get_me(),
                    message.chat
                )

                await message.reply_photo(
                    random.choice(YUMI_PICS),
                    has_spoiler=True,
                    caption=final_caption,
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)

                # Auto-detect and link channel if group has a linked channel
                try:
                    from SHUKLAMUSIC.utils.database import set_cmode
                    chat_info = await client.get_chat(message.chat.id)
                    if chat_info.linked_chat:
                        await set_cmode(message.chat.id, chat_info.linked_chat.id)
                except Exception:
                    pass

                # DM the adder (group) with help button
                try:
                    if message.from_user:
                        await app.send_message(
                            message.from_user.id,
                            _["start_dm_grp_1"].format(
                                message.from_user.mention,
                                message.chat.title,
                            ),
                            reply_markup=InlineKeyboardMarkup([
                                [
                                    InlineKeyboardButton(
                                        "🎵 /ᴘʟᴀʏ sᴏɴɢ",
                                        url=f"https://t.me/{app.username}?start=help",
                                    ),
                                    InlineKeyboardButton(
                                        "📖 ᴄᴏᴍᴍᴀɴᴅs",
                                        url=f"https://t.me/{app.username}?start=help",
                                    ),
                                ],
                                [
                                    InlineKeyboardButton(
                                        "💬 sᴜᴘᴘᴏʀᴛ",
                                        url=f"https://t.me/{config.SUPPORT_CHAT}",
                                    ),
                                ],
                            ]),
                        )
                except Exception:
                    pass

                await message.stop_propagation()
        except Exception as ex:
            print(ex)


@app.on_chat_member_updated(filters.channel, group=-10)
async def channel_bot_added(client, member: ChatMemberUpdated):
    """Handle channel additions where Telegram does not emit new_chat_members."""
    old = member.old_chat_member
    new = member.new_chat_member
    if not new or new.user.id != app.id:
        return
    if old and old.status not in {"left", "kicked"}:
        return

    chat = member.chat
    await add_served_chat(chat.id)
    connect_url = f"https://t.me/{app.username}?startgroup=channelplay_{chat.id}"
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔗 ᴄᴏɴɴᴇᴄᴛ ᴛʜɪs ᴄʜᴀɴɴᴇʟ",
                    url=connect_url,
                    style=ButtonStyle.SUCCESS,
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 ʜᴏᴡ ᴛᴏ sᴇᴛᴜᴘ",
                    url=f"https://t.me/{app.username}?start=help",
                    style=ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    "💬 sᴜᴘᴘᴏʀᴛ",
                    url=config.SUPPORT_CHAT,
                    style=ButtonStyle.DANGER,
                ),
            ],
        ]
    )
    try:
        await app.send_message(
            member.from_user.id,
            f"👋 <b>ʜᴇʟʟᴏ {member.from_user.mention}!</b>\n\n"
            f"✅ <b>{BRAND_NAME}</b> was added to <b>{html.escape(chat.title or 'your channel')}</b>.\n"
            "Use the button below to connect this channel to a music group.",
            reply_markup=buttons,
        )
    except Exception:
        # Telegram can reject unsolicited DMs when the adder has never opened
        # the bot; the in-channel setup message remains available.
        pass
    try:
        await client.send_message(
            chat.id,
            f"✅ <b>{BRAND_NAME}</b> is ready in <b>{html.escape(chat.title or 'this channel')}</b>.\n"
            "Open the private setup button to connect a music group.",
            reply_markup=buttons,
        )
    except Exception:
        pass
