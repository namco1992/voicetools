# coding: utf-8
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import random
import base64
from functools import wraps
from hashlib import md5
from subprocess import Popen, PIPE
from io import BytesIO
from tempfile import NamedTemporaryFile

import redis
import pyaudio
import wave
from voicetools import BaseClient, APIError

from .settings import (
    LogConfig as LC, RedisConfig as RC, BaiduAPIConfig as BAC,
    BasicConfig as BC, ErrNo)

conn_pool = redis.ConnectionPool(host=RC.HOST_ADDR, port=RC.PORT, db=RC.DB)


def convert_to_wav(file_):
    p = Popen(['ffmpeg', '-y', '-i', '-', '-f', 'wav', 'output.wav'], stdin=file_ , stdout=None, stderr=None)
    p.wait()


def init_logging_handler():
    handler = TimedRotatingFileHandler(LC.LOGGING_LOCATION, when='MIDNIGHT')
    formatter = logging.Formatter(LC.LOGGING_FORMAT)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(LC.LOGGING_LEVEL)
    logger.addHandler(handler)
    return logger


def generate_response():
    if random.random() <= BC.HAPPINESS_THRESHOLD:
        return BC.POSITIVE_ANSWER[random.randint(1, len(BC.POSITIVE_ANSWER))]
    else:
        return BC.NEGATIVE_ANSWER[random.randint(1, len(BC.NEGATIVE_ANSWER))]


def unique_id(func, args, kwargs):
    return md5(func.__name__ + repr(args) + repr(kwargs)).hexdigest()


def timestamp():
    return int(time.time() * 1000)


def cache(func):
    @wraps(func)
    def _(*args, **kwargs):
        cache_handler = CacheHandler()
        id_ = unique_id(func, *args, **kwargs)
        print id_
        cache = cache_handler.get(id_)
        if cache:
            print 'cached'
            audio_handler = AudioHandler()
            audio_handler.aplay(base64.b64decode(cache))
            # return cache
        else:
            print 'set cache'
            func(*args, **kwargs)
            with open('output.wav', 'rb') as f:
                encoded_audio = base64.b64encode(f.read())
                cache_handler.set(id_, encoded_audio, 86400*7)
            # return buffer_
    return _


class BaiduAPIClient(BaseClient):
    """docstring for BaiduAPIClient"""
    def __init__(self, **kwargs):
        super(BaiduAPIClient, self).__init__(**kwargs)
        self.apikey = BAC.API_KEY
        self.headers = {'apikey': self.apikey}

    def request_handler(self, url, params):
        try:
            resp = self.get_request(
                url=url,
                params=params,
                headers=self.headers)
        except Exception, e:
            raise e
        content = resp.json()
        if 'errNum' in content:
            err_msg = 'err_msg: %s' % content.get('errMsg', 'baidu api unknown error')
            raise ErrNo.ExceptionMap.get(content['errNum'][:4], APIError)(err_msg)
        else:
            return content

    def heweather(self):
        try:
            content = self.request_handler(
                url=BAC.WEATHER_URL,
                params={'city': BC.LOCATION})
        except Exception, e:
            raise e
        weather_info = content['HeWeather data service 3.0'][0]
        if weather_info['status'] != 'ok':
            raise APIError('query weather api failed.')
        return weather_info


class AudioHandler(object):
    """docstring for AudioHandler"""
    def __init__(self, chunk=1024, format_=pyaudio.paInt16, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = format_
        self.CHANNELS = channels
        self.RATE = rate

    def record(self, record_seconds, file_):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        input_device_index=0,
                        frames_per_buffer=self.CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * record_seconds)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(file_, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(''.join(frames))
        wf.close()

    def arecord(self, record_seconds, is_buffer=False, file_=BC.INPUT_NAME):
        if is_buffer:
            p = Popen(
                ['arecord', '-r', '16000', '-D', 'plughw:1,0', '-f', 'S16_LE', '-d', str(record_seconds), '-'],
                stdout=PIPE,
                stderr=PIPE)
            stdout, _ = p.communicate()
            return stdout
        else:
            p = Popen(
                ['arecord', '-r', '16000', '-D', 'plughw:1,0', '-f', 'S16_LE', '-d', str(record_seconds), file_])
            p.wait()

    def aplay(self, is_buffer=False, file_=BC.OUTPUT_NAME):
        if is_buffer:
            p = Popen(['aplay', '-'], stdin=file_)
        else:
            p = Popen(['aplay', file_])
        p.wait()

    def play(self, file_):
        wf = wave.open(file_, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(self.CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(self.CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()


class Keyword(object):
    """docstring for Keyword"""
    def __init__(self, list_):
        list_.sort()
        self.keywords = list_
        self.value = '/'.join(list_)


class CacheHandler(object):
    """docstring for CacheHandler"""
    def __init__(self):
        self.client = redis.StrictRedis(
            connection_pool=conn_pool, socket_timeout=RC.SOCKET_TIMEOUT)

    def set(self, name, value, ttl=None):
        if ttl:
            self.client.setex(name, ttl, value)
        else:
            self.client.set(name, value)

    def get(self, name):
        return self.client.get(name)

    def delete(self, name):
        return self.client.delete(name)

    def expire(self, name, ttl):
        return self.client.expire(name, ttl)

    def zset(self, name, key, score, ttl=None, is_audio=True):
        if is_audio:
            key = base64.b64encode(key)
        if ttl:
            pipeline = self.client.pipeline()
            pipeline.zadd(name, score, key)
            pipeline.expire(name, ttl)
            return pipeline.execute()
        else:
            self.client.zadd(name, score, key)

    def zget(self, name, start, end, is_audio=True):
        ret = self.client.zrange(name, start, end)
        if is_audio:
            return base64.b64decode(ret)
        else:
            return ret

    def zdel(self, name, start, end):
        # zremrangebyrank
        return self.client.zremrangebyrank(name, start, end)
