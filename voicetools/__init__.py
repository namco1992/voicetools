# -*- coding: utf-8 -*-
"""
voicetools library
=====================


"""
__title__ = 'voicetools'
__version__ = '0.0.1'
__author__ = 'namco1992'
__license__ = 'Apache 2.0'

from .api import Wolfram, TuringRobot, BaiduVoice
from .clients import BaseClient
from . import utils
from .exceptions import (
    APIError, RespError, RecognitionError, VerifyError, QuotaError)
