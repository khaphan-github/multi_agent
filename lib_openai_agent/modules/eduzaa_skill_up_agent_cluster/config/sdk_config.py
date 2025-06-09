
from agents import set_default_openai_client
from openai import AsyncOpenAI
from ..env import env
custom_client = AsyncOpenAI(api_key=env.OPEN_API_KEY)
set_default_openai_client(custom_client)
