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
    - LLM_PROXY_OPEN_AI_DEFAULT_OPEN_API_KEY: The default OpenAI API key. Defaults to an empty string.

    Example `.env` file:
      LLM_PROXY_OPEN_AI_DEFAULT_OPEN_API_KEY=your_openai_api_key
    """
    # OpenAI
    DEFAULT_OPEN_API_KEY: str = os.getenv(
        "LLM_PROXY_OPEN_AI_DEFAULT_OPEN_API_KEY", "")

    DEFAULT_OPEN_AI_MODEL_NAME: str = os.getenv(
        "LLM_PROXY_OPEN_AI_DEFAULT_OPEN_AI_MODEL_NAME", "")


env = Config()
