"""
    This file contains all project configs read from env file.
"""

import os
from dotenv import load_dotenv
load_dotenv()


class Base(object):
    """
    Base configuration class. Contains all the default configurations.
    """

    DEBUG: bool = True
    VERSION: str = "1.0.0"
    TZ: str = os.getenv("TZ", "Asia/Ho_Chi_Minh")


class Config(Base):
    """
    Main configuration class. Contains all the configurations for the project.
    Config redis cache
    """

    DEBUG: bool = True
    VERSION: str = os.getenv("VERSION")
    # OpenAI API Key dung chung cho cac bot
    OPENAI_API_KEY: str = os.getenv("OPEN_AI_API_KEY")

    # Config key to learning course
    BUDDY_LEARNING_COURSE_OPEN_API_KEY: str = os.getenv(
        "BUDDY_LEARNING_COURSE_OPEN_API_KEY")
    BUDDY_LEARNING_COURSE_MODEL_NAME: str = os.getenv(
        "BUDDY_LEARNING_COURSE_MODEL_NAME")
    BUDDY_LEARNING_ASSISTANT_EDUZAA_FULLCOURSE_PREFIX: str = os.getenv(
        "BUDDY_LEARNING_ASSISTANT_EDUZAA_FULLCOURSE_PREFIX", "")

    IOREDIS_HOST: str = os.getenv("IOREDIS_HOST")
    IOREDIS_PORT: str = os.getenv("IOREDIS_PORT")
    IOREDIS_DB_INDEX: str = os.getenv("IOREDIS_DB_INDEX")
    IOREDIS_KEY_PREFIX: str = os.getenv("IOREDIS_KEY_PREFIX")

    SKPY_NOTIFY_HOST: str = os.getenv("SKPY_NOTIFY_HOST")
    EDUZAA_BACKEND_PROXY: str = os.getenv("EDUZAA_BACKEND_PROXY")


config = Config()
