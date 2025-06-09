# Filxe xy ly get history theo user id.

from libs.utils.json_curd import JsonCRUD


class MessageObject():
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class ChatHistoryProvider:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.jsondb = JsonCRUD(db_path)

    def create(self, record: dict, auto_id: bool = True):
        # Logic to create a record in the database
        self.jsondb.create(record, auto_id=auto_id)

    def read(self, user_id: str, chat_id: str) -> list[MessageObject]:
        # Logic to read records from the database and filter by user_id and chat_id
        records = self.jsondb.read_all()
        filtered_records = [
            record for record in records
            if record.get('user_id') == user_id and record.get('chat_id') == chat_id
        ]
        print(
            f"Filtered records for user_id={user_id}, chat_id={chat_id}: {filtered_records}")
        return [MessageObject(role=record['role'], content=record['content']) for record in filtered_records]
