import asyncio
from redis.asyncio import Redis
from config import Database
from typing import List, Union

class DatabaseClient:
    """Hybrid database client with Redis and in-memory fallback."""
    
    def __init__(self, host: str, port: int, password: str):
        """Initialize database client with Redis connection and in-memory fallback."""
        self.redis = None
        self.use_redis = False
        self.memory_db = {}  # In-memory fallback storage
        
        # Try to connect to Redis
        try:
            self.redis = Redis(host=host, port=port, password=password, ssl=True, decode_responses=True)
            # Test connection
            asyncio.get_event_loop().run_until_complete(self.redis.ping())
            self.use_redis = True
            print("✓ Connected to Redis database")
        except Exception as e:
            print(f"✗ Redis connection failed: {e}")
            print("✓ Using in-memory database as fallback")

    def ensure_str(self, value: Union[str, int]) -> str:
        """Convert value to string for consistent storage."""
        if isinstance(value, (str, int)):
            return str(value)
        raise ValueError("Invalid input type: value should be str or int")

    async def is_inserted(self, var: Union[str, int], id: Union[str, int]) -> bool:
        """Check if an ID exists in the specified key."""
        try:
            var_str, id_str = self.ensure_str(var), self.ensure_str(id)
            if self.use_redis:
                data = await self.redis.get(var_str)
                return id_str in (data.split() if data else [])
            else:
                # In-memory fallback
                return id_str in self.memory_db.get(var_str, [])
        except Exception as e:
            print(f"Error in is_inserted: {e}")
            return False

    async def insert(self, var: Union[str, int], id: Union[str, int]) -> bool:
        """Insert an ID into the specified key."""
        try:
            var_str, id_str = self.ensure_str(var), self.ensure_str(id)
            
            if self.use_redis:
                users = await self.fetch_all(var_str)
                if id_str not in users:
                    users.append(id_str)
                    await self.redis.set(var_str, " ".join(users))
            else:
                # In-memory fallback
                if var_str not in self.memory_db:
                    self.memory_db[var_str] = []
                if id_str not in self.memory_db[var_str]:
                    self.memory_db[var_str].append(id_str)
            return True
        except Exception as e:
            print(f"Error in insert: {e}")
            return False

    async def fetch_all(self, var: Union[str, int]) -> List[str]:
        """Fetch all IDs from the specified key."""
        try:
            var_str = self.ensure_str(var)
            if self.use_redis:
                data = await self.redis.get(var_str)
                return data.split() if data else []
            else:
                # In-memory fallback
                return self.memory_db.get(var_str, [])
        except Exception as e:
            print(f"Error in fetch_all: {e}")
            return []

    async def delete(self, var: Union[str, int], id: Union[str, int]) -> bool:
        """Delete an ID from the specified key."""
        try:
            var_str, id_str = self.ensure_str(var), self.ensure_str(id)
            
            if self.use_redis:
                users = await self.fetch_all(var_str)
                if id_str in users:
                    users.remove(id_str)
                    await self.redis.set(var_str, " ".join(users))
            else:
                # In-memory fallback
                if var_str in self.memory_db and id_str in self.memory_db[var_str]:
                    self.memory_db[var_str].remove(id_str)
            return True
        except Exception as e:
            print(f"Error in delete: {e}")
            return False


# Initialize database client with fallback
db = DatabaseClient(Database.REDIS_HOST, Database.REDIS_PORT, Database.REDIS_PASSWORD)
