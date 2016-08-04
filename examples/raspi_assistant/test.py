# coding: utf-8
import os
import sys
import wave
import pyaudio
from io import BytesIO
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(HOME)

from raspi_assistant.utils import init_logging_handler
from raspi_assistant.handler import BaseHandler, ActionHandler


def main():
    logger = init_logging_handler()
    handler = BaseHandler()
    # func, result = handler.process(['今天天气怎么样', ])
    # result = handler.execute('weather_today', 'test')
    # print result
    handler.feedback('你好')
    # handler.audio_handler.play('err_audio.wav')
    # audio_handler = AudioHandler()
    # with open('err_audio.wav', 'rb') as f:
    #     audio = BytesIO()
    #     audio.write(f.read())
    # audio_handler.play(audio)
    
    # p = vlc.MediaPlayer("file:///path/to/track.mp3")

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
        print wf.getparams()
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

if __name__ == '__main__':
    main()
