from typing import Union

from src.BetterDict import BetterDict


class Message(BetterDict):
    def __init__(self, **options) -> None:
        super().__init__()

        self.sender = options.get("sender", None)
        self.receiver = options.get("receiver", None)
        self.message_type = None
        # self.payload = None

    def __str__(self):
        return f"{self.message_type}:{self.sender}:{self.receiver}"

    def send(self):
        with Socket.get_socket() as s:
            s.connect(self.receiver)
            s.send(str(self))
