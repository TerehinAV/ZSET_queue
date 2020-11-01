# -*- coding: utf-8 -*-
"""
Simple queue using redis ZSET
"""
from datetime import datetime, timedelta
from helpers import RedisConnection


QUEUE_KEY = "queue"
QUEUE_KEY_LIMIT_DAYS = 7


class SimpleZSETQueue:
    def __init__(self):
        self.db = RedisConnection.create()

    def _get_score(self):
        """Returns score for ZSET record"""
        return self.get_score_by_dt(datetime.now())

    @staticmethod
    def get_score_by_dt(dt):
        """Returns score for ZSET record by custom datetime"""
        return -1 * int(dt.timestamp())

    @staticmethod
    def _get_thresh():
        """Returns threshold for """
        return -1 * int((datetime.now() - timedelta(days=QUEUE_KEY_LIMIT_DAYS + 1)).timestamp())

    def add_to_queue(self, task, score=None):
        """Add task to queue"""
        self.db.zadd(QUEUE_KEY, {task: score or self._get_score()})

    def get_first(self):
        """Returns first element added to queue"""
        return self.db.zpopmin(QUEUE_KEY)

    def get_all(self):
        """Returns all tasks"""
        return self.db.zrange(QUEUE_KEY, 0, -1)

    def get_last(self):
        """Return last added element from queue"""
        return self.db.zpopmax(QUEUE_KEY)

    def remove_tail(self):
        """Removes all records older than 7 days"""
        threshold = self._get_thresh()
        self.db.zremrangebyscore(QUEUE_KEY, threshold, 0)

    def destroy(self):
        """Clear queue"""
        self.db.delete(QUEUE_KEY)
