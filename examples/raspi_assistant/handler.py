# coding: utf-8
import logging
import traceback
from io import BytesIO
import datetime

import jieba
from voicetools import BaiduVoice, TuringRobot

from .settings import BasicConfig as BC, BaiduAPIConfig as BAC
from .utils import (
    AudioHandler, Keyword, cache, CacheHandler, timestamp, BaiduAPIClient,
    generate_response)

logger = logging.getLogger()


class BaseHandler(object):

    def __init__(self):
        self.token = BaiduVoice.get_baidu_token(BC.VOICE_API_KEY, BC.VOICE_SECRET)
        self.bv = BaiduVoice(self.token)
        self.audio_handler = AudioHandler()

    def receive(self, sec=6):
        f = BytesIO()
        self.audio_handler.record(sec, f)
        self.feedback(generate_response())
        return self.bv.asr(f)

    def process(self, results):
        seg_list = jieba.cut(results[0])
        command = Keyword(list(set(seg_list) & BC.KEYWORDS))
        return BC.FUNC_MAP.get(command.value, ActionHandler.default), results[0]

    def execute(self, func, bv, audio_handler):
        return func(bv, audio_handler)

    @cache
    def feedback(self, content=None):
        if content:
            audio = self.bv.tts(content)
        self.audio_handler.play(audio)

    def worker(self):
        results = self.receive()
        func, command = self.process(results)
        content = self.execute(func, self.bv, self.audio_handler, command)
        self.feedback(content)


class ActionHandler(object):
    """docstring for ActionHandler"""

    @staticmethod
    def default(bv, audio_handler, command):
        robot = TuringRobot(BC.TURING_KEY)
        try:
            content = robot.ask_turing(command)
        except Exception, e:
            logger.warn(traceback.format_exc())
            return '没有找到问题的答案'
        else:
            return content

    @staticmethod
    def _memo(date, bv, audio_handler):
        audio_handler.play(bv.tts('请说出内容'))
        f = BytesIO()
        audio_handler.record(6, f)
        cache_handler = CacheHandler()
        cache_handler.zset(date, f.read(), timestamp)
        return '完成记录'

    @staticmethod
    def memo_today(bv, audio_handler):
        return ActionHandler._memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            bv=bv,
            audio_handler=audio_handler
            )

    @staticmethod
    def memo_tomo(bv, audio_handler):
        return ActionHandler._memo(
            date=(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            bv=bv,
            audio_handler=audio_handler
            )

    @staticmethod
    def play_memo(date, audio_handler):
        cache_handler = CacheHandler()
        audio = cache_handler.zget(date, 0, -1)
        if audio:
            for item in audio:
                audio_handler.play(audio)
            return '播放结束'
        else:
            audio_handler.play('未找到记录')
            return None

    @staticmethod
    def play_memo_tomo(bv, audio_handler):
        return ActionHandler.play_memo(
            date=(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            audio_handler=audio_handler
            )

    @staticmethod
    def play_memo_today(bv, audio_handler):
        return ActionHandler.play_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            audio_handler=audio_handler
            )

    @staticmethod
    def del_memo(date, start, end):
        cache_handler = CacheHandler()
        cache_handler.zdel(date, start, end)
        return '删除成功'

    @staticmethod
    def del_last_memo(bv, audio_handler):
        return ActionHandler.del_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            start=-1,
            end=-1
            )

    @staticmethod
    def del_first_memo(bv, audio_handler):
        return ActionHandler.del_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            start=0,
            end=0
            )

    @staticmethod
    def del_all_memo(bv, audio_handler):
        return ActionHandler.del_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            start=0,
            end=-1
            )

    @staticmethod
    def weather_tomo(bv, audio_handler):
        return ActionHandler.query_weather('today')

    @staticmethod
    def weather_today(bv, audio_handler):
        return ActionHandler.query_weather('tomo')

    @staticmethod
    def query_weather(today_or_tomo):
        client = BaiduAPIClient()
        try:
            content = client.heweather()
        except Exception, e:
            logger.warn(traceback.format_exc())
            return '查询天气失败，请检查日志'
        if today_or_tomo == 'today':
            now_weather = content.get('now')
            today_weather = content.get('daily_forecast')[0]
            text = BAC.TODAY_WEATHER_TEXT.format(
                cond=now_weather['cond']['txt'],
                fl=now_weather['fl'],
                hum=now_weather['hum'],
                min=today_weather['tmp']['min'],
                max=today_weather['tmp']['max'],
                txt_d=today_weather['cond']['txt_d'],
                txt_n=today_weather['cond']['txt_n'],
                pop=today_weather['pop'],
                qlty=content['aqi']['city']['aqi']
                )
        elif today_or_tomo == 'tomo':
            tomo_weather = content.get('daily_forecast')[1]
            text = BAC.TOMO_WEATHER_TEXT.format(
                min=tomo_weather['tmp']['min'],
                max=tomo_weather['tmp']['max'],
                txt_d=tomo_weather['cond']['txt_d'],
                txt_n=tomo_weather['cond']['txt_n'],
                pop=tomo_weather['pop']
                )
        else:
            return '查询天气失败，请检查日志'
        return text
