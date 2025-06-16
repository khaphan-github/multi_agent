from openai import AsyncOpenAI as OpenAI


async def create_thread(client: OpenAI, thread_data):
    """
    Create a new thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_data (dict): Data required to create the thread.

    Returns:
        dict: The created thread's details.
    """
    try:
        thread = await client.beta.threads.create(**thread_data)
        return thread
    except Exception as e:
        print(f"Error creating thread: {e}")
        raise


async def update_thread(client: OpenAI, thread_id, update_data):
    """
    Update an existing thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to update.
        update_data (dict): Data to update the thread.

    Returns:
        dict: The updated thread's details.
    """
    try:
        updated_thread = await client.beta.threads.update(thread_id, **update_data)
        return updated_thread
    except Exception as e:
        print(f"Error updating thread with ID '{thread_id}': {e}")
        raise


async def delete_thread(client: OpenAI, thread_id):
    """
    Delete a thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to delete.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        response = await client.beta.threads.delete(thread_id)
        return response
    except Exception as e:
        print(f"Error deleting thread with ID '{thread_id}': {e}")
        raise


async def get_thread(client: OpenAI, thread_id):
    """
    Retrieve thread details.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to retrieve.

    Returns:
        dict: The thread's details.
    """
    try:
        thread = await client.beta.threads.retrieve(thread_id)
        return thread
    except Exception as e:
        print(f"Error retrieving thread with ID '{thread_id}': {e}")
        raise
