# VIet service goi client
# Service goi runnder.

from modules.eduzaa_skill_up_agent_cluster.stream.stream_handler import StreamHandler
from modules.eduzaa_skill_up_agent_cluster.contexts.context import get_context
from modules.eduzaa_skill_up_agent_cluster.runner.main_agent_runner import run_skillup_conversation


class ServiceManager:
    def __init__(self):
        """
        Khởi tạo ServiceManager.
        """
        pass

    async def run(self, user_id: str = None, chat_id: str = None, skill_id: str = None, messsage: str = None):
        """
        Chạy dịch vụ với các tham số đã cho.
        :param user_id: ID người dùng
        :param chat_id: ID cuộc trò chuyện
        :param skill_id: ID kỹ năng
        :return: Kết quả của dịch vụ
        """
        context = get_context(user_id, chat_id, skill_id)
        run = await run_skillup_conversation(
            user_input=messsage,
            context=context
        )
        return StreamHandler(run).stream_events()
