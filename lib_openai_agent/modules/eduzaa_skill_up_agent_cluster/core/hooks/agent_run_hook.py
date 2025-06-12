from typing import Any
from agents import RunHooks, Agent, Tool
from agents.run_context import RunContextWrapper
from langfuse import observe, get_client

# Luu thong tin vao bang trace de biet cac buoc da di qua
# Bang vao redis cho nhanh cung duoc

from agents import Agent, Runner, trace
import asyncio
from agents import Agent, Runner
from langfuse import Langfuse
from langfuse.types import TraceContext
import base64
import os
from dotenv import load_dotenv
load_dotenv()


class AgentRunHook(RunHooks):
    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
    """Hook to handle agent run events."""

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        """Called before the agent is invoked."""
        print(
            f"Starting agent: {agent.name}.")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        """Called when the agent produces a final output."""
        print(f"Agent completed: {agent.name}")

    async def on_handoff(self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent) -> None:
        """Called when a handoff occurs."""
        print(f"Handoff from {from_agent.name} to {to_agent.name}")

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        """Called before a tool is invoked."""
        print(f"Agent {agent.name} starting tool: {tool.name}")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:
        """Called after a tool is invoked."""
        print(f"Agent {agent.name} completed tool: {tool.name}")
