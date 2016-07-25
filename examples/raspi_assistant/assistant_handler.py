# coding: utf-8
import subprocess
import os
import datetime

from pydub import AudioSegment

from raspi_assistant.src.bll.voice_handler import text_to_audio, audio_to_text
from raspi_assistant.src.handler.base_handler import BaseHandler
from raspi_assistant.src.handler.action_handler import ActionHandler
from raspi_assistant.config import (
    Path, send_audio_file, receive_audio_file, RetCode, err_audio_file, Action
    )
from raspi_assistant.src.bll.get_answer_handler import get_answer, generate_response
from raspi_assistant.src.bll.weather_handler import query_weather


class AssistantHandler(BaseHandler):
    def __init__(self, arg):
        super(AssistantHandler, self).__init__()

    def wakeup(self):
        self.speak(content=generate_response())
        self.listen_and_response()

    def listen_and_response(self):
        print 'listening'
        action = None
        # listen
        ret, content = self.listen()
        print 'get_answer'
        # get answer
        if ret == RetCode.SUCCESS:
            content, action = get_answer(content)
        # speak and move
        if action:
            self.execute(action)
        else:
            self.speak(content)

    def execute(self, action):
        execution = getattr(ActionHandler, 'execute_'+action)
        if not execution:
            execution = ActionHandler.default_action
        execution(action)

    def make_memo(self):
        self.speak(content=u'好的，你想记点什么')
        record_time = datetime.datetime.now()
        now_record = '.'.join((record_time.strftime("%Y-%m-%d-%H%M%S"), 'wav'))
        today_record = '.'.join((record_time.strftime("%Y-%m-%d"), 'wav'))
        today_mp3_record = '.'.join((record_time.strftime("%Y-%m-%d"), 'mp3'))
        now_path = os.path.join(Path.VOICE_DIR, now_record)
        today_path = os.path.join(Path.VOICE_DIR, today_record)
        ret = self.record(now_path, 10)
        print 'record finished.'
        if ret != 0:
            self.speak()
            return
        if os.path.exists(today_path):
            # pydub拼接起来
            today = AudioSegment.from_wav(today_path)
            now = AudioSegment.from_wav(now_path)
            today += now
            today.export(os.path.join(Path.VOICE_DIR, today_mp3_record), format='mp3')
        else:
            os.rename(now_path, today_path)
        self.speak(content=u'录音完毕')
        return
