
class MediaNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class MediaProfileNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
