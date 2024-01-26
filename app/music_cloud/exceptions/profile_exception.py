from rest_framework import status

from .exception_base import BaseCustomException


class ProfileNotFound(BaseCustomException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class ProfileRoleNotFound(BaseCustomException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND)
