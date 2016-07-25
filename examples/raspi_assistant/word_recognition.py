# coding: utf-8

movement = (u'前进', u'转弯', u'转', u'停下')
make_record = (u'记下来', u'提醒我')
play_record = (u'备忘录', u'哪些该做的')
query = ('tell me about', 'introduce', 'search')
positive_answer = {
    # 1: 'what can I do for you.',
    # 2: 'no problem.',
    # 4: 'with pleasure.',
    # 5: 'anything you say.',
    # 6: 'as your wish.',
    # 7: 'I can not wait to do this.',
    1: u'等候多时',
    2: u'你回来了',
    3: u'我听到你说的了',
    4: u'今天工作辛苦吗',
    5: u'你今天又变帅了',
    6: u'需要我帮你做点什么？'
}

# The negative_answer won't negative your command, just the emotion expression
negative_answer = {
    1: '别吵了，真烦人',
    2: '好了好了，我听见了',
    3: '我今天心情不太好',
    4: '别找我，我想静静，也别问我静静是谁',
    5: '每天都来烦我，你什么时候给我找个男朋友'
}

today_weather_text = \
u'当前天气{cond}，体感温度{fl}摄氏度，空气湿度百分之{hum}。今日温度为{min}到{max}摄氏度，{txt_d}转{txt_n}，降水概率百分之{pop}，空气质量{qlty}。'

tomorrow_weather_text = \
    u'明天的气温是{min}到{max}摄氏度，{txt_d}转{txt_n}，降水概率百分之{pop}。'
