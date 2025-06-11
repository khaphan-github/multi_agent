from typing import Any
from agents import RunHooks, Agent, Tool
from agents.run_context import RunContextWrapper
from langfuse import observe, get_client
from opentelemetry import trace as otel_trace
import base64
import os
from dotenv import load_dotenv

# Luu thong tin vao bang trace de biet cac buoc da di qua
# Bang vao redis cho nhanh cung duoc

from agents import Agent, Runner, trace
from agents import Agent, Runner

load_dotenv()

# Build Basic Auth header.
LANGFUSE_AUTH = base64.b64encode(
    f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
).decode()

# Configure OpenTelemetry endpoint & headers
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ.get(
    "LANGFUSE_HOST") + "/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

# Initialize tracer
tracer = otel_trace.get_tracer(__name__)


class AgentRunHook(RunHooks):
    def __init__(self):
        self.spans = {}

    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
    """Hook to handle agent run events."""

    @observe(name="agent_start")
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        """Called before the agent is invoked."""
        span = tracer.start_span(f"{agent.name}")
        span.set_attribute("agent.name", agent.name)

        # Get input from context
        input_data = getattr(context, '_input', '') or str(context)
        span.set_attribute("input", input_data)

        self.spans[agent.name] = span
        print(f"🚀 Starting agent: {agent.name}")

    @observe(name="agent_end")
    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        """Called when the agent produces a final output."""
        if agent.name in self.spans:
            span = self.spans[agent.name]
            span.set_attribute("output", str(output))
            span.set_attribute("status", "completed")
            span.end()
            del self.spans[agent.name]

        print(f"✅ Agent completed: {agent.name}")

    @observe(name="agent_handoff")
    async def on_handoff(self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent) -> None:
        """Called when a handoff occurs."""
        with tracer.start_as_current_span("handoff") as span:
            span.set_attribute("from_agent", from_agent.name)
            span.set_attribute("to_agent", to_agent.name)

        print(f"🔄 Handoff from {from_agent.name} to {to_agent.name}")

    @observe(name="tool_start")
    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        """Called before a tool is invoked."""
        span = tracer.start_span(f"tool_{tool.name}")
        span.set_attribute("tool.name", tool.name)
        span.set_attribute("agent.name", agent.name)

        tool_key = f"{agent.name}_{tool.name}"
        self.spans[tool_key] = span

        print(f"🔧 Agent {agent.name} starting tool: {tool.name}")

    @observe(name="tool_end")
    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:
        """Called after a tool is invoked."""
        tool_key = f"{agent.name}_{tool.name}"
        if tool_key in self.spans:
            span = self.spans[tool_key]
            span.set_attribute("output", str(result))
            span.set_attribute("status", "completed")
            span.end()
            del self.spans[tool_key]

        print(f"✅ Agent {agent.name} completed tool: {tool.name}")
