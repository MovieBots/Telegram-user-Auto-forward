import asyncio
import logging
import os

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from storage import load_config, save_config

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("auto-forward")

app = Client(
    "userbot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    session_string=os.environ["SESSION_STRING"],
    workers=20,
)

def own_saved_message(_, __, message):
    return bool(
        message.from_user
        and message.from_user.is_self
        and message.chat.type == "private"
    )

SELF_SAVED = filters.create(own_saved_message)

@app.on_message(SELF_SAVED & filters.command(["help", "start"], prefixes=["/", "."]))
async def help_command(_, message):
    await message.reply_text(
        "User-session auto-forwarder\\n\\n"
        "/addsource <channel_id_or_@username>\\n"
        "/removesource <channel_id_or_@username>\\n"
        "/listsources\\n"
        "/setdest <channel_id_or_@username>\\n"
        "/status\\n\\n"
        "Send these commands in your own Saved Messages. "
        "Your logged-in account must already have access to source channels."
    )

@app.on_message(SELF_SAVED & filters.command(["addsource"], prefixes=["/", "."]))
async def add_source(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /addsource -1001234567890 or /addsource @channel")
    cfg = load_config()
    value = message.command[1]
    if value not in cfg["sources"]:
        cfg["sources"].append(value)
        save_config(cfg)
    await message.reply_text(f"Source added: {value}")

@app.on_message(SELF_SAVED & filters.command(["removesource"], prefixes=["/", "."]))
async def remove_source(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /removesource -1001234567890 or /removesource @channel")
    cfg = load_config()
    value = message.command[1]
    if value not in cfg["sources"]:
        return await message.reply_text("Source not found.")
    cfg["sources"].remove(value)
    save_config(cfg)
    await message.reply_text(f"Source removed: {value}")

@app.on_message(SELF_SAVED & filters.command(["listsources"], prefixes=["/", "."]))
async def list_sources(_, message):
    cfg = load_config()
    await message.reply_text("Sources:\\n" + ("\\n".join(cfg["sources"]) if cfg["sources"] else "(none)"))

@app.on_message(SELF_SAVED & filters.command(["setdest"], prefixes=["/", "."]))
async def set_destination(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /setdest -1001234567890 or /setdest @channel")
    cfg = load_config()
    cfg["destination"] = message.command[1]
    save_config(cfg)
    await message.reply_text(f"Destination set: {cfg['destination']}")

@app.on_message(SELF_SAVED & filters.command(["status"], prefixes=["/", "."]))
async def status(_, message):
    cfg = load_config()
    await message.reply_text(
        f"Source channels: {len(cfg['sources'])}\\n"
        f"Destination: {cfg['destination'] or '(not set)'}"
    )

@app.on_message(filters.incoming & ~filters.service)
async def auto_forward(_, message):
    # Only watch channels explicitly configured by the account owner.
    if message.chat.type != "channel":
        return

    cfg = load_config()
    source_ids = set()
    for source in cfg["sources"]:
        try:
            chat = await app.get_chat(source)
            source_ids.add(chat.id)
        except Exception:
            log.exception("Cannot access configured source %r", source)

    if message.chat.id not in source_ids:
        return

    destination = cfg.get("destination")
    if not destination:
        log.warning("No destination configured; message %s skipped", message.id)
        return

    try:
        await message.copy(destination)
        log.info("Copied message %s from %s to %s", message.id, message.chat.id, destination)
    except FloodWait as exc:
        log.warning("FloodWait: waiting %s seconds before retry", exc.value)
        await asyncio.sleep(exc.value)
        try:
            await message.copy(destination)
            log.info("Copied message %s after FloodWait", message.id)
        except Exception:
            log.exception("Retry failed for message %s", message.id)
    except Exception:
        log.exception("Copy failed for message %s from %s", message.id, message.chat.id)

if __name__ == "__main__":
    log.info("Starting user-session auto-forwarder")
    app.run()
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass

def start_health_server():
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

threading.Thread(
    target=start_health_server,
    daemon=True
).start()
