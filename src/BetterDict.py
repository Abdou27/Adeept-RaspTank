

class BetterDict(dict):
    def __init__(self) -> None:
        super().__init__()

    def __getattr__(self, attr: str):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def __setattr__(self, attr: str, value) -> None:
        self[attr] = value

