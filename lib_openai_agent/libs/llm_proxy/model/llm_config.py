from .llm_budget import LLMBudget


class LLMConfig:
    def __init__(self, enable=True, use_message=False, budget: LLMBudget = None):
        self.enable = enable
        self.budget = budget or None
        self.use_message = use_message

    def is_enable(self):
        return self.enable

    def __repr__(self):
        return f"LLMConfig(enable={self.enable}, use_message={self.use_message}, budget={self.budget})"
