# Telegram User-Session Auto-Forwarder

Automatically copies new messages from configured Telegram **channels** to one destination using a Pyrogram user session. Supports videos, documents, photos, captions and other messages that Telegram allows the account to copy.

## Koyeb setup
1. Push this folder to a private GitHub repository.
2. Create a Koyeb service from that repository (Dockerfile build).
3. Add environment variables: `API_ID`, `API_HASH`, `SESSION_STRING`.
4. Optionally set `SOURCE_CHANNELS` (comma-separated IDs/usernames) and `DESTINATION_CHANNEL`.
5. Deploy and inspect Runtime Logs.

## Telegram commands
Send commands in your own **Saved Messages**:
- `/help`
- `/addsource -1001234567890` or `/addsource @channelusername`
- `/removesource -1001234567890`
- `/listsources`
- `/setdest -1009876543210` or `/setdest @channelusername`
- `/status`

The logged-in Telegram user must already be a member of source channels and have permission to post in the destination. Private channels generally need their numeric channel ID. Commands save to `config.json`.

## Session string
Run `pip install -r requirements.txt`, then `python session_generator.py` on your own computer and follow the prompts. Keep the session string private; put it in Koyeb's `SESSION_STRING` variable. Do not commit it to GitHub.

## Important limitations
- Only new messages are copied; old messages are not backfilled.
- This watches channel posts, not private chats or groups.
- Koyeb's local filesystem may be ephemeral. Command-added channels stored in `config.json` can be lost after redeploy/restart unless you use persistent storage. Environment variables `SOURCE_CHANNELS` and `DESTINATION_CHANNEL` are a stable initial configuration.
- Use only for channels and content you are authorized to access and copy.
