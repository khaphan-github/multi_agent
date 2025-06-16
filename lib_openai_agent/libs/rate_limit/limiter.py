class RateLimiter:
    def __init__(self, redis_client, prefix, env=None):
        """
        Initialize RateLimiter with Redis client and key prefix.
        :param redis_client: Redis client instance.
        :param prefix: Key prefix for rate limiting.
        :param env: Environment configuration with rate limit settings.
        """
        self.redis_client = redis_client
        self.prefix = prefix
        self.env = env

    def is_ip_blocked(self, ip: str) -> bool:
        """
        Check if an IP is blocked.
        :param ip: IP address to check.
        """
        return self.redis_client.exists(f"{self.prefix}:blocked:{ip}")

    def log_spam_ip(self, ip: str, max_attempts=None, block_time=None, spam_exp=None) -> bool:
        """
        Log failed attempts and block the IP if necessary.
        :param ip: IP address to log.
        :param max_attempts: Maximum allowed attempts before blocking. If None, uses env config.
        :param block_time: Duration to block the IP in seconds. If None, uses env config.
        :param spam_exp: Expiration time for spam logs in seconds. If None, uses env config.
        """
        key = f"{self.prefix}:spam:{ip}"

        # Use env config values if parameters not provided
        if self.env:
            max_attempts = max_attempts or self.env.RATE_LIMIT_MAX_ATTEMPTS
            block_time = block_time or self.env.RATE_LIMIT_BLOCK_TIME
            spam_exp = spam_exp or self.env.RATE_LIMIT_SPAM_EXP

        if self.redis_client.exists(f"{self.prefix}:blocked:{ip}"):
            return True  # IP is already blocked

        count = self.redis_client.incr(key)  # Increment the count
        self.redis_client.expire(key, spam_exp)  # Keep failed attempt logs

        if count >= max_attempts:
            self.redis_client.setex(
                f"{self.prefix}:blocked:{ip}",
                block_time,
                "1"
            )  # Block IP
            return True  # IP is now blocked

        return False
