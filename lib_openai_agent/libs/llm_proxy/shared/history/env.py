"""
  This file contains all project configs read from env file.
"""

import os
from dotenv import load_dotenv
load_dotenv()


class Config():
    """
    Configuration class for environment variables used in the application.

    Environment Variables:
    - LLM_PROXY_OPEN_AI_IOREDIS_HOST: The hostname for the Redis server. Defaults to "localhost".
    - LLM_PROXY_OPEN_AI_IOREDIS_PORT: The port number for the Redis server. Defaults to 6379.
    - LLM_PROXY_OPEN_AI_IOREDIS_DB_INDEX: The database index to use in Redis. Defaults to 0.
    - LLM_PROXY_OPEN_AI_IOREDIS_KEY_PREFIX: The prefix for Redis keys. Defaults to "llm_proxy".
    - LLM_PROXY_OPEN_AI_DEFAULT_OPEN_API_KEY: The default OpenAI API key. Defaults to an empty string.

    Example `.env` file:
      LLM_PROXY_OPEN_AI_IOREDIS_HOST=redis.example.com
      LLM_PROXY_OPEN_AI_IOREDIS_PORT=6380
      LLM_PROXY_OPEN_AI_IOREDIS_DB_INDEX=1
      LLM_PROXY_OPEN_AI_IOREDIS_KEY_PREFIX=my_custom_prefix
      LLM_PROXY_OPEN_AI_DEFAULT_OPEN_API_KEY=your_openai_api_key
    """
    # Redis
    IOREDIS_HOST: str = os.getenv(
        "LLM_PROXY_OPEN_AI_IOREDIS_HOST", "localhost")
    IOREDIS_PORT: int = int(os.getenv("LLM_PROXY_OPEN_AI_IOREDIS_PORT", 6379))
    IOREDIS_DB_INDEX: int = int(
        os.getenv("LLM_PROXY_OPEN_AI_IOREDIS_DB_INDEX", 0))
    IOREDIS_KEY_PREFIX: str = os.getenv(
        "LLM_PROXY_OPEN_AI_IOREDIS_KEY_PREFIX", "llm_proxy")

    # OpenAI
    DEFAULT_OPEN_API_KEY: str = os.getenv(
        "LLM_PROXY_OPEN_AI_DEFAULT_OPEN_API_KEY", "")


env = Config()
