from openai import AsyncOpenAI as OpenAI


async def create_assistant(client: OpenAI, **kwargs):
    """
    Create a new assistant.

    Args:
        client (OpenAI): The OpenAI client instance.
        assistant_data (dict): Data required to create the assistant, including:
            - instructions (str): Instructions for the assistant.
            - name (str): Name of the assistant.
            - tools (list): List of tools the assistant can use.
            - model (str): Model to use for the assistant.

    Returns:
        dict: The created assistant's details.
    """
    try:
        assistant = await client.beta.assistants.create(**kwargs)
        return assistant
    except Exception as e:
        print(f"Error creating assistant: {e}")
        raise


async def update_assistant(client: OpenAI, assistant_id, **kwargs):
    """
    Update an existing assistant.

    Args:
        client (OpenAI): The OpenAI client instance.
        assistant_id (str): The ID of the assistant to update.
        update_data (dict): Data to update the assistant, including:
            - instructions (str): Updated instructions for the assistant.
            - name (str): Updated name of the assistant.
            - tools (list): Updated list of tools the assistant can use.
            - model (str): Updated model to use for the assistant.

    Returns:
        dict: The updated assistant's details.
    """
    try:
        updated_assistant = await client.beta.assistants.update(assistant_id, **kwargs)
        return updated_assistant
    except Exception as e:
        print(f"Error updating assistant with ID '{assistant_id}': {e}")
        raise


async def delete_assistant(client: OpenAI, assistant_id):
    """
    Delete an assistant.

    Args:
        client (OpenAI): The OpenAI client instance.
        assistant_id (str): The ID of the assistant to delete.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        response = await client.beta.assistants.delete(assistant_id)
        return response
    except Exception as e:
        print(f"Error deleting assistant with ID '{assistant_id}': {e}")
        raise


async def get_assistant(client: OpenAI, assistant_id):
    """
    Retrieve assistant details.

    Args:
        client (OpenAI): The OpenAI client instance.
        assistant_id (str): The ID of the assistant to retrieve.

    Returns:
        dict: The assistant's details.
    """
    try:
        assistant = await client.beta.assistants.retrieve(assistant_id)
        return assistant
    except Exception as e:
        print(f"Error retrieving assistant with ID '{assistant_id}': {e}")
        raise


async def list_assistants(client: OpenAI, **kwargs):
    """
    List all assistants with optional filters.

    Args:
        client (OpenAI): The OpenAI client instance.
        **kwargs: Additional arguments for listing assistants (e.g., order, limit).

    Returns:
        list: A list of assistants.
    """
    try:
        assistants = await client.beta.assistants.list(**kwargs)
        return assistants.data
    except Exception as e:
        print(f"Error listing assistants: {e}")
        raise
