import logfire
# Configure logfire instrumentation.
logfire.configure(
    service_name='my_agent_service',
 
    send_to_logfire=False,
)
# This method automatically patches the OpenAI Agents SDK to send logs via OTLP to Langfuse.
logfire.instrument_openai_agents()