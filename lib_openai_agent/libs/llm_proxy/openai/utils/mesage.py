from openai import AsyncOpenAI as OpenAI


async def create_message(client: OpenAI, thread_id, role, content, **kwargs):
    """
    Create a new message in a thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to add the message to.
        role (str): The role of the message sender (e.g., "user", "assistant").
        content (str): The content of the message.
        **kwargs: Additional arguments for the message creation.

    Returns:
        dict: The created message's details.
    """
    try:
        message = await client.beta.threads.messages.create(
            thread_id,
            role=role,
            content=content,
            **kwargs
        )
        return message
    except Exception as e:
        print(f"Error creating message in thread '{thread_id}': {e}")
        raise


async def list_messages(client: OpenAI, thread_id, **kwargs):
    """
    List all messages in a thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to list messages for.
        **kwargs: Additional arguments for listing messages.

    Returns:
        list: A list of messages in the thread.
    """
    try:
        messages = await client.beta.threads.messages.list(thread_id, **kwargs)
        return messages.data
    except Exception as e:
        print(f"Error listing messages in thread '{thread_id}': {e}")
        raise


async def retrieve_message(client: OpenAI, thread_id, message_id, **kwargs):
    """
    Retrieve a specific message in a thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread containing the message.
        message_id (str): The ID of the message to retrieve.
        **kwargs: Additional arguments for retrieving the message.

    Returns:
        dict: The retrieved message's details.
    """
    try:
        message = await client.beta.threads.messages.retrieve(
            thread_id=thread_id,
            message_id=message_id,
            **kwargs
        )
        return message
    except Exception as e:
        print(
            f"Error retrieving message with ID '{message_id}' in thread '{thread_id}': {e}")
        raise


async def update_message(client: OpenAI, thread_id, message_id, metadata, **kwargs):
    """
    Update a specific message in a thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread containing the message.
        message_id (str): The ID of the message to update.
        metadata (dict): Metadata to update the message with.
        **kwargs: Additional arguments for updating the message.

    Returns:
        dict: The updated message's details.
    """
    try:
        updated_message = await client.beta.threads.messages.update(
            thread_id=thread_id,
            message_id=message_id,
            metadata=metadata,
            **kwargs
        )
        return updated_message
    except Exception as e:
        print(
            f"Error updating message with ID '{message_id}' in thread '{thread_id}': {e}")
        raise


async def delete_message(client: OpenAI, thread_id, message_id, **kwargs):
    """
    Delete a specific message in a thread.

    Args:
        client (OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread containing the message.
        message_id (str): The ID of the message to delete.
        **kwargs: Additional arguments for deleting the message.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        deleted_message = await client.beta.threads.messages.delete(
            thread_id=thread_id,
            message_id=message_id,
            **kwargs
        )
        return deleted_message
    except Exception as e:
        print(
            f"Error deleting message with ID '{message_id}' in thread '{thread_id}': {e}")
        raise
