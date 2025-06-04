# Format stream hanlder
from agents import RawResponsesStreamEvent, RunResultStreaming
from openai.types.responses import ResponseTextDeltaEvent


class StreamHandler:
    def __init__(self, result: RunResultStreaming):
        self.result = result

    async def stream_events(self):
        async for event in self.result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                yield delta
