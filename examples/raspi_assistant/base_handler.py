# coding: utf-8
import subprocess
import os

import redis
from voicetools import BaiduVoice

from .get_answer_handler import get_answer, generate_response
from .weather_handler import query_weather
from .settings import RedisConfig as RC
from .utils import AudioHandler

conn_pool = redis.ConnectionPool(host=RC.HOST_ADDR, port=RC.PORT, db=RC.DB)


class BaseHandler(object):
    """docstring for BaseHandler"""


    def get_audio(self, content):
        # get audio from redis or
        # text_to_audio
        return text_to_audio(content)

    def record(self, file_path, duration):
        return subprocess.call('arecord -D "plughw:1,0" -d %d -f S16_LE -c1 -r16000 %s' % (duration, file_path), shell=True)

    def play_audio(self, file_path):
        subprocess.call('mpg123 %s' % file_path, shell=True)

    def play_wav(self, file_path):
        subprocess.call('omxplayer -o local %s' % file_path, shell=True)


class MainHandler(BaseHandler):

    def __init__(self, api_key, secret_key):
        self.redis_client = redis.StrictRedis(
            connection_pool=conn_pool, socket_timeout=RC.SOCKET_TIMEOUT)
        self.token = BaiduVoice.get_baidu_token(api_key, secret_key)
        self.bv = BaiduVoice(self.token)
        self.audio_handler = AudioHandler()

    def receive(self):
        self.audio_handler.record(6, )
        return self.bv.asr()

    def process(self):
        pass

    def execute(self):
        pass

    def feedback(self):
        pass

