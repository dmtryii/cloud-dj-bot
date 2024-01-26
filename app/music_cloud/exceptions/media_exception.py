from rest_framework import status

from .exception_base import BaseCustomException


class MediaNotFound(BaseCustomException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class MediaProfileNotFound(BaseCustomException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class MediaDownloadNotFound(BaseCustomException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND)
