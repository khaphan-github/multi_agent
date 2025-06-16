from openai import AsyncOpenAI as OpenAI


async def create_vector(client: OpenAI, vector_data):
    """
    Create a new vector.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_data (dict): Data required to create the vector.

    Returns:
        dict: The created vector's details.
    """
    try:
        vector_store = await client.vector_stores.create(**vector_data)
        return vector_store
    except Exception as e:
        print(f"Error creating vector: {e}")
        raise


async def update_vector(client: OpenAI, vector_store_id, update_data, **kwargs):
    """
    Update an existing vector store.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_store_id (str): The ID of the vector store to update.
        update_data (dict): Data to update the vector store.
        **kwargs: Additional arguments for updating the vector store.

    Returns:
        dict: The updated vector store's details.
    """
    try:
        vector_store = await client.vector_stores.update(
            vector_store_id=vector_store_id,
            **update_data,
            **kwargs
        )
        return vector_store
    except Exception as e:
        print(f"Error updating vector store with ID '{vector_store_id}': {e}")
        raise


async def delete_vector(client: OpenAI, vector_store_id, **kwargs):
    """
    Delete a vector store.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_store_id (str): The ID of the vector store to delete.
        **kwargs: Additional arguments for the delete operation.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        deleted_vector_store = await client.vector_stores.delete(
            vector_store_id=vector_store_id,
            **kwargs
        )
        return deleted_vector_store
    except Exception as e:
        print(f"Error deleting vector store with ID '{vector_store_id}': {e}")
        raise


async def get_vector(client: OpenAI, vector_store_id, **kwargs):
    """
    Retrieve vector store details.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_store_id (str): The ID of the vector store to retrieve.
        **kwargs: Additional arguments for retrieving the vector store.

    Returns:
        dict: The vector store's details.
    """
    try:
        vector_store = await client.vector_stores.retrieve(
            vector_store_id=vector_store_id,
            **kwargs
        )
        return vector_store
    except Exception as e:
        print(
            f"Error retrieving vector store with ID '{vector_store_id}': {e}")
        raise


async def list_vector_stores(client: OpenAI, **kwargs):
    """
    List all vector stores.

    Args:
        client (OpenAI): The OpenAI client instance.
        **kwargs: Additional arguments for listing vector stores.

    Returns:
        list: A list of vector stores.
    """
    try:
        vector_stores = await client.vector_stores.list(**kwargs)
        return vector_stores
    except Exception as e:
        print(f"Error listing vector stores: {e}")
        raise


async def create_vector_store_file(client: OpenAI, vector_store_id, file_id, **kwargs):
    """
    Create a file in a vector store.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_store_id (str): The ID of the vector store.
        file_id (str): The ID of the file to add to the vector store.
        **kwargs: Additional arguments for creating the file.

    Returns:
        dict: The created vector store file's details.
    """
    try:
        vector_store_file = await client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id,
            **kwargs
        )
        return vector_store_file
    except Exception as e:
        print(
            f"Error creating file in vector store with ID '{vector_store_id}': {e}")
        raise


async def list_vector_store_files(client: OpenAI, vector_store_id, **kwargs):
    """
    List all files in a vector store.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_store_id (str): The ID of the vector store.
        **kwargs: Additional arguments for listing files.

    Returns:
        list: A list of files in the vector store.
    """
    try:
        vector_store_files = await client.vector_stores.files.list(
            vector_store_id=vector_store_id,
            **kwargs
        )
        return vector_store_files
    except Exception as e:
        print(
            f"Error listing files in vector store with ID '{vector_store_id}': {e}")
        raise


async def retrieve_vector_store_file(client: OpenAI, vector_store_id, file_id, **kwargs):
    """
    Retrieve a file from a vector store.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_store_id (str): The ID of the vector store.
        file_id (str): The ID of the file to retrieve.
        **kwargs: Additional arguments for retrieving the file.

    Returns:
        dict: The retrieved vector store file's details.
    """
    try:
        vector_store_file = await client.vector_stores.files.retrieve(
            vector_store_id=vector_store_id,
            file_id=file_id,
            **kwargs
        )
        return vector_store_file
    except Exception as e:
        print(
            f"Error retrieving file with ID '{file_id}' from vector store with ID '{vector_store_id}': {e}")
        raise


async def delete_vector_store_file(client: OpenAI, vector_store_id, file_id, **kwargs):
    """
    Delete a file from a vector store.

    Args:
        client (OpenAI): The OpenAI client instance.
        vector_store_id (str): The ID of the vector store.
        file_id (str): The ID of the file to delete.
        **kwargs: Additional arguments for deleting the file.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        deleted_vector_store_file = await client.vector_stores.files.delete(
            vector_store_id=vector_store_id,
            file_id=file_id,
            **kwargs
        )
        return deleted_vector_store_file
    except Exception as e:
        print(
            f"Error deleting file with ID '{file_id}' from vector store with ID '{vector_store_id}': {e}")
        raise
