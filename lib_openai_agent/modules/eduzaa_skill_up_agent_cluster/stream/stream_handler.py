# Format stream hanlder
from dataclasses import dataclass
import json
from typing import Any
from agents import RawResponsesStreamEvent, RunResultStreaming
from openai.types.responses import ResponseTextDeltaEvent
import uuid
import re


@dataclass
class StreamObject():
    def __init__(self, chat_id: str, content: str = '', is_error: bool = False, is_last: bool = False,  metadata: Any = {}, error: str = None,):
        self.id = str(uuid.uuid4())
        self.chat_id = chat_id
        self.is_error = is_error
        self.content = content
        self.is_last = is_last
        self.error = error
        # Break line for next line
        # if content includes . or \n then next_line is True
        self.next_line = self.is_end_of_sentence(self.content)
        self.metadata = metadata

    def is_end_of_sentence(self, text: str) -> bool:
        """
        """
        text = text.strip()
        pattern = r'([.!?])([\'")\]]*)$'
        return bool(re.search(pattern, text))

    def to_dict(self):
        return {
            "id": self.id,
            "chatId": self.chat_id,
            "content": self.content,
            "isError": self.is_error,
            "isLast": self.is_last,
            "errorMsg": self.error if self.error else None,
            "nextLine": self.next_line,
            "metadata": self.metadata if self.metadata else {}
        }

    def to_string(self):
        data = self.to_dict()
        data.pop("id", None)
        data.pop("chatId", None)
        return f'id: {self.id}\ndata: {json.dumps(data)} \n\n'


class StreamHandler:
    def __init__(self, result: RunResultStreaming | None):
        self.result = result

    @staticmethod
    def stream_error_events(chat_id: str, error_msg: str = None, metadata: Any = {}):
        '''
            Stream error events.
            chat_id: ID của cuộc trò chuyện.
            error_msg: Thông báo lỗi.
        '''
        yield StreamObject(chat_id=chat_id, error=error_msg, is_error=True, is_last=True, metadata=metadata).to_dict()

    async def stream_events(self, chat_id: str, call_back_stream_event_fn=None, call_back_final_response_fn=None, metadata=None):
        '''
            Truong hop call back co the async.
            call_back_stream_event_fn: nhant ung event
            call_back_final_response_fn: nhan ung phan hoi cuoi cung    
        '''
        yield StreamObject(chat_id=chat_id, metadata=metadata).to_string()

        final_response_event = None
        if call_back_final_response_fn:
            final_response_event = []

        async for event in self.result.stream_events():
            if call_back_final_response_fn:
                final_response_event.append(event)

            if call_back_stream_event_fn:
                if callable(call_back_stream_event_fn):
                    if hasattr(call_back_stream_event_fn, "__call__") and hasattr(call_back_stream_event_fn, "__await__"):
                        await call_back_stream_event_fn(event=event, chat_id=chat_id, metadata=metadata)
                    else:
                        call_back_stream_event_fn(
                            event=event, chat_id=chat_id, metadata=metadata)

            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                # TODO: Change stream object to dict
                delta = event.data.delta
                yield delta
                # yield StreamObject(chat_id=chat_id, content=delta).to_string()

        if call_back_final_response_fn:
            if hasattr(call_back_final_response_fn, "__call__") and hasattr(call_back_final_response_fn, "__await__"):
                await call_back_final_response_fn(chat_id=chat_id, events=final_response_event, metadata=metadata)
            else:
                call_back_final_response_fn(
                    chat_id=chat_id, events=final_response_event, metadata=metadata)

        yield StreamObject(chat_id=chat_id, is_last=True, metadata=metadata).to_string()
