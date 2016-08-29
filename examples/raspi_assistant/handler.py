# coding: utf-8
import logging
import traceback
import datetime
from tempfile import NamedTemporaryFile

import jieba
from voicetools import BaiduVoice, TuringRobot

from .settings import BasicConfig as BC, BaiduAPIConfig as BAC
from .utils import (
    AudioHandler, Keyword, cache, CacheHandler, timestamp, BaiduAPIClient,
    generate_response, convert_to_wav)

logger = logging.getLogger()

FUNC_MAP = {
    Keyword(['备忘录', ]).value: 'memo_today',
    Keyword(['提醒', ]).value: 'memo_today',
    Keyword(['备忘录', '今天']).value: 'memo_today',
    Keyword(['提醒', '今天']).value: 'memo_today',
    Keyword(['备忘录', '明天']).value: 'memo_tomo',
    Keyword(['提醒', '明天']).value: 'memo_tomo',
    Keyword(['备忘录', '播放']).value: 'play_memo_today',
    Keyword(['提醒', '播放']).value: 'play_memo_today',
    Keyword(['备忘录', '播放', '明天']).value: 'play_memo_tomo',
    Keyword(['提醒', '播放', '明天']).value: 'play_memo_tomo',
    Keyword(['备忘录', '删除']).value: 'del_all_memo',
    Keyword(['提醒', '删除']).value: 'del_all_memo',
    Keyword(['备忘录', '删除', '最后']).value: 'del_last_memo',
    Keyword(['提醒', '删除', '最后']).value: 'del_last_memo',
    Keyword(['备忘录', '删除', '第一条']).value: 'del_first_memo',
    Keyword(['提醒', '删除', '第一条']).value: 'del_first_memo',
    Keyword(['明天', '天气']).value: 'weather_tomo',
    Keyword(['今天', '天气']).value: 'weather_today'
}


class BaseHandler(object):

    def __init__(self, baidu_token=None):
        if not baidu_token:
            try:
                token = BaiduVoice.get_baidu_token(BC.VOICE_API_KEY, BC.VOICE_SECRET)
                self.token = token['access_token']
            except Exception, e:
                logger.warn('======Get baidu voice token failed, %s', traceback.format_exc())
                raise e
        else:
            self.token = baidu_token
        self.bv = BaiduVoice(self.token)
        self.audio_handler = AudioHandler()

    def __repr__(self):
        return '<BaseHandler>'

    def receive(self, sec=4):
        self.feedback(generate_response())
        self.audio_handler.arecord(sec)
        try:
            return self.bv.asr('record.wav')
        except Exception, e:
            logger.warn('======Baidu ASR failed, %s', traceback.format_exc())

    def process(self, results):
        seg_list = list(jieba.cut(results[0], cut_all=True))
        # command = Keyword(list(set(seg_list) & BC.KEYWORDS))
        command = Keyword(list(set((x.encode('utf-8') for x in seg_list)) & BC.KEYWORDS))
        logger.info('=======Recognition result: %s', command.value)
        return FUNC_MAP.get(command.value, 'default'), results[0]

    def execute(self, func_name, result):
        func = getattr(ActionHandler, func_name)
        return func(self, result)

    @cache
    def feedback(self, content=None):
        if content:
            try:
                data = NamedTemporaryFile()
                data.write(self.bv.tts(content))
                data.seek(0)
                convert_to_wav(data)
                data.close()
            except Exception, e:
                logger.warn('======Baidu TTS failed, %s', traceback.format_exc())
            else:
                self.audio_handler.aplay()

    def worker(self):
        try:
            results = self.receive()
            func, result = self.process(results)
            content = self.execute(func, result)
            self.feedback(content)
        except Exception, e:
            self.feedback('出现系统异常，请检查日志')


class ActionHandler(object):
    """docstring for ActionHandler"""

    @staticmethod
    def default(base_handler, result):
        print 'turing run'
        robot = TuringRobot(BC.TURING_KEY)
        try:
            content = robot.ask_turing(result)
        except Exception, e:
            logger.warn(traceback.format_exc())
            return '没有找到问题的答案'
        else:
            return content

    @staticmethod
    def _memo(date, base_handler):
        base_handler.feedback('请说出记录内容')
        audio = base_handler.audio_handler.arecord(6, is_buffer=True)
        cache_handler = CacheHandler()
        cache_handler.zset(date, audio, timestamp(), 86400*3)
        return '完成记录'

    @staticmethod
    def memo_today(base_handler, result):
        return ActionHandler._memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            base_handler=base_handler
            )

    @staticmethod
    def memo_tomo(base_handler, result):
        return ActionHandler._memo(
            date=(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            base_handler=base_handler
            )

    @staticmethod
    def play_memo(date, base_handler):
        cache_handler = CacheHandler()
        audio = cache_handler.zget(date, 0, -1)
        if audio:
            for item in audio:
                base_handler.audio_handler.aplay(item, is_buffer=True)
            return '播放结束'
        else:
            base_handler.feedback('未找到记录')
            return None

    @staticmethod
    def play_memo_tomo(base_handler, result):
        return ActionHandler.play_memo(
            date=(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            base_handler=base_handler
            )

    @staticmethod
    def play_memo_today(base_handler, result):
        return ActionHandler.play_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            base_handler=base_handler
            )

    @staticmethod
    def del_memo(date, start, end):
        cache_handler = CacheHandler()
        cache_handler.zdel(date, start, end)
        return '删除成功'

    @staticmethod
    def del_last_memo(base_handler, result):
        return ActionHandler.del_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            start=-1,
            end=-1
            )

    @staticmethod
    def del_first_memo(base_handler, result):
        return ActionHandler.del_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            start=0,
            end=0
            )

    @staticmethod
    def del_all_memo(base_handler, result):
        return ActionHandler.del_memo(
            date=datetime.date.today().strftime('%Y-%m-%d'),
            start=0,
            end=-1
            )

    @staticmethod
    def weather_tomo(base_handler, result):
        return ActionHandler.query_weather('tomo')

    @staticmethod
    def weather_today(base_handler, result):
        return ActionHandler.query_weather('today')

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
