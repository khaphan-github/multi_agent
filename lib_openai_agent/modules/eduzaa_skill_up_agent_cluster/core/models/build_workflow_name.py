def build_workflow_name(
    workflow_name: str,
    user_id: str,
    chat_id: str,
) -> str:
    """
    Build a workflow name based on the user ID and chat ID.

    Args:
      user_id (str): The ID of the user.
      chat_id (str): The ID of the chat.

    Returns:
      str: A formatted workflow name.
    """
    return f"{workflow_name}_{user_id}_{chat_id}"
