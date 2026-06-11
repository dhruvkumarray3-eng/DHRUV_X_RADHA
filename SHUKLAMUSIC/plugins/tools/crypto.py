import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app
from config import BANNED_USERS

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
TONCENTER_URL = "https://tonapi.io/v2/accounts/{address}"

async def fetch_price(coin_id: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                COINGECKO_URL,
                params={"ids": coin_id, "vs_currencies": "usd,inr", "include_24hr_change": "true"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                data = await resp.json()
                return data.get(coin_id, {})
    except Exception:
        return {}


@app.on_message(filters.command(["ton"]) & ~BANNED_USERS)
async def ton_price(client, message: Message):
    m = await message.reply_text("🔄 <b>Fetching TON price...</b>")
    data = await fetch_price("the-open-network")
    if not data:
        return await m.edit_text("❌ <b>Failed to fetch TON price. Try again later.</b>")
    usd = data.get("usd", "N/A")
    inr = data.get("inr", "N/A")
    change = data.get("usd_24h_change", 0)
    arrow = "📈" if change and change > 0 else "📉"
    change_str = f"{change:.2f}%" if change else "N/A"
    await m.edit_text(
        f"<b>💎 TON (The Open Network)</b>\n\n"
        f"💵 <b>USD :</b> <code>${usd:,}</code>\n"
        f"🇮🇳 <b>INR :</b> <code>₹{inr:,}</code>\n"
        f"{arrow} <b>24h Change :</b> <code>{change_str}</code>\n\n"
        f"<i>Powered by CoinGecko</i>"
    )


@app.on_message(filters.command(["usdt"]) & ~BANNED_USERS)
async def usdt_price(client, message: Message):
    m = await message.reply_text("🔄 <b>Fetching USDT price...</b>")
    data = await fetch_price("tether")
    if not data:
        return await m.edit_text("❌ <b>Failed to fetch USDT price. Try again later.</b>")
    usd = data.get("usd", "N/A")
    inr = data.get("inr", "N/A")
    change = data.get("usd_24h_change", 0)
    arrow = "📈" if change and change > 0 else "📉"
    change_str = f"{change:.4f}%" if change else "N/A"
    await m.edit_text(
        f"<b>💵 USDT (Tether)</b>\n\n"
        f"💵 <b>USD :</b> <code>${usd}</code>\n"
        f"🇮🇳 <b>INR :</b> <code>₹{inr:,}</code>\n"
        f"{arrow} <b>24h Change :</b> <code>{change_str}</code>\n\n"
        f"<i>Powered by CoinGecko</i>"
    )


@app.on_message(filters.command(["balance"]) & ~BANNED_USERS)
async def ton_balance(client, message: Message):
    args = message.command
    if len(args) < 2:
        return await message.reply_text(
            "❌ <b>Usage:</b> <code>/balance @username_or_address</code>\n\n"
            "<i>Example: /balance @mytonwallet or /balance UQA...</i>"
        )
    address = args[1].lstrip("@")
    m = await message.reply_text(f"🔄 <b>Fetching TON balance for</b> <code>{address}</code><b>...</b>")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                TONCENTER_URL.format(address=address),
                headers={"Accept": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status != 200:
                    return await m.edit_text(
                        f"❌ <b>Could not find wallet for</b> <code>{address}</code>\n"
                        "<i>Make sure you use a valid TON address or .ton domain.</i>"
                    )
                data = await resp.json()
    except Exception as e:
        return await m.edit_text(f"❌ <b>Error fetching balance:</b> <code>{e}</code>")

    balance_nano = int(data.get("balance", 0))
    balance_ton = balance_nano / 1_000_000_000
    name = data.get("name") or data.get("username") or address
    status = data.get("status", "unknown")

    await m.edit_text(
        f"<b>👛 TON Wallet Balance</b>\n\n"
        f"🏷️ <b>Address :</b> <code>{address}</code>\n"
        f"💎 <b>Balance :</b> <code>{balance_ton:.4f} TON</code>\n"
        f"📊 <b>Status :</b> <code>{status}</code>\n\n"
        f"<i>Powered by TON API</i>"
    )
