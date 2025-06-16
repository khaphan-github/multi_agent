from typing import Any


class LLMBudget:
    def __init__(self, budget_token: int = 0):
        self.budget_token = budget_token

    def __repr__(self):
        return f"LLMBudget(budget_token={self.budget_token})"

    async def usaged_budget_token(self, usage_token, **kwargs):
        '''
            Phuong thuc nay se duoc dung neu ben xu dung muon co logic lien quan den bugget.
        '''
        try:
            print("Usage token:", usage_token)
        except Exception as e:
            raise Exception(f"Error in usaged_budget_token: {e}")

    async def check_budget_exceeded(self, **kwargs: Any) -> bool:
        '''
            Kiem tra xem da vuot qua han muc hay chua
        '''
        return True

    async def get_budge_token(self, **kwargs: Any) -> int:
        '''
            Max token limit 
        '''
        return self.budget_token
