"""
Top-level entry point: starts a lightweight HTTP health server in a background
thread, then runs the main Telegram bot in the foreground asyncio event loop.
"""
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import sys


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass  # suppress access logs


def run_health_server():
    server = HTTPServer(("0.0.0.0", 8000), HealthHandler)
    server.serve_forever()


if __name__ == "__main__":
    # Start health server in a daemon thread (won't block process exit)
    t = threading.Thread(target=run_health_server, daemon=True)
    t.start()
    print("[Health] HTTP health server running on 0.0.0.0:8000")

    # Run the bot in the main thread as normal
    import runpy
    runpy.run_module("SHUKLAMUSIC", run_name="__main__", alter_sys=True)
