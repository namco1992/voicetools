# coding: utf-8
from .utils import Keyword
KEYWORDS = {u'提醒', u'备忘录', u'播放', u'今天', u'明天', u'天气'}


FUNC_MAP = {
    Keyword([u'备忘录', ]).value: 'a',
    Keyword([u'提醒', ]).value: 'b',
    Keyword([u'备忘录', u'播放']).value: 'c',
    Keyword([u'明天', u'天气']).value: 'd',
    Keyword([u'今天', u'天气']).value: 'e'
}


POSITIVE_ANSWER = {
    1: u'等候多时',
    2: u'你回来了',
    3: u'我听到你说的了',
    4: u'今天工作辛苦吗',
    5: u'你今天又变帅了',
    6: u'需要我帮你做点什么？'
}

# The negative_answer won't negative your command, just the emotion expression
NEGATIVE_ANSWER = {
    1: '别吵了，真烦人',
    2: '好了好了，我听见了',
    3: '我今天心情不太好',
    4: '我想静静，也别问我静静是谁',
    5: '每天都来烦我，你什么时候给我找个男朋友'
}

TODAY_WEATHER_TEXT = \
u'当前天气{cond}，体感温度{fl}摄氏度，空气湿度百分之{hum}。今日温度为{min}到{max}摄氏度，{txt_d}转{txt_n}，降水概率百分之{pop}，空气质量{qlty}。'

TOMO_WEATHER_TEXT = \
    u'明天的气温是{min}到{max}摄氏度，{txt_d}转{txt_n}，降水概率百分之{pop}。'


if __name__ == '__main__':
    print FUNC_MAP[Keyword([u'提醒']).value]
