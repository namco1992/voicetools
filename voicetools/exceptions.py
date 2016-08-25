# coding: utf-8
from requests import RequestException


class RespError(RequestException):
    """The response status code is not 200"""


class APIError(RequestException):
    """Third-party API error occured."""


class RecognitionError(APIError):
    """The request for Baidu Voice ASR API failed."""


class VerifyError(APIError):
    """Auth failed."""


class QuotaError(APIError):
    """The number of requests exceeds the quota."""
