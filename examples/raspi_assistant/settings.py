# coding: utf-8
import os
import logging
# audio file name config
receive_audio_file = 'receive_audio.mp3'
send_audio_file = 'send_audio.wav'
err_audio_file = 'err_audio.mp3'


class RedisConfig(object):
    """docstring for RedisConfig"""
    HOST_ADDR = 'localhost'
    PORT = 6379
    DB = 0
    SOCKET_TIMEOUT = 1

# emotion config
happiness_threshold = 0.6


class GPIO_Config(object):
    """GPIO config"""
    VOICE_SENSOR = 4


class Path(object):
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(PROJECT_DIR, 'log')
    VOICE_DIR = os.path.join(PROJECT_DIR, 'voice')


class Action(object):
    Memo = 'memo'
    PlayMemo = 'play_memo'
    WeatherTomorrow = 'weather_tomo'
    WeatherToday = 'weather_today'


class LogConfig(object):
    LOGGING_FORMAT = '%(asctime)s %(funcName)s:%(lineno)d [%(levelname)s] %(message)s'
    LOGGING_LOCATION = './log/raspi_assistant.log'
    LOGGING_LEVEL = logging.DEBUG


class ConsName(object):
    BAIDU_TOKEN = 'baidu_token'
