from ..model.llm_config import LLMConfig
from .env import env
from ..model.llm_budget import LLMBudget


class DeepSeekLLMConfig(LLMConfig):
    def __init__(self, enable=True, name=None, temperature=None, top_p=None, default_model=None, sys_prompt=None, assistant_id=None, vectorstore_id=None, api_key=None, budget: LLMBudget = None, use_message=False, desc=None, metadata=None, tools=None, tool_instances=None):
        super().__init__(enable=enable, budget=budget, use_message=use_message)
        self.api_key = api_key or env.DEFAULT_DEEPSEEK_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key is required but not provided as DEFAULT_OPEN_API_KEY or api_key at constructor.")
        self.name = name or None
        self.temperature = temperature or None
        self.top_p = top_p or None
        self.default_model = default_model or None
        self.sys_prompt = sys_prompt or None
        self.assistant_id = assistant_id or None
        self.vectorstore_id = vectorstore_id or None
        self.desc = desc or None
        self.metadata = metadata or {}
        self.tools = tools or []
        self.tool_instances = tool_instances or []

    def __repr__(self):
        return f"EduzaaGuestV1Config(name={self.name}, temperature={self.temperature}, " \
               f"default_model={self.default_model}, assistant_id={self.assistant_id}, " \
               f"vectorstore_id={self.vectorstore_id}, api_key={self.api_key}, " \
               f"enable={self.enable}, budget={self.budget}, use_message={self.use_message}, " \
               f"desc={self.desc}, metadata={self.metadata}, tools={self.tools}, " \
               f"tool_instances={self.tool_instances})"
