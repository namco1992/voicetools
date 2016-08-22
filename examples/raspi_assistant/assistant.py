# coding: utf-8
import os
import sys
import time

import RPi.GPIO as GPIO

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(HOME)

from raspi_assistant.settings import GPIOConfig
from raspi_assistant.utils import init_logging_handler
from raspi_assistant.handler import BaseHandler

logger = init_logging_handler()


def set_GPIO():
    GPIO.setmode(GPIO.BCM)
    set_voice_sensor()


def set_voice_sensor():
    GPIO.setup(GPIOConfig.VOICE_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIOConfig.VOICE_SENSOR, GPIO.FALLING)


def loop():
    # 初始化
    handler = BaseHandler()
    try:
        while True:
            # 下降沿检测
            if GPIO.event_detected(GPIOConfig.VOICE_SENSOR):
                GPIO.remove_event_detect(GPIOConfig.VOICE_SENSOR)
                handler.worker()
                GPIO.add_event_detect(GPIOConfig.VOICE_SENSOR, GPIO.FALLING)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    set_GPIO()
    loop()
