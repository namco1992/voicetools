# coding: utf-8
import os
import sys
import logging
import time

import RPi.GPIO as GPIO

HOME = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(HOME)

from raspi_assistant.config.installer import install_logger
from raspi_assistant.config import Path, GPIO_Config
from raspi_assistant.src.handler.assistant_handler import AssistantHandler


install_logger(os.path.join(Path.LOG_DIR, 'raspi_assistant.log'))
logger = logging.getLogger()


def set_GPIO():
    GPIO.setmode(GPIO.BCM)
    set_voice_sensor()


def set_voice_sensor():
    GPIO.setup(GPIO_Config.VOICE_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_Config.VOICE_SENSOR, GPIO.FALLING)


def loop():
    assistant_handler = AssistantHandler()
    try:
        while True:
            # 下降沿检测
            if GPIO.event_detected(GPIO_Config.VOICE_SENSOR):
                GPIO.remove_event_detect(GPIO_Config.VOICE_SENSOR)
                assistant_handler.wakeup()
                GPIO.add_event_detect(GPIO_Config.VOICE_SENSOR, GPIO.FALLING)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    set_GPIO()
    loop()
