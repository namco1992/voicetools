# coding: utf-8
import logging

from voicetools import (
    APIError, RespError, RecognitionError, VerifyError, QuotaError)

from .utils import Keyword


class RedisConfig(object):
    """docstring for RedisConfig"""
    HOST_ADDR = 'localhost'
    PORT = 6379
    DB = 0
    SOCKET_TIMEOUT = 1


class BasicConfig(object):
    LOCATION = '成都'
    TURING_KEY = 'turingkey'
    VOICE_API_KEY = 'key'
    VOICE_SECRET = 'secret'
    HAPPINESS_THRESHOLD = 0.6
    KEYWORDS = {u'提醒', u'备忘录', u'播放', u'今天', u'明天', u'天气'}
    POSITIVE_ANSWER = {
        1: u'等候多时',
        2: u'你回来了',
        3: u'我听到你说的了',
        4: u'今天工作辛苦吗',
        5: u'你今天又变帅了',
        6: u'需要我帮你做点什么？'
    }
    # The negative_answer won't negative your command, just the emotion expression
    NEGATIVE_ANSWER = {
        1: '别吵了，真烦人',
        2: '好了好了，我听见了',
        3: '我今天心情不太好',
        4: '我想静静，也别问我静静是谁',
        5: '每天都来烦我，你什么时候给我找个男朋友'
    }
    FUNC_MAP = {
        Keyword([u'备忘录', ]).value: 'a',
        Keyword([u'提醒', ]).value: 'b',
        Keyword([u'备忘录', u'播放']).value: 'c',
        Keyword([u'明天', u'天气']).value: 'd',
        Keyword([u'今天', u'天气']).value: 'e'
    }


class GPIOConfig(object):
    """GPIO config"""
    VOICE_SENSOR = 4


class LogConfig(object):
    LOGGING_FORMAT = '%(asctime)s %(funcName)s:%(lineno)d [%(levelname)s] %(message)s'
    LOGGING_LOCATION = './log/raspi_assistant.log'
    LOGGING_LEVEL = logging.DEBUG


class BaiduAPIConfig(object):
    API_KEY = 'apikey'
    WEATHER_URL = 'http://apis.baidu.com/heweather/weather/free'
    TODAY_WEATHER_TEXT = \
    u'当前天气{cond}，体感温度{fl}摄氏度，空气湿度百分之{hum}。今日温度为{min}到{max}摄氏度，{txt_d}转{txt_n}，降水概率百分之{pop}，空气质量{qlty}。'

    TOMO_WEATHER_TEXT = \
        u'明天的气温是{min}到{max}摄氏度，{txt_d}转{txt_n}，降水概率百分之{pop}。'


class ErrNo(object):
    ExceptionMap = {
        3001: QuotaError,
        3002: VerifyError,
        3303: APIError,
    }
