# coding: utf-8
from raspi_assistant.config import RetCode, apikey, weather_url
from raspi_assistant.src.bll.voice_handler import get_rclient
from raspi_assistant.src.globals.word_recognition import today_weather_text, tomorrow_weather_text
from raspi_assistant.config import Action


def query_weather(action, cityid='CN101270101'):
    client = get_rclient(weather_url)
    ret, resp = client.handle_normal_get(
        params={'cityid': cityid},
        headers={'apikey': apikey}
        )
    if ret != RetCode.SUCCESS:
        return ret, u'查询天气失败了'
    content = resp.json()
    content = content['HeWeather data service 3.0'][0]
    if action == Action.WeatherToday:
        now_weather = content.get('now')
        today_weather = content.get('daily_forecast')[0]
        if all((now_weather, today_weather)):
            text = today_weather_text.format(
                cond=now_weather['cond']['txt'],
                fl=now_weather['fl'],
                hum=now_weather['hum'],
                min=today_weather['tmp']['min'],
                max=today_weather['tmp']['max'],
                txt_d=today_weather['cond']['txt_d'],
                txt_n=today_weather['cond']['txt_n'],
                pop=today_weather['pop'],
                qlty=content['aqi']['city']['qlty']
                )
            return RetCode.SUCCESS, text
        else:
            return RetCode.DATA_NOT_EXIST, u'啊呀，查询天气出错了'
    if action == Action.WeatherTomorrow:
        tomo_weather = content.get('daily_forecast')[1]
        if isinstance(tomo_weather, dict):
            text = tomorrow_weather_text.format(
                min=tomo_weather['tmp']['min'],
                max=tomo_weather['tmp']['max'],
                txt_d=tomo_weather['cond']['txt_d'],
                txt_n=tomo_weather['cond']['txt_n'],
                pop=tomo_weather['pop']
                )
            return RetCode.SUCCESS, text
        else:
            return RetCode.DATA_NOT_EXIST, u'啊呀，查询天气出错了'
