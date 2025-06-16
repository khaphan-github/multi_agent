from openai import AsyncOpenAI as OpenAI

async def create_thread(client: OpenAI, thread_id=None):
    """
    Tao thread -> thread_id.
      -  thread_id = None => Tao thread moi
      -  Else = retrival thread_id.
    """
    if thread_id:
        return thread_id

    try:
        thread = await client.beta.threads.create(metadata={"chat_id": str(thread_id)})
        return thread.id
    except Exception as e:
        print(f"Error creating thread: {e}")
        return None


async def remove_thread(client: OpenAI, thread_id):
    if not thread_id:
        await client.beta.threads.delete(thread_id=thread_id)