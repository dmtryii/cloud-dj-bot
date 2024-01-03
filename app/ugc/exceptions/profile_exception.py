
class ProfileNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ProfileRoleNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
