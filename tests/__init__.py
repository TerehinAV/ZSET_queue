# -*- coding: utf-8 -*-
"""
Simple ZSET queue tests
"""
import unittest
from datetime import datetime, timedelta
from simple_queue import SimpleZSETQueue, QUEUE_KEY_LIMIT_DAYS


class TestZSETQueue(unittest.TestCase):
    def setUp(self):
        self.queue = SimpleZSETQueue()

    def tearDown(self):
        self.queue.destroy()

    def _get_tasks(self, tasks_count):
        for day in range(1, tasks_count + 1):
            dt = datetime.now() - timedelta(days=day)
            score = self.queue.get_score_by_dt(dt)
            self.queue.add_to_queue("task_{}".format(day), score)

    def test_add(self):
        task = "task"
        self.queue.add_to_queue(task)
        from_redis = self.queue.get_last()
        self.assertEqual(from_redis[0][0].decode(), task)

    def test_get_all(self):
        tasks_count = 10
        self._get_tasks(tasks_count)
        tasks = self.queue.get_all()
        self.assertEqual(len(tasks), tasks_count)
        self.queue.destroy()

    def test_remove_tail(self):
        tasks_count = 10
        self._get_tasks(tasks_count)
        self.queue.remove_tail()
        tasks_left = self.queue.get_all()
        self.assertEqual(len(tasks_left), QUEUE_KEY_LIMIT_DAYS)
        self.queue.destroy()


if __name__ == '__main__':
    unittest.main()
