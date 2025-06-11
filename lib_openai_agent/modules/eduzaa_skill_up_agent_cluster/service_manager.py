# VIet service goi client
# Service goi runnder.

from agents import Runner, trace
from .core.models.build_chat_id import build_chat_id
from .core.models.build_workflow_name import build_workflow_name
from .contexts.skill_up import SkillUpContextProvider
from .contexts.user_info import UserInfoContextProvider
from .models.models import CustomContexModel
from .contexts.history import ChatHistoryProvider
from .agents import generate_response_agent
from .agents import triage_agent
from .core.hooks.agent_run_hook import AgentRunHook
from .core.stream.stream_handler import StreamHandler
# Format stream hanlder
from agents import RawResponsesStreamEvent, RunResultStreaming
from openai.types.responses import ResponseTextDeltaEvent


class ServiceManager:
    def __init__(
        self,
        chat_history_provider=ChatHistoryProvider('./chat_history.json'),
        # Addtional context provider.
        skill_up_context_provider=SkillUpContextProvider(),

        # User info context provider
        # TODO: User info context provider.
        user_info_context_provider=UserInfoContextProvider(),
        # Eduzaa bla bla context provider.
    ):
        """
        Khởi tạo ServiceManager.
        """
        self.chat_history_provider = chat_history_provider
        self.skill_up_context_provider = skill_up_context_provider
        self.user_info_context_provider = user_info_context_provider

    def get_context(self, user_id, chat_id, skill_id) -> CustomContexModel:
        """
        Lấy ngữ cảnh hiện tại.
        :return: Ngữ cảnh hiện tại
        """
        message = list(
            map(str, self.chat_history_provider.read(user_id, chat_id)))
        # Lấy mô tả kỹ năng từ skill_id
        skill_info = self.skill_up_context_provider.get_skill(skill_id)

        user_info = self.user_info_context_provider.get_user_info(user_id)

        return CustomContexModel(
            mo_ta=skill_info['mo_ta'],
            history=message,
            user_info=user_info
        )

    def create_or_get_chat_id(self, chat_id) -> str:
        '''
            Create unique chat_id.
        '''
        if chat_id:
            return chat_id
        return build_chat_id()

    def _save_final_response(self, **kwargs):
        """
        Lưu phản hồi cuối cùng vào cơ sở dữ liệu.
        :param user_id: ID người dùng
        :param chat_id: ID cuộc trò chuyện
        :param response: Phản hồi cuối cùng
        """
        content = ''

        for event in kwargs.get('events', []):
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                content += delta

        self.chat_history_provider.create({
            'metadata': kwargs.get('metadata', {}),
            'chat_id': kwargs.get('chat_id', None),
            'content': content,
            'role': 'assistant'
        }, False)

    def save_user_message(self, user_id: str, chat_id: str, skill_id: str, message: str):
        """
        """
        self.chat_history_provider.create({
            'metadata': {'user_id': user_id, 'skill_id': skill_id},
            'chat_id': chat_id,
            'content': message,
            'role': 'user'
        }, False)

    async def run(self, user_id: str = None, chat_id: str = None, skill_id: str = None, messsage: str = None, agent=triage_agent, out_agent=generate_response_agent, ):
        """
        Chạy dịch vụ với các tham số đã cho.
        :param user_id: ID người dùng
        :param chat_id: ID cuộc trò chuyện
        :param skill_id: ID kỹ năng
        :return: Kết quả của dịch vụ
        """
        _chat_id = self.create_or_get_chat_id(chat_id)

        self.save_user_message(
            user_id=user_id,
            chat_id=_chat_id,
            skill_id=skill_id,
            message=messsage
        )

        context = self.get_context(
            user_id, _chat_id, skill_id)

        workflow_name = build_workflow_name('SkillUp', user_id, _chat_id)

        with trace(workflow_name):
            try:
                result = await Runner.run(
                    starting_agent=agent,
                    input=messsage,
                    context=context,
                    hooks=AgentRunHook()
                )

                # Pass result to generate_response_agent
                new_input = result.to_input_list()
                result = Runner.run_streamed(
                    out_agent, new_input
                )

                return StreamHandler(result).stream_events(
                    chat_id=_chat_id,
                    call_back_final_response_fn=self._save_final_response,
                    metadata={
                        'user_id': user_id,
                        'skill_id': skill_id
                    }
                )
            except Exception as e:
                print(f"Error during agent run: {e}")
                StreamHandler.stream_error_events(
                    chat_id=_chat_id,
                    error_msg=str(e)
                )
