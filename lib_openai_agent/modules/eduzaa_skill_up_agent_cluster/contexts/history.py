# Filxe xy ly get history theo user id.

from libs.utils.json_curd import JsonCRUD


class MessageObject():
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_string(self):
        return f"{self.role.capitalize()}: {self.content} \n"


class ChatHistoryProvider:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.jsondb = JsonCRUD(db_path)
        self.jsondb.clear_all()

    def create(self, record: dict, auto_id: bool = True):
        # Logic to create a record in the database
        self.jsondb.create(record, auto_id=auto_id)

    def read(self, user_id: str, chat_id: str) -> list[str]:
        # Logic to read records from the database and filter by user_id and chat_id
        records = self.jsondb.read_all()
        filtered_records = records
        return [MessageObject(role=record['role'], content=record['content']).to_string() for record in filtered_records]
