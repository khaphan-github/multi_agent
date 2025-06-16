from openai import AsyncOpenAI as OpenAI


async def create_run(client: OpenAI, run_data, **kwargs):
    """
    Create a new run.

    Args:
        client (OpenAI): The OpenAI client instance.
        run_data (dict): Data required to create the run.
        **kwargs: Additional arguments for the run creation.

    Returns:
        dict: The created run's details.
    """
    try:
        run = await client.beta.runs.create(**run_data, **kwargs)
        return run
    except Exception as e:
        print(f"Error creating run: {e}")
        raise


async def get_run(client: OpenAI, run_id, **kwargs):
    """
    Retrieve run details.

    Args:
        client (OpenAI): The OpenAI client instance.
        run_id (str): The ID of the run to retrieve.
        **kwargs: Additional arguments for retrieving the run.

    Returns:
        dict: The run's details.
    """
    try:
        run = await client.beta.runs.retrieve(run_id, **kwargs)
        return run
    except Exception as e:
        print(f"Error retrieving run with ID '{run_id}': {e}")
        raise


async def list_runs(client: OpenAI, **kwargs):
    """
    List all runs with optional filters.

    Args:
        client (OpenAI): The OpenAI client instance.
        **kwargs: Additional arguments for listing runs (e.g., order, limit).

    Returns:
        list: A list of runs.
    """
    try:
        runs = await client.beta.runs.list(**kwargs)
        return runs.data
    except Exception as e:
        print(f"Error listing runs: {e}")
        raise


async def delete_run(client: OpenAI, run_id, **kwargs):
    """
    Delete a run.

    Args:
        client (OpenAI): The OpenAI client instance.
        run_id (str): The ID of the run to delete.
        **kwargs: Additional arguments for the delete operation.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        response = await client.beta.runs.delete(run_id, **kwargs)
        return response
    except Exception as e:
        print(f"Error deleting run with ID '{run_id}': {e}")
        raise


async def create_streaming_run(client: OpenAI, thread_id, assistant_id, **kwargs):
    """
    Create a new streaming run.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to associate with the run.
        assistant_id (str): The ID of the assistant to use for the run.
        **kwargs: Additional arguments for the run creation.

    Returns:
        Async generator: A stream of events from the run.
    """
    try:
        stream = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            stream=True,
            **kwargs
        )
        return stream
    except Exception as e:
        print(
            f"Error creating streaming run for thread '{thread_id}' and assistant '{assistant_id}': {e}")
        raise


async def create_and_run_stream(client: OpenAI, assistant_id, thread_data, **kwargs):
    """
    Create and run a thread with streaming.

    Args:
        client (OpenAI): The OpenAI client instance.
        assistant_id (str): The ID of the assistant to use for the thread.
        thread_data (dict): The thread data, including messages.
        **kwargs: Additional arguments for the thread creation and run.

    Returns:
        Async generator: A stream of events from the thread run.
    """
    try:
        stream = client.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread=thread_data,
            stream=True,
            **kwargs
        )
        return stream
    except Exception as e:
        print(
            f"Error creating and running thread with assistant '{assistant_id}': {e}")
        raise


async def list_thread_runs(client: OpenAI, thread_id, **kwargs):
    """
    List all runs for a specific thread with optional filters.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to list runs for.
        **kwargs: Additional arguments for listing runs (e.g., order, limit).

    Returns:
        list: A list of runs for the specified thread.
    """
    try:
        runs = await client.beta.threads.runs.list(thread_id, **kwargs)
        return runs.data
    except Exception as e:
        print(f"Error listing runs for thread '{thread_id}': {e}")
        raise
