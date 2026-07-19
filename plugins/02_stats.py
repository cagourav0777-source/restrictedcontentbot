import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import db  

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@Client.on_message(filters.command("users") & filters.private)
async def users_handler(client: Client, message: Message):
    """Handle the /users command - shows total users for this bot."""
    bot_info = await Client.get_me()
    user_count = len(await db.fetch_all(f"{bot_info.username}users"))
    await message.reply(f"👥 **Total Users on this bot:** {user_count}")
