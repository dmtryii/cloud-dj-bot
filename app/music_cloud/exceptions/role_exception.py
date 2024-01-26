from rest_framework import status

from .exception_base import BaseCustomException


class RoleMediaLengthExceeded(BaseCustomException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status.HTTP_403_FORBIDDEN)


class RoleDelayBetweenDownloadsExceeded(BaseCustomException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status.HTTP_403_FORBIDDEN)
