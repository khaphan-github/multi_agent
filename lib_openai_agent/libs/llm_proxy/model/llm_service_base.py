import logging
from operator import is_
from .llm_config import LLMConfig
from .llm_budget import LLMBudget


class LLMServiceBase():
    def __init__(self, config: LLMConfig):
        self.config = config

    async def can_use(self):
        '''
            Kiem tra dieu kien
            - Enable - Kich hoat hay khong
            - Budget - Co viet qua han muc hay khong
        '''
        if self.config.is_enable() is False:
            raise ValueError("Assistant is not enabled.")

        if self.config.budget is not None:
            is_budget = await self.config.budget.check_budget_exceeded()
            if is_budget == False:
                raise ValueError(
                    f"Budget exceeded. Cannot use assistant. {self.config.budget}")

    async def get_max_token_limit(self):
        """
        Get the maximum token limit for the assistant.
        """
        if self.config.budget is not None:
            token_limit = await self.config.budget.get_budge_token()
            return None if token_limit == 0 else token_limit
        return None

    async def usaged_budget_token(self, total_token):
        if self.config.budget is not None:
            await self.config.budget.usaged_budget_token(
                usage_token=total_token,
            )
