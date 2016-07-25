# coding: utf-8
import random

from raspi_assistant.src.globals.word_recognition import (
    movement, positive_answer, negative_answer, make_record, query, play_record
    )
from raspi_assistant.src.bll.thinking_handler import thinking_turing
from raspi_assistant.config import happiness_threshold, Action


def get_answer(content):
    print content
    if any((x in content for x in movement)):
        # TODO: 判断运动类型
        print 'I got move'
        return generate_response(), u'move'
    elif u'天气' in content:
        if u'明天' in content:
            print 'I got weather and tomorrow'
            return generate_response(), Action.WeatherTomorrow
        else:
            print 'I got weather'
            return generate_response(), Action.WeatherToday
    elif any((x in content for x in make_record)):
        print 'I got record'
        return generate_response(), Action.Record
    elif any((x in content for x in play_record)):
        print 'play record'
        return generate_response(), Action.PlayRecord
    else:
        print 'I have to search'
        return thinking_turing(content), None


def generate_response():
    if random.random() <= happiness_threshold:
        return positive_answer[random.randint(1, len(positive_answer))]
    else:
        return negative_answer[random.randint(1, len(negative_answer))]
