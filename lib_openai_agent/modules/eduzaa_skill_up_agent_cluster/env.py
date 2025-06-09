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
    OPEN_API_KEY: str = os.getenv(
        "OPEN_API_KEY")

    @classmethod
    def validate(cls):
        """
        Validates that all required environment variables are set.
        Raises an EnvironmentError if any required variables are missing.
        """
        required_vars = [
            "OPEN_API_KEY",
        ]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise EnvironmentError(
                f"OPEN_API_KEY: Missing required environment variables: {', '.join(missing_vars)}"
            )

        # Validate numeric values are actually integers
        integer_vars = [
            ("OPEN_API_KEY", "OPEN_API_KEY"),
        ]

        for attr_name, env_name in integer_vars:
            value = getattr(cls, attr_name)
            if value is not None:
                try:
                    setattr(cls, attr_name, int(value))
                except ValueError:
                    raise EnvironmentError(
                        f"Invalid value for {env_name}: expected integer, got {value}")
        return True

    def __repr__(self):
        """String representation of the environment configuration"""
        return f"AdmissionAIChatbotEnv(OPEN_API_KEY={self.ADMISSION_ASSISTANT_ID})"


# Create a singleton instance for easy import
env = Env()
