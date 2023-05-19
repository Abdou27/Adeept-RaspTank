from typing import Union


class Message(dict):
    def __init__(self) -> None:
        super().__init__()
        self.sender_ip = None
        self.receiver_ip = None
        self.message_type = None
        self.payload = None

    def __getattr__(self, attr: str) -> Union[str, dict]:
        if attr in self:
            return self[attr]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def __setattr__(self, attr: str, value: Union[str, dict]) -> None:
        self[attr] = value

