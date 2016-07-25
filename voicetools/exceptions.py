# coding: utf-8
from requests import RequestException


class RespError(RequestException):
    """The response status code is not 200"""


class APIError(RequestException):
    """Third-party API error occured."""


class RecognitionError(APIError):
    """Third-party API error occured."""


class VerifyError(APIError):
    """Third-party API error occured."""


class QuotaError(APIError):
    """Third-party API error occured."""
