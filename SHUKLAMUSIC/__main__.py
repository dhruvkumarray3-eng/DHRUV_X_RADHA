# -----------------------------------------------
# SHUKLAMUSIC / DHRUV X RADHA Music Bot
# -----------------------------------------------
import asyncio
import errno
import importlib
import os
from aiohttp import web
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
import config
from SHUKLAMUSIC import LOGGER, app, userbot
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.misc import sudo
from SHUKLAMUSIC.plugins import ALL_MODULES
from SHUKLAMUSIC.utils.database import get_banned_users, get_gbanned
from SHUKLAMUSIC.plugins.tools.vclogger import initialize_vc_logger
from SHUKLAMUSIC.core.commands import register_bot_commands
from pyrogram.errors import FloodWait


# ── Keep-alive web server ─────────────────────────────────────────────────────
async def _ping(request):
    return web.Response(
        text='{"status":"ok","bot":"NOBITA X PRIME"}',
        content_type="application/json",
    )

async def start_keepalive():
    """Start a lightweight HTTP server so the repl stays alive via pings."""
    _app = web.Application()
    _app.router.add_get("/", _ping)
    _app.router.add_get("/ping", _ping)
    runner = web.AppRunner(_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    try:
        await site.start()
    except OSError as error:
        await runner.cleanup()
        if error.errno != errno.EADDRINUSE:
            raise
        LOGGER("SHUKLAMUSIC").warning(
            f"Keep-alive port {port} is already in use; "
            "continuing without starting a second HTTP listener."
        )
        return
    LOGGER("SHUKLAMUSIC").info(f"Keep-alive server started on port {port}")


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
        and not config.STRING6
        and not config.STRING7
    ):
        LOGGER(__name__).error("String Session Not Filled, Please Fill A Pyrogram Session")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            pass
        users = await get_banned_users()
        for user_id in users:
            pass
    except:
        pass
    try:
        await app.start()
    except FloodWait as error:
        wait_seconds = int(getattr(error, "value", 0))
        wait_minutes = max(1, (wait_seconds + 59) // 60)
        LOGGER("SHUKLAMUSIC").warning(
            "Telegram temporarily rate-limited bot authentication "
            f"(retry after about {wait_minutes} minutes); shutting down cleanly."
        )
        return
    for all_module in ALL_MODULES:
        importlib.import_module("SHUKLAMUSIC.plugins" + all_module)
    LOGGER("SHUKLAMUSIC.plugins").info("All Features Loaded!")
    await register_bot_commands()
    await userbot.start()
    await SHUKLA.start()
    try:
        await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SHUKLAMUSIC").error(
            "No active voice chat in LOGGER_ID; continuing without startup audio."
        )
    except:
        pass
    await SHUKLA.decorators()
    await initialize_vc_logger()
    # Restore any dynamic sessions added via /addsession
    try:
        from SHUKLAMUSIC.plugins.sudo.addsession import restore_dynamic_sessions
        await restore_dynamic_sessions()
    except Exception:
        pass
    await start_keepalive()
    LOGGER("SHUKLAMUSIC").info("Bot fully started!")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("SHUKLAMUSIC").info("Bot stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
