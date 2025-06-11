from agents import Agent, Runner, trace
import asyncio
from agents import Agent, Runner
from langfuse import Langfuse
from langfuse.types import TraceContext
import base64
import os
from langfuse import observe, get_client
from opentelemetry import trace as otel_trace

from dotenv import load_dotenv
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

# Initialize tracer
tracer = otel_trace.get_tracer(__name__)

# langfuse = Langfuse(
#     secret_key="sk-lf-d6691e4d-f1f8-4606-a2a1-354ecb1ca094",
#     public_key="pk-lf-27382bd2-e4bc-4775-89e0-b6d0a81d035b",
#     host="http://localhost:3000"
# )


@observe(name="main_tracing")
async def main(input_query):
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
    )

    result = await Runner.run(agent, input_query)
    print(result.final_output)
    return result


async def run():
    input_query = "Why is AI agent evaluation important?"

    with tracer.start_as_current_span("OpenAI-Agent-Trace") as span:
        span.set_attribute("langfuse.user.id", "user-12345")
        span.set_attribute("langfuse.session.id", "my-agent-session")
        span.set_attribute("langfuse.tags", [
                           "staging", "demo", "OpenAI Agent SDK"])
        span.set_attribute("langfuse.environment", "local-dev")

        result = await main(input_query)

        # Add input and output values to parent trace
        span.set_attribute("input.value", input_query)
        span.set_attribute("output.value", result.final_output)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
