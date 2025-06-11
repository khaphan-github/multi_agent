# Cau hinh goi bien moi turong.
"""
Environment variable configuration for the Admission AI Chatbot module.
This module loads and validates necessary environment variables.
"""

import base64
import os
from dotenv import load_dotenv
load_dotenv()


class Env:
    # Environment variables
    LANGFUSE_PUBLIC_KEY: str = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST: str = os.getenv("LANGFUSE_HOST")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPEN_API_KEY: str = os.getenv("OPEN_API_KEY")

    @classmethod
    def setup_config(cls):
        """Setup configuration including auth headers and OpenTelemetry"""
        # Build Basic Auth header
        if cls.LANGFUSE_PUBLIC_KEY and cls.LANGFUSE_SECRET_KEY:
            langfuse_auth = base64.b64encode(
                f"{cls.LANGFUSE_PUBLIC_KEY}:{cls.LANGFUSE_SECRET_KEY}".encode()
            ).decode()

            # Configure OpenTelemetry endpoint & headers
            if cls.LANGFUSE_HOST:
                os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = cls.LANGFUSE_HOST + \
                    "/api/public/otel"
                os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {langfuse_auth}"

        # Set OpenAI API Key
        if cls.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = cls.OPENAI_API_KEY

    @classmethod
    def validate(cls):
        """
        Validates that all required environment variables are set.
        Raises an EnvironmentError if any required variables are missing.
        """
        required_vars = [
            "OPENAI_API_KEY",
            "LANGFUSE_PUBLIC_KEY",
            "LANGFUSE_SECRET_KEY",
            "LANGFUSE_HOST"
        ]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        return True

    def __repr__(self):
        """String representation of the environment configuration"""
        return f"Env(OPENAI_API_KEY={'***' if self.OPENAI_API_KEY else None})"


# Create a singleton instance and setup configuration
env = Env()
env.setup_config()

# Validate environment on module import
try:
    env.validate()
except EnvironmentError as e:
    print(f"Warning: {e}")
    print("Please check your .env file or set the required environment variables.")
