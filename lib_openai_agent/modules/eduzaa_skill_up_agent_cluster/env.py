# Cau hinh goi bien moi turong.
"""
Environment variable configuration for the Admission AI Chatbot module.
This module loads and validates necessary environment variables.
"""

import os
from dotenv import load_dotenv
load_dotenv()


class Env:
    # General environment variables with sensible defaults
    ADMISSION_OPEN_AI_API_KEY: str = os.getenv("ADMISSION_OPEN_AI_API_KEY")

    @classmethod
    def validate(cls):
        """
        Validates that all required environment variables are set.
        Raises an EnvironmentError if any required variables are missing.
        """
        required_vars = [
            "ADMISSION_OPEN_AI_API_KEY",
        ]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise EnvironmentError(
                f"ADMISSION_AI_CHATBOT_MODULE: Missing required environment variables: {', '.join(missing_vars)}"
            )

        # Validate numeric values are actually integers
        integer_vars = [
            ("IOREDIS_CHAT_HISTORY_PORT", "IOREDIS_CHAT_HISTORY_PORT"),
        ]

        for attr_name, env_name in integer_vars:
            value = getattr(cls, attr_name)
            if value is not None:
                try:
                    setattr(cls, attr_name, int(value))
                except ValueError:
                    raise EnvironmentError(
                        f"Invalid value for {env_name}: expected integer, got {value}")

        # Validate retrieval action value is either ON or OFF
        if cls.RETRIEVAL_BASED_ACTION not in ["ON", "OFF"]:
            raise EnvironmentError(
                f"RETRIEVAL_BASED_ACTION must be ON or OFF, got: {cls.RETRIEVAL_BASED_ACTION}")

        return True

    def __repr__(self):
        """String representation of the environment configuration"""
        return f"AdmissionAIChatbotEnv(ADMISSION_ASSISTANT_ID={self.ADMISSION_ASSISTANT_ID})"

# Create a singleton instance for easy import
env = Env()
