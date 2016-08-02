# coding: utf-8
import subprocess
import logging
import os
from io import BytesIO
from functools import wraps

import jieba
import redis
from voicetools import BaiduVoice, TuringRobot

from .get_answer_handler import get_answer, generate_response
from .weather_handler import query_weather
from .settings import RedisConfig as RC, Action
from .utils import AudioHandler, Keyword
from .constants import FUNC_MAP, KEYWORDS

conn_pool = redis.ConnectionPool(host=RC.HOST_ADDR, port=RC.PORT, db=RC.DB)
logger = logging.getLogger()


class BaseHandler(object):
    """docstring for BaseHandler"""

    @staticmethod
    def cache_wrapper(self, func):
        @wraps(func)
        def _(content):
            # self.redis_client
            return _


class MainHandler(BaseHandler):

    def __init__(self, api_key, secret_key):
        self.redis_client = redis.StrictRedis(
            connection_pool=conn_pool, socket_timeout=RC.SOCKET_TIMEOUT)
        self.token = BaiduVoice.get_baidu_token(api_key, secret_key)
        self.bv = BaiduVoice(self.token)
        self.audio_handler = AudioHandler()

    def receive(self):
        f = BytesIO()
        self.audio_handler.record(6, f)
        return self.bv.asr(f)

    def process(self, results):
        seg_list = jieba.cut(results[0])
        command = Keyword(list(set(seg_list) & KEYWORDS))
        return FUNC_MAP.get(command.value, None)

    def execute(self, func):
        return func()

    @BaseHandler.cache_wrapper
    def feedback(self, content):
        if content:
            audio = self.bv.tts(content)
        else:
            audio = self.bv.tts('默认')
        self.audio_handler.play(audio)

    def worker(self):
        results = self.receive()
        func = self.process(results)
        content = self.execute(func)
        self.feedback(content)
