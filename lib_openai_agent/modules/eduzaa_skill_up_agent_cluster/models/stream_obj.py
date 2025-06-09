class StreamObj:
    def __init__(self, message: str, id: str = None):
        self.message = message
        self.id = id
    def to_dict(self) -> dict:
        """
        Converts the StreamObj to a dictionary representation.

        :return: A dictionary containing the message and ID.
        """
        return {
            "message": self.message,
            "id": self.id
        }