# Run locally on your own computer. Never share the output session string.
import asyncio
from pyrogram import Client

async def main():
    api_id = int(input("API_ID: ").strip())
    api_hash = input("API_HASH: ").strip()
    async with Client("session_generator", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
        print("\\nSESSION_STRING (keep secret):\\n")
        print(await app.export_session_string())

if __name__ == "__main__":
    asyncio.run(main())
