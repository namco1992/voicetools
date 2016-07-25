# coding: utf-8
import os
import datetime

from raspi_assistant.src.handler.assistant_handler import AssistantHandler
from raspi_assistant.config import (
    Path, send_audio_file, receive_audio_file, RetCode, err_audio_file, Action
    )
from raspi_assistant.src.bll.weather_handler import query_weather


class ActionHandler(object):

    @classmethod
    def default_action(cls):
        pass

    @classmethod
    def execute_record(cls, action):
        assistant = AssistantHandler()
        return assistant.make_memo()

    @classmethod
    def execute_play_record(cls, action):
        assistant = AssistantHandler()
        today_record = '.'.join((str(datetime.date.today()), 'mp3'))
        assistant.play_audio(os.path.join(Path.VOICE_DIR, today_record))

    @classmethod
    def execute_weather_tomo(cls, action):
        assistant = AssistantHandler()
        ret, content = query_weather(Action.WeatherTomorrow)
        assistant.speak(content)

    @classmethod
    def execute_weather_today(cls, action):
        assistant = AssistantHandler()
        ret, content = query_weather(Action.WeatherToday)
        assistant.speak(content)
