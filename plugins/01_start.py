import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db  

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    """Handle the /start command for cloned bots - welcomes users and tracks them."""
    user_id = message.from_user.id
    user = await client.get_me()

    await message.reply(
        f"**Hi {message.chat.first_name}!**\n"
        f"I am {user.first_name}, I can save messages from any **public** channel.\n"
        "Just send me the message link, and I will send it to you."
    )
    # Track user in database
    bot_info = await Client.get_me()
    if not await db.is_inserted(f"{bot_info.username}users", user_id):
        await db.insert(f"{bot_info.username}users", user_id)
    if not await db.is_inserted("total_users", user_id):
        await db.insert("total_users", user_id)

@Client.on_message(filters.command("source") & filters.private)
async def source_handler(client: Client, message: Message):
    """Handle the /source command - provides link to source code."""
    await message.reply(
        "Source code available on GitHub.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("View Source", url="https://github.com/Harshit-shrivastav/Save-Contents-Cloner-Bot")]]
        ),
  )
