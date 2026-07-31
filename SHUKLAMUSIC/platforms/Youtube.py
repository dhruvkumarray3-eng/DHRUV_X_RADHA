# ---------------------------------------------------------------
# 🔸 ShrutiMusic Api Youtube.py file.
# 🔹 Developed & Maintained by: Nand Yaduvanshi (https://github.com/NoxxOP)
# 📅 Copyright © 2025 – All Rights Reserved
# ❤️ Made with dedication and love by NoxxOP & itzshukla
# ---------------------------------------------------------------

import asyncio
import logging
import os
import re
from typing import Union
import yt_dlp
import aiohttp as _aiohttp_module

_LOGGER = logging.getLogger(__name__)

# ── YouTube Data API v3 helpers ───────────────────────────────────────────────
try:
    from config import YOUTUBE_API_KEY as _YT_API_KEY
except Exception:
    _YT_API_KEY = ""

_YT_API_BASE = "https://www.googleapis.com/youtube/v3"


def _iso_to_min(iso: str) -> str:
    """Convert ISO 8601 duration (PT3M45S) → 'MM:SS' string."""
    h = int((re.search(r'(\d+)H', iso) or type('', (), {'group': lambda s, n: 0})()).group(1) or 0)
    m = int((re.search(r'(\d+)M', iso) or type('', (), {'group': lambda s, n: 0})()).group(1) or 0)
    s = int((re.search(r'(\d+)S', iso) or type('', (), {'group': lambda s, n: 0})()).group(1) or 0)
    total = h * 3600 + m * 60 + s
    mm, ss = divmod(total, 60)
    return f"{mm}:{ss:02d}"


async def _yt_api_search(query: str, max_results: int = 10) -> list:
    """Search via YouTube Data API v3. Returns list of track dicts."""
    if not _YT_API_KEY:
        return []
    try:
        async with _aiohttp_module.ClientSession() as session:
            async with session.get(
                f"{_YT_API_BASE}/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": max_results,
                    "key": _YT_API_KEY,
                },
                timeout=_aiohttp_module.ClientTimeout(total=10),
            ) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
            items = data.get("items") or []
            if not items:
                return []
            # Fetch durations in one batch call
            ids = ",".join(it["id"]["videoId"] for it in items)
            async with session.get(
                f"{_YT_API_BASE}/videos",
                params={"part": "contentDetails", "id": ids, "key": _YT_API_KEY},
                timeout=_aiohttp_module.ClientTimeout(total=10),
            ) as resp2:
                dur_map = {}
                if resp2.status == 200:
                    vdata = await resp2.json()
                    dur_map = {
                        v["id"]: _iso_to_min(v["contentDetails"]["duration"])
                        for v in (vdata.get("items") or [])
                    }
            results = []
            for it in items:
                vid = it["id"]["videoId"]
                sn = it["snippet"]
                thumb = (
                    sn.get("thumbnails", {}).get("high", {}).get("url")
                    or sn.get("thumbnails", {}).get("default", {}).get("url")
                    or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                )
                results.append({
                    "title": sn["title"],
                    "link": f"https://www.youtube.com/watch?v={vid}",
                    "vidid": vid,
                    "duration_min": dur_map.get(vid, "0:00"),
                    "thumb": thumb,
                })
            return results
    except Exception as exc:
        _LOGGER.warning(f"[YT API search] failed for '{query}': {exc}")
        return []


# Cookies: prefer root-level cookies.txt, fall back to assets/cookies.txt
_ROOT_COOKIES = os.path.join(os.path.dirname(__file__), "..", "..", "cookies.txt")
_ASSET_COOKIES = os.path.join(os.path.dirname(__file__), "..", "assets", "cookies.txt")


def _cookies_file():
    for p in (_ROOT_COOKIES, _ASSET_COOKIES):
        if os.path.exists(p) and os.path.getsize(p) > 50:
            return p
    return None


def _base_ydl_opts(**extra):
    """Return a yt-dlp options dict with anti-bot extractor args and cookies.

    Uses format 18 (360p combined H.264+AAC) as the first choice because it
    is served over plain HTTPS and does not require SABR tokens or PO tokens.
    Falls back to bestaudio for videos that don't carry format 18.
    The `android` client exposes format 18; `mweb` provides its config download
    so DO NOT add skip=configs here.
    """
    opts = {
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "format": "18/bestaudio[ext=m4a]/bestaudio/best",
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "mweb"],
            }
        },
    }
    cookies = _cookies_file()
    if cookies:
        opts["cookiefile"] = cookies
    opts.update(extra)
    return opts
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from py_yt import VideosSearch, Playlist
import aiohttp

API_URL = os.environ.get("API_URL", "https://api01.shrutibots.site")

API_KEY = os.environ.get("API_KEY", "ShrutiBots2knm7tCsnIVesZt50Lwb") ## Get This API KEY FROM: @SHRUTIAPIBOT 

DOWNLOAD_DIR = "downloads"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# ── Conversion lock: prevents two coroutines converting the same file ──
import threading as _threading
_conv_locks: dict = {}
_conv_lock_guard = _threading.Lock()


def _get_conv_lock(path: str):
    with _conv_lock_guard:
        if path not in _conv_locks:
            _conv_locks[path] = asyncio.Lock()
        return _conv_locks[path]


def _wav_path(mp3: str) -> str:
    return mp3.replace(".mp3", ".wav")


def _tmp_wav_path(mp3: str) -> str:
    return mp3.replace(".mp3", ".wav.tmp")


async def _convert_to_wav(mp3_path: str) -> str:
    """
    Pre-convert MP3 → 48 kHz stereo PCM WAV so pytgcalls streams with
    zero decode overhead (only Opus encode needed during playback).
    Uses a .tmp file + atomic rename to prevent partial-file reads.
    """
    wav  = _wav_path(mp3_path)
    tmp  = _tmp_wav_path(mp3_path)

    # Fast path – WAV already ready
    if os.path.exists(wav) and os.path.getsize(wav) > 0:
        return wav

    # Serialise per-file so two callers don't race
    lock = _get_conv_lock(mp3_path)
    async with lock:
        # Re-check after acquiring lock
        if os.path.exists(wav) and os.path.getsize(wav) > 0:
            return wav

        # Clean up any leftover .tmp
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass

        try:
            proc = await asyncio.create_subprocess_exec(
                "ffmpeg", "-y",
                "-threads", "0",          # multi-threaded decode
                "-i", mp3_path,
                "-ar", "48000",           # match pytgcalls AudioQuality.HIGH
                "-ac", "2",               # stereo
                "-acodec", "pcm_s16le",   # raw PCM – zero decode overhead during stream
                "-map_metadata", "-1",    # strip tags (smaller, faster seek)
                tmp,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()

            if os.path.exists(tmp) and os.path.getsize(tmp) > 0:
                os.replace(tmp, wav)       # atomic rename
                return wav
        except Exception:
            pass
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

    return mp3_path   # fallback: stream MP3 if conversion failed


def _cleanup_wav_cache(keep: int = 25) -> None:
    """
    Keep only the <keep> most-recently-used WAV files.
    Called asynchronously so it never blocks the event loop.
    """
    try:
        wavs = [
            os.path.join(DOWNLOAD_DIR, f)
            for f in os.listdir(DOWNLOAD_DIR)
            if f.endswith(".wav")
        ]
        if len(wavs) <= keep:
            return
        # Sort oldest-accessed first
        wavs.sort(key=lambda p: os.path.getatime(p))
        for old in wavs[: len(wavs) - keep]:
            try:
                os.remove(old)
                # Also remove matching .mp3 to free space
                mp3 = old.replace(".wav", ".mp3")
                if os.path.exists(mp3):
                    os.remove(mp3)
            except Exception:
                pass
    except Exception:
        pass


async def download_song(link: str) -> str:
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    if not video_id or len(video_id) < 3:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    mp3_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
    wav_path = _wav_path(mp3_path)

    # ── 1. Return cached WAV (lag-free stream, zero conversion wait) ──
    if os.path.exists(wav_path) and os.path.getsize(wav_path) > 0:
        return wav_path

    # ── 2. Download MP3 from ShrutiAPI if not cached ──
    if not (os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 100_000):
        downloaded = False
        for attempt in range(2):          # 1 retry on failure
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{API_URL}/download",
                        params={"url": video_id, "type": "audio", "api_key": API_KEY},
                        timeout=aiohttp.ClientTimeout(total=25),
                    ) as resp:
                        if resp.status != 200:
                            break
                        # Reject non-audio responses (e.g. rate-limit JSON)
                        content_type = resp.content_type or ""
                        if not content_type.startswith("audio/"):
                            break
                        tmp_dl = mp3_path + ".dl"
                        with open(tmp_dl, "wb") as f:
                            async for chunk in resp.content.iter_chunked(131072):
                                f.write(chunk)
                        # Require at least 50 KB — real MP3 is always larger
                        if os.path.exists(tmp_dl) and os.path.getsize(tmp_dl) > 50_000:
                            os.replace(tmp_dl, mp3_path)
                            downloaded = True
                            break
                        # Too small → not real audio; clean up and fall through
                        if os.path.exists(tmp_dl):
                            os.remove(tmp_dl)
            except Exception:
                if os.path.exists(mp3_path + ".dl"):
                    try:
                        os.remove(mp3_path + ".dl")
                    except Exception:
                        pass
                if attempt == 0:
                    await asyncio.sleep(2)   # brief pause before retry

        # ── 2b. Fallback to yt-dlp if ShrutiAPI failed ──
        if not downloaded or not (os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 50_000):
            yt_url = f"https://www.youtube.com/watch?v={video_id}" if "youtube" not in link else link
            tmp_ytdl = mp3_path + ".ytdl"
            try:
                _ytdlp_args = [
                    "yt-dlp",
                    # Prefer highest-quality audio; format 18 is only 360p/AAC
                    # so we skip it here to get true HD audio for streaming.
                    "-f", "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
                    "-x", "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "--no-playlist",
                    "--extractor-args", "youtube:player_client=android,mweb",
                    "--no-check-certificate",
                    "--geo-bypass",
                ]
                _cookies = _cookies_file()
                if _cookies:
                    _ytdlp_args += ["--cookies", _cookies]
                _ytdlp_args += ["-o", tmp_ytdl, yt_url]
                proc = await asyncio.create_subprocess_exec(
                    *_ytdlp_args,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.PIPE,
                )
                _, stderr_data = await asyncio.wait_for(proc.communicate(), timeout=300)
                if proc.returncode != 0 and stderr_data:
                    _LOGGER.warning(
                        f"[download_song] yt-dlp exited {proc.returncode} for {video_id}: "
                        + stderr_data.decode(errors="replace")[-400:]
                    )
                # yt-dlp may append .mp3 extension
                import glob as _glob
                for candidate in [tmp_ytdl, tmp_ytdl + ".mp3"] + _glob.glob(tmp_ytdl + "*"):
                    if os.path.exists(candidate) and os.path.getsize(candidate) > 10_000:
                        os.replace(candidate, mp3_path)
                        downloaded = True
                        break
            except Exception as _ytdl_exc:
                _LOGGER.warning(f"[download_song] yt-dlp exception for {video_id}: {_ytdl_exc}")
            finally:
                import glob as _glob
                for f in _glob.glob(tmp_ytdl + "*"):
                    try:
                        os.remove(f)
                    except Exception:
                        pass

        if not downloaded or not (os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0):
            return None

    # ── 3. Pre-convert to WAV (blocks only for conversion, not download) ──
    result = await _convert_to_wav(mp3_path)

    # ── 4. Background cache housekeeping (non-blocking) ──
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _cleanup_wav_cache, 25)

    return result


async def download_video(link: str) -> str:
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    if not video_id or len(video_id) < 3:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return file_path

    yt_url = f"https://www.youtube.com/watch?v={video_id}" if "youtube" not in link else link
    downloaded = False

    # ── 1. Try ShrutiAPI ──
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/download",
                params={"url": video_id, "type": "video", "api_key": API_KEY},
                timeout=aiohttp.ClientTimeout(total=20),
            ) as resp:
                if resp.status == 200:
                    # Reject non-video responses (e.g. rate-limit JSON)
                    content_type = resp.content_type or ""
                    if content_type.startswith("video/"):
                        tmp_dl = file_path + ".dl"
                        with open(tmp_dl, "wb") as f:
                            async for chunk in resp.content.iter_chunked(131072):
                                f.write(chunk)
                        if os.path.exists(tmp_dl) and os.path.getsize(tmp_dl) > 100_000:
                            os.replace(tmp_dl, file_path)
                            downloaded = True
                        elif os.path.exists(tmp_dl):
                            os.remove(tmp_dl)
    except Exception:
        pass

    # ── 2. Fallback to yt-dlp ──
    if not downloaded:
        tmp_ytdl = file_path + ".ytdl"
        try:
            _ytdlp_args = [
                "yt-dlp",
                # Prefer 1080p H.264 + best audio; fall back to best available.
                "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "--no-playlist",
                "--extractor-args", "youtube:player_client=android,mweb",
                "--no-check-certificate",
                "--geo-bypass",
            ]
            _cookies = _cookies_file()
            if _cookies:
                _ytdlp_args += ["--cookies", _cookies]
            _ytdlp_args += ["-o", tmp_ytdl, yt_url]
            proc = await asyncio.create_subprocess_exec(
                *_ytdlp_args,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr_data = await asyncio.wait_for(proc.communicate(), timeout=120)
            if proc.returncode != 0 and stderr_data:
                _LOGGER.warning(
                    f"[download_video] yt-dlp exited {proc.returncode} for {video_id}: "
                    + stderr_data.decode(errors="replace")[-400:]
                )
            import glob as _glob
            for candidate in [tmp_ytdl, tmp_ytdl + ".mp4"] + _glob.glob(tmp_ytdl + "*"):
                if os.path.exists(candidate) and os.path.getsize(candidate) > 10_000:
                    os.replace(candidate, file_path)
                    downloaded = True
                    break
        except Exception as _ytdl_exc:
            _LOGGER.warning(f"[download_video] yt-dlp exception for {video_id}: {_ytdl_exc}")
        finally:
            import glob as _glob
            for f in _glob.glob(tmp_ytdl + "*"):
                try:
                    os.remove(f)
                except Exception:
                    pass

    if downloaded and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return file_path
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass
    return None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset: entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        # ── 1. YouTube Data API v3 ─────────────────────────────────────────────
        api_results = await _yt_api_search(link, max_results=1)
        if api_results:
            r = api_results[0]
            duration_min = r["duration_min"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
            return r["title"], duration_min, duration_sec, r["thumb"], r["vidid"]
        # ── 2. Fallback: youtube-search-python ────────────────────────────────
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        api_results = await _yt_api_search(link, max_results=1)
        if api_results:
            return api_results[0]["title"]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        api_results = await _yt_api_search(link, max_results=1)
        if api_results:
            return api_results[0]["duration_min"]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        api_results = await _yt_api_search(link, max_results=1)
        if api_results:
            return api_results[0]["thumb"]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            downloaded_file = await download_video(link)
            if downloaded_file:
                return 1, downloaded_file
            return 0, "Video download failed"
        except Exception as e:
            return 0, f"Video download error: {e}"

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            plist = await Playlist.get(link)
        except Exception:
            return []
        videos = plist.get("videos") or []
        ids = []
        for data in videos[:limit]:
            if not data:
                continue
            vid = data.get("id")
            if not vid:
                continue
            ids.append(vid)
        return ids

    async def related_track(self, vidid: str, played_ids: set = None):
        """Fetch a YouTube-related track using the YouTube Radio/Mix playlist.
        Skips vidids in `played_ids` to prevent autoplay repeats.
        Returns (details_dict, vidid) or (None, None) on failure."""

        _played = played_ids or set()

        def _fetch():
            ydl_opts = _base_ydl_opts(
                extract_flat=True,
                playlist_items="2-50",   # large pool to prevent repeats
            )

            url = f"https://www.youtube.com/watch?v={vidid}&list=RD{vidid}"
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    entries = info.get("entries") or []
                    for entry in entries:
                        eid = entry.get("id") or ""
                        etitle = entry.get("title") or ""
                        edur = entry.get("duration")
                        # skip seed, already-played, private/deleted, or shorts (<60 s)
                        if (
                            not eid
                            or eid == vidid
                            or eid in _played
                            or not etitle
                            or etitle in ("[Private video]", "[Deleted video]")
                            or (edur and int(edur) < 60)
                        ):
                            continue
                        dur_min = "0:00"
                        if edur:
                            m, s = divmod(int(edur), 60)
                            dur_min = f"{m}:{s:02d}"
                        return {
                            "title": etitle,
                            "duration_min": dur_min,
                            "vidid": eid,
                            "link": f"https://www.youtube.com/watch?v={eid}",
                            "thumb": f"https://i.ytimg.com/vi/{eid}/hqdefault.jpg",
                        }, eid
            except Exception as e:
                _LOGGER.warning(f"[related_track] Radio Mix fetch failed for {vidid}: {e}")
            return None, None

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        # ── 1. YouTube Data API v3 (fastest, most reliable) ───────────────────
        api_results = await _yt_api_search(link, max_results=1)
        if api_results:
            r = api_results[0]
            return r, r["vidid"]

        # ── 2. Fallback: youtube-search-python ────────────────────────────────
        try:
            results = VideosSearch(link, limit=1)
            result_list = (await results.next()).get("result") or []
            if result_list:
                r = result_list[0]
                track_details = {
                    "title": r["title"],
                    "link": r["link"],
                    "vidid": r["id"],
                    "duration_min": r["duration"],
                    "thumb": r["thumbnails"][0]["url"].split("?")[0],
                }
                return track_details, r["id"]
        except Exception:
            pass

        # ── 3. Last resort: yt-dlp ytsearch ──────────────────────────────────
        def _ytdlp_search():
            opts = _base_ydl_opts(skip_download=True, noplaylist=True)
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{link}", download=False)
                if info and info.get("entries"):
                    entry = info["entries"][0]
                    dur = int(entry.get("duration") or 0)
                    m, s = divmod(dur, 60)
                    return {
                        "title": entry.get("title", "Unknown"),
                        "link": f"https://www.youtube.com/watch?v={entry['id']}",
                        "vidid": entry["id"],
                        "duration_min": f"{m}:{s:02d}",
                        "thumb": f"https://i.ytimg.com/vi/{entry['id']}/hqdefault.jpg",
                    }, entry["id"]
            return None, None

        loop = asyncio.get_event_loop()
        track_details, vidid = await loop.run_in_executor(None, _ytdlp_search)
        if track_details:
            return track_details, vidid

        raise ValueError(f"No search results found for: {link}")

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = _base_ydl_opts()
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    if "dash" not in str(format["format"]).lower():
                        formats_available.append(
                            {
                                "format": format["format"],
                                "filesize": format.get("filesize"),
                                "format_id": format["format_id"],
                                "ext": format["ext"],
                                "format_note": format["format_note"],
                                "yturl": link,
                            }
                        )
                except Exception:
                    continue
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        # ── 1. YouTube Data API v3 ────────────────────────────────────────────
        api_results = await _yt_api_search(link, max_results=10)
        if api_results and query_type < len(api_results):
            r = api_results[query_type]
            return r["title"], r["duration_min"], r["thumb"], r["vidid"]

        # ── 2. Fallback: youtube-search-python ────────────────────────────────
        try:
            a = VideosSearch(link, limit=10)
            result = (await a.next()).get("result") or []
            if result and query_type < len(result):
                r = result[query_type]
                return r["title"], r["duration"], r["thumbnails"][0]["url"].split("?")[0], r["id"]
        except Exception:
            pass

        # ── 3. Last resort: yt-dlp ytsearch10 ────────────────────────────────
        def _ytdlp_slider():
            opts = _base_ydl_opts(skip_download=True, noplaylist=True)
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(f"ytsearch10:{link}", download=False)
                if info and info.get("entries"):
                    idx = min(query_type, len(info["entries"]) - 1)
                    entry = info["entries"][idx]
                    dur = int(entry.get("duration") or 0)
                    m, s = divmod(dur, 60)
                    return (
                        entry.get("title", "Unknown"),
                        f"{m}:{s:02d}",
                        f"https://i.ytimg.com/vi/{entry['id']}/hqdefault.jpg",
                        entry["id"],
                    )
            return None, None, None, None

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _ytdlp_slider)

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
        try:
            if video:
                downloaded_file = await download_video(link)
            else:
                downloaded_file = await download_song(link)
            if downloaded_file:
                return downloaded_file, True
            return None, False
        except Exception:
            return None, False


YouTube = YouTubeAPI()
