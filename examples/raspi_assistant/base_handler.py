# coding: utf-8
import subprocess
import os
import datetime

from pydub import AudioSegment

from raspi_assistant.bll.voice_handler import text_to_audio, audio_to_text
from raspi_assistant.config import (
    Path, send_audio_file, receive_audio_file, RetCode, err_audio_file, Action
    )
from raspi_assistant.bll.get_answer_handler import get_answer, generate_response
from raspi_assistant.bll.weather_handler import query_weather


class BaseHandler(object):

    def listen(self):
        # recording
        ret = self.record(os.path.join(Path.VOICE_DIR, send_audio_file), 4)
        print 'record finished.'
        if ret != 0:
            return RetCode.SERVER_ERR, 'there is something wrong, try again.'
        else:
            # audio_to_text
            ret, content = audio_to_text()
            print ret, content
            return ret, content[:-1]

    def speak(self, content=None):
        if not content:
            self.play_audio(os.path.join(Path.VOICE_DIR, err_audio_file))
            return
        ret = self.get_audio(content)
        if ret != RetCode.SUCCESS:
            self.play_audio(os.path.join(Path.VOICE_DIR, err_audio_file))
        else:
            self.play_audio(os.path.join(Path.VOICE_DIR, receive_audio_file))

    def get_audio(self, content):
        # get audio from redis or
        # text_to_audio
        return text_to_audio(content)

    def move(self):
        pass

    def forward(self):
        pass

    def backward(self):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def record(self, file_path, duration):
        return subprocess.call('arecord -D "plughw:1,0" -d %d -f S16_LE -c1 -r16000 %s' % (duration, file_path), shell=True)

    def play_audio(self, file_path):
        subprocess.call('mpg123 %s' % file_path, shell=True)

    def play_wav(self, file_path):
        subprocess.call('omxplayer -o local %s' % file_path, shell=True)
