# coding: utf-8
import os
import sys
import logging

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(HOME)

from raspi_assistant.utils import init_logging_handler
from raspi_assistant.handler import BaseHandler, ActionHandler


def main():
    logger = init_logging_handler()
    handler = BaseHandler()
    func, result = handler.process(['今天天气怎么样', ])
    handler.execute(func, result)


if __name__ == '__main__':
    main()
