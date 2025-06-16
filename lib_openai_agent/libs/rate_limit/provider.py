from .infra_config import RateLimitRedis
from slowapi import Limiter
from slowapi.util import get_remote_address
from .limiter import RateLimiter
from .env import env
rate_limit_redis_provider = RateLimitRedis()
limiter = Limiter(key_func=get_remote_address)

# Singleton instance of RateLimitRedis
rate_limitter_handler = RateLimiter(
    prefix="rate_limit",
    redis_client=rate_limit_redis_provider.client,
    env=env
)
