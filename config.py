import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Telegram:
    """Telegram API configuration."""
    API_ID = int(os.environ.get('API_ID'))
    API_HASH = os.environ.get('API_HASH')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    AUTH_USER_ID = int(os.environ.get('AUTH_USER_ID'))
    
class Database:
    """Redis database configuration."""
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
