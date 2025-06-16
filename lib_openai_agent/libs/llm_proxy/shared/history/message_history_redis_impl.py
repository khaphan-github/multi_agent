from ...model.llm_message import LLMMessage, LLMMessageHandler
from redis import Redis, RedisError
from .env import env


class LLMMessageHandlerImpl(LLMMessageHandler):
    def __init__(self):
        try:
            self.redis = Redis(
                host=env.IOREDIS_HOST,
                port=env.IOREDIS_PORT,
                db=int(env.IOREDIS_DB_INDEX)
            )
            self.key_prefix = env.IOREDIS_KEY_PREFIX
        except Exception as e:
            print(f"Failed to initialize Redis connection .env: {e}")
            print(f"LLM_PROXY_OPEN_AI_IOREDIS_HOST={env.IOREDIS_HOST}")
            print(f"LLM_PROXY_OPEN_AI_IOREDIS_PORT={env.IOREDIS_PORT}")
            print(
                f"LLM_PROXY_OPEN_AI_IOREDIS_DB_INDEX={env.IOREDIS_DB_INDEX}")
            print(
                f"LLM_PROXY_OPEN_AI_IOREDIS_KEY_PREFIX={env.IOREDIS_KEY_PREFIX}")
            raise

    def push_message(self, message: LLMMessage):
        """
        Adds a new LLMMessage to the handler and stores it in Redis.

        Redis Output Format:
        - Each message is stored as a hash using `hset` with a unique key:
          Key: {key_prefix}:{chat_session_id}:{message.id}
          Value: A hash containing the message fields (e.g., content, timestamp, etc.)
        - A list is maintained for each chat session using `lpush`:
          Key: {key_prefix}:{chat_session_id}
          Value: A list of message keys in reverse chronological order.
        """
        key = f"{self.key_prefix}:llm_proxy_history_key_list"  # Assuming metadata contains `chat_session_id`
        # Unique key for the message
        message_key = f"{key}:{message.get_id()}"
        try:
            # Use hset to store the message data
            # Use the to_redis_format method to prepare the message
            filtered_message = message.to_redis_format()
            self.redis.hset(message_key, mapping=filtered_message)
            # Use lpush to save the message key
            self.redis.lpush(key, message_key)
        except (RedisError, Exception) as e:
            print(f"Failed to push message to Redis: {e}")

    def __repr__(self):
        return f"LLMMessageHandlerImpl(redis={self.redis}, key_prefix={self.key_prefix!r})"
