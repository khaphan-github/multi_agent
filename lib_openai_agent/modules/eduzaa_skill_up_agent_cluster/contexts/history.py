# Filxe xy ly get history theo user id.

class MessageObject():
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class ChatHistoryProvider:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create(self, record: dict, auto_id: bool = True):
        # Logic to create a record in the database
        pass

    def read(self, user_id: str, chat_id: str) -> list[MessageObject]:
        # Logic to read records from the database
        return []
