from logging import config
import uuid
from enum import Enum
from datetime import datetime
from config.main import *
import bleach
import pytz  # Add pytz for timezone support
import json  # Add JSON for serialization


class Role(Enum):
    USER = "USER"
    AI = "AI"


class LLMMessage:
    def __init__(self, role: Role, message, usage=None, metadata=None, setting=None, chat_session_id=None, timestamp=None, tz=config.TZ):
        self.id = str(uuid.uuid4())  # Add a unique ID for each message
        self.chat_session_id = chat_session_id
        self.message = message
        self.role = role
        self.setting = setting
        self.usage = usage
        self.metadata = metadata
        self.timestamp = timestamp or datetime.now(pytz.timezone(tz))
        self.timezone = tz  # Store the timezone as a string

    def get_id(self):
        """
        Returns the unique ID of the message.
        """
        return self.id

    def to_redis_format(self):
        """
        Converts the LLMMessage instance into a Redis-compatible dictionary format.
        - Converts datetime fields to ISO 8601 strings.
        - Converts Role enums to strings.
        - Serializes `usage`, `metadata`, and `setting` to JSON if they are objects.
        - Filters out None values.
        """
        return {
            k: (v.value if isinstance(v, Role) else v.isoformat()
                if isinstance(v, datetime) else json.dumps(v, default=lambda o: o.__dict__)
                if k in {"metadata", "setting", "usage"} and v is not None else v)
            for k, v in self.__dict__.items()
            if v is not None
        }

    @classmethod
    def from_redis_format(cls, data):
        """
        Creates an LLMMessage instance from a Redis-compatible dictionary.
        - Converts ISO 8601 strings back to datetime objects.
        - Converts Role strings back to Role enums.
        - Deserializes `usage`, `metadata`, and `setting` from JSON if they are objects.
        - Converts timezone strings back to pytz.timezone objects.
        """
        data['timestamp'] = datetime.fromisoformat(
            data['timestamp']) if 'timestamp' in data else None
        data['role'] = Role(data['role']) if 'role' in data else None
        data['usage'] = json.loads(data['usage']) if 'usage' in data and isinstance(
            data['usage'], str) else data.get('usage')
        data['metadata'] = json.loads(data['metadata']) if 'metadata' in data and isinstance(
            data['metadata'], str) else data.get('metadata')
        data['setting'] = json.loads(data['setting']) if 'setting' in data and isinstance(
            data['setting'], str) else data.get('setting')
        data['tz'] = data.get('timezone', config.TZ)
        data['tz'] = pytz.timezone(data['tz'])
        return cls(**data)

    def __repr__(self):
        return (f"LLMMessage(id={self.id!r}, role={self.role!r}, message={self.message!r}, "
                f"setting={self.setting!r}, usage={self.usage!r}, metadata={self.metadata!r}, "
                f"chat_session_id={self.chat_session_id!r}, timestamp={self.timestamp!r}, timezone={self.timezone!r})")


# Lop con phai implement cai nay de push mesage.

class LLMMessageHandler:
    def push_message(self, message: LLMMessage, **kwargs):
        pass

    def __repr__(self):
        return f"LLMMessageHandler(messages={self.messages!r})"
