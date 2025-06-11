# VIet service goi client
# Service goi runnder.

from dotenv import load_dotenv
from langfuse import observe, get_client
import os
from agents import Runner, trace
from opentelemetry import trace as otel_trace
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
import base64
# Initialize tracer
tracer = otel_trace.get_tracer(__name__)

load_dotenv()

# Build Basic Auth header.
LANGFUSE_AUTH = base64.b64encode(
    f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
).decode()

# Configure OpenTelemetry endpoint & headers
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ.get(
    "LANGFUSE_HOST") + "/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

# OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')


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

        return content

    def _trace_response_output(self,  **kwargs):
        content = ''

        for event in kwargs.get('events', []):
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                content += delta

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
        """
        _chat_id = self.create_or_get_chat_id(chat_id)
        workflow_name = build_workflow_name("Workflow", user_id, _chat_id)

        with tracer.start_as_current_span(workflow_name) as main_span:
            main_span.set_attribute("langfuse.session.id", _chat_id)
            main_span.set_attribute("langfuse.tags", ["workflow", "skill_up"])
            main_span.set_attribute("user_id", user_id or "")
            main_span.set_attribute("chat_id", _chat_id)
            main_span.set_attribute("skill_id", skill_id or "")
            main_span.set_attribute(
                "input", messsage if messsage else "")

            try:
                # Context preparation
                self.save_user_message(
                    user_id=user_id, chat_id=_chat_id, skill_id=skill_id, message=messsage)
                context = self.get_context(user_id, _chat_id, skill_id)

                with tracer.start_as_current_span("AgentPhanLoai") as triage_span:
                    triage_span.set_attribute(
                        "input", messsage if messsage else "")

                    with trace(f"{workflow_name}_triage"):
                        result = await Runner.run(
                            starting_agent=agent,
                            input=messsage,
                            context=context,
                            hooks=AgentRunHook()
                        )

                    triage_span.set_attribute("output", str(result))

                with tracer.start_as_current_span("AgentTaoPhanHoi") as response_span:
                    new_input = result.to_input_list()
                    response_span.set_attribute("input", str(new_input))
                    new_input = result.to_input_list()

                    result = Runner.run_streamed(
                        out_agent, new_input
                    )

                    def call_back_final_response_fn(chat_id, events, metadata):
                        content = self._save_final_response(
                            events=events, chat_id=chat_id, metadata=metadata)
                        response_span.set_attribute("output", content)
                        main_span.set_attribute("status", "success")
                        response_span.set_attribute("stream_initialized", True)

                    return StreamHandler(result).stream_events(
                        chat_id=_chat_id,
                        call_back_final_response_fn=call_back_final_response_fn,
                        metadata={
                            'user_id': user_id,
                            'skill_id': skill_id,
                            'chat_id': _chat_id,
                        },
                    )

            except Exception as e:
                main_span.set_attribute("error", str(e)[:200])
                main_span.set_attribute("status", "error")
                print(f"Error during agent run: {e}")
                raise e
