# coding: utf-8
import os

# baidu API config
baidu_token_url = 'https://openapi.baidu.com/oauth/2.0/token'
text2audio_url = 'http://tsn.baidu.com/text2audio'
audio2text_url = 'http://vop.baidu.com/server_api?lan=zh&ptc=1&cuid=%s&token=%s'
cuid = '08-62-66-4C-8F-E1'
base_url = 'http://baike.baidu.com'
weather_url = 'http://apis.baidu.com/heweather/weather/free'
apikey = '780aea9d64c182fc847ef8e317aa89bc'

# turing robot config
turing_url = 'http://www.tuling123.com/openapi/api'
turing_key = '4d639fbc3c156ce966e91191fe60c531'

# wolfram API config
wolfram_app_id = 'QW9W43-2JJ9KK54KV'

# audio file name config
receive_audio_file = 'receive_audio.mp3'
send_audio_file = 'send_audio.wav'
err_audio_file = 'err_audio.mp3'

# redis config
host_addr = 'localhost'
port = 6379
db = 0
socket_timeout = 1

# emotion config
happiness_threshold = 0.6

# GPIO config
class GPIO_Config(object):
    VOICE_SENSOR = 4


class Path(object):
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(PROJECT_DIR, 'log')
    VOICE_DIR = os.path.join(PROJECT_DIR, 'voice')


class RetCode(object):
    SUCCESS = "0000"
    NETWORK_ERR = "0001"
    DB_ERR = "0002"
    SERVER_ERR = "0003"
    DATA_NOT_EXIST = "0004"


class Action(object):
    Record = 'record'
    PlayRecord = 'play_record'
    WeatherTomorrow = 'weather_tomo'
    WeatherToday = 'weather_today'
