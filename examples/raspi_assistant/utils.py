# coding: utf-8
import logging

import pyaudio
import wave
from logging.handlers import TimedRotatingFileHandler
from .settings import LogConfig as LC


def init_logging_handler():
    handler = TimedRotatingFileHandler(LC.LOGGING_LOCATION, when='MIDNIGHT')
    # handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LC.LOGGING_FORMAT)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(LC.LOGGING_LEVEL)
    logger.addHandler(handler)
    return logger


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
        wf.writeframes(b''.join(frames))
        wf.close()

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


class ActionHandler(object):

    @staticmethod
    def memo():
        return assistant.make_memo()

    @staticmethod
    def play_memo():
        today_record = '.'.join((str(datetime.date.today()), 'mp3'))
        assistant.play_audio(os.path.join(Path.VOICE_DIR, today_record))

    @staticmethod
    def weather_tomo():
        ret, content = query_weather(Action.WeatherTomorrow)
        assistant.speak(content)

    @staticmethod
    def weather_today():
        ret, content = query_weather(Action.WeatherToday)
        assistant.speak(content)


class Keyword(object):
    """docstring for Keyword"""
    def __init__(self, list_):
        list_.sort()
        self.value = '/'.join(list_)
