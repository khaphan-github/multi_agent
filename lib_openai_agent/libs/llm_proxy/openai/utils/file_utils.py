from openai import AsyncOpenAI as OpenAI

# https://platform.openai.com/docs/api-reference/files


async def create_file(client: OpenAI, **kwargs):
    """
    Create a new file.

    Args:
        client (OpenAI): The OpenAI client instance.
        **kwargs: Dynamic input values for file creation.
    """
    return await client.files.create(**kwargs)


async def delete_file(client: OpenAI, file_id, **kwargs):
    """
    Delete a file.

    Args:
        client (OpenAI): The OpenAI client instance.
        file_id (str): The ID of the file to delete.
        **kwargs: Additional input values for file deletion.
    """
    return await client.files.delete(file_id, **kwargs)


async def get_file(client: OpenAI, file_id, **kwargs):
    """
    Retrieve file details.

    Args:
        client (OpenAI): The OpenAI client instance.
        file_id (str): The ID of the file to retrieve.
        **kwargs: Additional input values for file retrieval.
    """
    return await client.files.retrieve(file_id, **kwargs)


async def list_files(client: OpenAI, **kwargs):
    """
    List all files.

    Args:
        client (OpenAI): The OpenAI client instance.
        **kwargs: Additional input values for listing files.
    """
    return await client.files.list(**kwargs)
