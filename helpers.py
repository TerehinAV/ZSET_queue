# -*- coding: utf-8 -*-
"""
Helpers functions module
"""

import redis

DEFAULT_REDIS_HOST = "localhost"
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_DB = 0


class RedisConnection:
    """Redis connection class"""
    connection = None

    @classmethod
    def _ping(cls):
        """Checking connection is still alive"""
        if cls.connection:
            return cls.connection.ping()
        else:
            return None

    @classmethod
    def create(cls, host=DEFAULT_REDIS_HOST, port=DEFAULT_REDIS_PORT, db=DEFAULT_REDIS_DB):
        """Creates/updates redis connection"""
        if not cls.connection:
            cls.connection = redis.Redis(host=host, port=port, db=db)
        else:
            pong = cls._ping()
            if not pong:
                cls.connection.close()
                cls.connection = redis.Redis(host=host, port=port, db=db)
        return cls.connection

    @classmethod
    def close(cls):
        """Close connection"""
        cls.connection.close()
