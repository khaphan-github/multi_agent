# Format stream hanlder
from agents import RawResponsesStreamEvent, RunResultStreaming
from openai.types.responses import ResponseTextDeltaEvent


class StreamHandler:
    def __init__(self, result: RunResultStreaming | None):
        self.result = result

    @staticmethod
    def stream_error_events(self, chat_id: str, call_back_stream_event_fn=None, call_back_final_response_fn=None, metadata=None):
        yield {"chat_id": chat_id, "isError": True, "error": "An error occurred while processing the stream."}

    async def stream_events(self, chat_id: str, call_back_stream_event_fn=None, call_back_final_response_fn=None, metadata=None):
        '''
            Truong hop call back co the async.
            call_back_stream_event_fn: nhant ung event
            call_back_final_response_fn: nhan ung phan hoi cuoi cung    
        '''

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
                delta = event.data.delta
                yield delta

        if call_back_final_response_fn:
            if hasattr(call_back_final_response_fn, "__call__") and hasattr(call_back_final_response_fn, "__await__"):
                await call_back_final_response_fn(chat_id=chat_id, events=final_response_event, metadata=metadata)
            else:
                call_back_final_response_fn(
                    chat_id=chat_id, events=final_response_event, metadata=metadata)

        yield {"chat_id": chat_id}

        yield '[DONE]'
