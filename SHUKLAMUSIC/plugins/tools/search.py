# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from SHUKLAMUSIC import app


class NoResultsFound(Exception):
    """Raised when a search provider returns no usable results."""


class NoResultsOrTrafficError(Exception):
    """Raised when a search provider throttles or rejects the request."""


class SearchResults(list[dict[str, str]]):
    """Keep the legacy five-button layout safe for short result lists."""

    def __getitem__(self, index):
        if isinstance(index, int) and index >= len(self):
            if not self:
                raise IndexError(index)
            return super().__getitem__(-1)
        return super().__getitem__(index)


async def google_search(query: str) -> SearchResults:
    """Fetch public Google results without the unmaintained parser package."""
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
        )
    }
    async with httpx.AsyncClient(
        headers=headers, follow_redirects=True, timeout=15
    ) as client:
        response = await client.get(url)
    if response.status_code in (429, 503):
        raise NoResultsOrTrafficError
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = SearchResults()
    seen_links: set[str] = set()
    for heading in soup.select("h3"):
        anchor = heading.find_parent("a")
        if anchor is None:
            continue
        link = anchor.get("href", "")
        title = heading.get_text(" ", strip=True)
        if not link.startswith("http") or not title or link in seen_links:
            continue
        seen_links.add(link)
        results.append({"titles": title, "links": link})
        if len(results) == 5:
            break
    if not results:
        raise NoResultsFound
    return results


async def stackoverflow_search(query: str) -> SearchResults:
    """Use the official Stack Exchange API for Stack Overflow results."""
    params = {
        "order": "desc",
        "sort": "relevance",
        "intitle": query,
        "site": "stackoverflow",
        "pagesize": 5,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            "https://api.stackexchange.com/2.3/search/advanced",
            params=params,
        )
    if response.status_code in (429, 503):
        raise NoResultsOrTrafficError
    response.raise_for_status()
    results = SearchResults(
        {
            "titles": item["title"],
            "links": item["link"],
        }
        for item in response.json().get("items", [])
        if item.get("title") and item.get("link")
    )
    if not results:
        raise NoResultsFound
    return results


def ikb(rows=None, back=False, todo="start_back"):
    """
    rows = pass the rows
    back - if want to make back button
    todo - callback data of back button
    """
    if rows is None:
        rows = []
    lines = []
    try:
        for row in rows:
            line = []
            for button in row:
                btn_text = button.split(".")[1].capitalize()
                button = btn(btn_text, button)  
                line.append(button)
            lines.append(line)
    except AttributeError:
        for row in rows:
            line = []
            for button in row:
                button = btn(*button)  
                line.append(button)
            lines.append(line)
    except TypeError:
        # make a code to handel that error
        line = []
        for button in rows:
            button = btn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    if back: 
        back_btn = [(btn("ʙᴀᴄᴋ", todo))]
        lines.append(back_btn)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def btn(text, value, type="callback_data"):
    return InlineKeyboardButton(text, **{type: value})






@app.on_message(filters.command('google'))
async def search_(app: app, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**ɢɪᴠᴇ ǫᴜᴇʀʏ ᴛᴏ sᴇᴀʀᴄʜ**")
    to_del = await msg.reply_text("**sᴇᴀʀᴄʜɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ...**")
    query = split[1]
    try:
        result = await google_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"**ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ʀᴇsᴜʟᴛs ᴏғ ʀǫᴜᴇsᴛᴇᴅ : {query.title()}**"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("**ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴄᴏʀʀᴇsᴘᴏɴᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ǫᴜᴇʀʏ**")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("****ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴅᴜᴇ ᴛᴏ ᴛᴏᴏ ᴍᴀɴʏ ᴛʀᴀғғɪᴄ**")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"**sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ :\nʀᴇᴘᴏʀᴛ ᴀᴛ ɪᴛ** @ITSZSHUKLA")
        print(f"error : {e}")
        return



@app.on_message(filters.command('stack'))
async def stack_search_(app: app, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**ɢɪᴠᴇ ǫᴜᴇʀʏ ᴛᴏ sᴇᴀʀᴄʜ**")
    to_del = await msg.reply_text("**sᴇᴀʀᴄʜɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ...**")
    query = split[1]
    try:
        result = await stackoverflow_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"**ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ʀᴇsᴜʟᴛs ᴏғ ʀǫᴜᴇsᴛᴇᴅ : {query.title()}**"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("**ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴄᴏʀʀᴇsᴘᴏɴᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ǫᴜᴇʀʏ**")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("****ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴅᴜᴇ ᴛᴏ ᴛᴏᴏ ᴍᴀɴʏ ᴛʀᴀғғɪᴄ**")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"**sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ :\nʀᴇᴘᴏʀᴛ ᴀᴛ ɪᴛ** @SHASHANKDEVS")
        print(f"error : {e}")
        return




