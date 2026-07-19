import os
import re
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from database import db
from config import Telegram

# Configure logging to file
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize the main bot client
bot = Client("SaveContentBot", api_id=Telegram.API_ID, api_hash=Telegram.API_HASH, bot_token=Telegram.BOT_TOKEN)


@bot.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, message: Message):
    """Handle the /start command - welcomes users and tracks them in database."""
    user_id = message.from_user.id
    logging.info(f"User {user_id} started the bot.")

    await message.reply(
        "Hi, I can create a contents saver bot for public channels for free.\n"
        "Just send/forward your Bot Token to me, and I will handle the rest.\n\n"
        "You can get your bot token from @BotFather."
    )

    if not await db.is_inserted("users", user_id):
        await db.insert("users", user_id)


@bot.on_message(filters.private & filters.command("stats") & filters.user(Telegram.AUTH_USER_ID))
async def stats_handler(client: Client, message: Message):
    """Handle the /stats command - shows bot statistics (admin only)."""
    user_count = len(await db.fetch_all("users"))
    total_user_count = len(await db.fetch_all("total_users"))
    bot_list = await db.fetch_all("bots")
    bot_count = len(bot_list)
    bot_users = "\n".join(bot_list) if bot_list else "No bots registered."

    logging.info(f"Admin requested stats: {user_count} users, {bot_count} bots.")

    await message.reply(f"👥 **User Count:** {user_count}\n👥 **Total User Count:** {total_user_count}\n🤖 **Bot Count:** {bot_count}\n\n**Registered Bots:**\n{bot_users}")


@bot.on_message(filters.private)
async def bot_clone_handler(client: Client, message: Message):
    """Handle bot token messages - creates and starts new bot instances."""
    user_id = message.from_user.id
    msg = await message.reply("⏳ Processing...")

    # Extract bot token from message
    match = re.search(r"\b([0-9]+:[\w-]+)", message.text)
    if not match:
        await msg.edit("❌ No valid Bot Token found. Get it from @BotFather.")
        return

    bot_token = match.group(1)
    
    # Check if bot is already running
    if await db.is_inserted("tokens", bot_token):
        await msg.edit("⚠️ This bot is already running.")
        return
    
    # Create safe client name from token
    client_name = re.sub(r'[^a-zA-Z0-9]', '', bot_token)
    try:
        await msg.edit("🚀 Starting your bot...")
        # Initialize and start new bot client
        new_bot = Client(in_memory=True, name=client_name, api_id=Telegram.API_ID, api_hash=Telegram.API_HASH, bot_token=bot_token, plugins={"root": "plugins"})

        await new_bot.start()
        # Set bot commands
        await new_bot.set_bot_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("users", "Total Users on this bot"),
            BotCommand("source", "Source code of this bot")
        ])

        # Save bot info to database
        bot_info = await new_bot.get_me()
        await db.insert("bots", f"@{bot_info.username}")
        if not await db.is_inserted("tokens", bot_token):
            await db.insert("tokens", bot_token)
        logging.info(f"New bot created: @{bot_info.username} by user {user_id}.")

        await msg.edit(
            f"✅ Successfully started your bot.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Start Bot", url=f"https://t.me/{bot_info.username}")]]
            )
        )
    except Exception as e:
        logging.error(f"Error in bot creation by {user_id}: {e}")
        await msg.edit("❌ An error occurred. Please check your Bot Token and try again.")
        print(e)

@bot.on_message(filters.private & filters.command("logs") & filters.user(Telegram.AUTH_USER_ID))
async def send_logs(client: Client, message: Message):
    """Handle the /logs command - sends log file to admin."""
    if os.path.exists("logs.txt"):
        await message.reply_document("logs.txt")
    else:
        await message.reply("No logs available.")


# Start the bot and keep it running
bot.start()
bot_info = bot.get_me()
print(f"Bot @{bot_info.username} is running!")
asyncio.get_event_loop().run_forever()

