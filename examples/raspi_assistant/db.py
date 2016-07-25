# coding: utf-8
import logging
import traceback

import redis

from raspi_assistant.src.globals import conn_pool
from raspi_assistant.config import socket_timeout


class RedisDal(object):
    def __init__(self, **kwargs):
        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = logging.getLogger()

    def set(self, name, ttl, value):
        try:
            client = redis.StrictRedis(connection_pool=conn_pool, socket_timeout=socket_timeout)
            if ttl:
                ret = client.setex(name, ttl, value)
            else:
                ret = client.set(name, value)
        except Exception, e:
            self.logger.warn(traceback.format_exc())
            return False
        return ret

    def get(self, name):
        try:
            client = redis.StrictRedis(connection_pool=conn_pool, socket_timeout=socket_timeout)
            ret = client.get(name)
        except Exception, e:
            self.logger.warn(traceback.format_exc())
            return False
        return ret
