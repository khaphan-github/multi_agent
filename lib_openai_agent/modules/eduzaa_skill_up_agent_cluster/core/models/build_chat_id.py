import uuid


def build_chat_id():
    """
    Build a chat ID based on a generated UUID.

    Returns:
      str: A formatted chat ID.
    """
    return 'ag_chat_' + str(uuid.uuid4())
