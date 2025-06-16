import os


class Env:
    # Redis rate limit configurations
    IOREDIS_RATE_LIMIT_HOST: str = os.getenv(
        "IOREDIS_RATE_LIMIT_HOST", "localhost")
    IOREDIS_RATE_LIMIT_PORT: int = int(
        os.getenv("IOREDIS_RATE_LIMIT_PORT", 6379))
    IOREDIS_RATE_LIMIT_DB_INDEX: int = int(
        os.getenv("IOREDIS_RATE_LIMIT_DB_INDEX", 0))
    IOREDIS_RATE_LIMIT_KEY_PREFIX: str = os.getenv(
        "IOREDIS_RATE_LIMIT_KEY_PREFIX", "rate_limit:")

    # Rate limit settings
    RATE_LIMIT_MAX_ATTEMPTS: int = int(os.getenv("RATE_LIMIT_MAX_ATTEMPTS", 5))
    RATE_LIMIT_BLOCK_TIME: int = int(os.getenv("RATE_LIMIT_BLOCK_TIME", 60))
    RATE_LIMIT_SPAM_EXP: int = int(os.getenv("RATE_LIMIT_SPAM_EXP", 3600))

    @classmethod
    def validate(cls):
        required_vars = [
            "IOREDIS_RATE_LIMIT_HOST",
            "IOREDIS_RATE_LIMIT_PORT",
            "IOREDIS_RATE_LIMIT_DB_INDEX",
            "IOREDIS_RATE_LIMIT_KEY_PREFIX",
            "RATE_LIMIT_MAX_ATTEMPTS",
            "RATE_LIMIT_BLOCK_TIME",
            "RATE_LIMIT_SPAM_EXP",
        ]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise EnvironmentError(
                f"RATE_LIMIT_MODULE: Missing required environment variables: {', '.join(missing_vars)}"
            )

    def __repr__(self):
        return (
            f"Env("
            f"IOREDIS_RATE_LIMIT_HOST={self.IOREDIS_RATE_LIMIT_HOST}, "
            f"IOREDIS_RATE_LIMIT_PORT={self.IOREDIS_RATE_LIMIT_PORT}, "
            f"IOREDIS_RATE_LIMIT_DB_INDEX={self.IOREDIS_RATE_LIMIT_DB_INDEX}, "
            f"IOREDIS_RATE_LIMIT_KEY_PREFIX={self.IOREDIS_RATE_LIMIT_KEY_PREFIX}, "
            f"RATE_LIMIT_MAX_ATTEMPTS={self.RATE_LIMIT_MAX_ATTEMPTS}, "
            f"RATE_LIMIT_BLOCK_TIME={self.RATE_LIMIT_BLOCK_TIME}, "
            f"RATE_LIMIT_SPAM_EXP={self.RATE_LIMIT_SPAM_EXP}"
            f")"
        )


env = Env()
