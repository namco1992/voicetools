# encoding: utf-8
import os
import sys
import logging

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print HOME
sys.path.append(HOME)

from raspi_assistant import BaiduVoice, TuringRobot, Wolfram
bv = BaiduVoice('24.c732785d895d118884937d4d2321d51e.2592000.1471771233.282335-8403190')
# test asr
# bv.asr(file_='err_audio.wav', lan='en', ptc=2)

# test tts
# with open('test_tts.wav', 'wb') as f:
#     f.write(bv.tts('你好'))

# test turing robot
# robot = TuringRobot('4d639fbc3c156ce966e91191fe60c531')
# print robot.ask_turing('成都天气')

# test wolfram
wolfram = Wolfram('QW9W43-2JJ9KK54KV')
print wolfram.ask_wolfram('who is the president of United States')

# import RPi.GPIO
# import time

# # 声音感应器OUT口连接的GPIO口
# SENSOR = 4

# RPi.GPIO.setmode(RPi.GPIO.BCM)

# # 指定GPIO4（声音感应器的OUT口连接的GPIO口）的模式为输入模式
# # 默认拉高到高电平，低电平表示OUT口有输出
# RPi.GPIO.setup(SENSOR, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
# RPi.GPIO.add_event_detect(SENSOR, RPi.GPIO.FALLING)
# try:
#     while True:
#         # 检测声音感应器是否输出低电平，若是低电平，表示声音被检测到，点亮或关闭LED灯
#         if (RPi.GPIO.input(SENSOR) == RPi.GPIO.LOW):
#             print 'Tested.'
#         if RPi.GPIO.event_detected(SENSOR):
#             print 'tested'
#         time.sleep(0.5)
# except KeyboardInterrupt:
#     pass

# RPi.GPIO.cleanup()


