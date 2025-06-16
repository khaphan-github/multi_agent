from core.singleton import Singleton
# Use env from the same folder
from .env import env
import redis


class RateLimitRedis(metaclass=Singleton):
    def __init__(self):
        rate_limit_host = env.IOREDIS_RATE_LIMIT_HOST
        rate_limit_port = int(env.IOREDIS_RATE_LIMIT_PORT)
        rate_limit_db = int(env.IOREDIS_RATE_LIMIT_DB_INDEX)
        self.key_prefix = env.IOREDIS_RATE_LIMIT_KEY_PREFIX  # Default key prefix from env
        self.client = redis.Redis(
            host=rate_limit_host,
            port=rate_limit_port,
            db=rate_limit_db,
        )
