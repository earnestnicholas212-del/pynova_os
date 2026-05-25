#!/usr/bin/env python3
"""Unit tests for the DES Engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from kernel.engine import Environment, Event, Timeout, Process


class TestEngine(unittest.TestCase):
    def test_empty_step(self):
        env = Environment()
        self.assertEqual(env.now, 0)
        result = env.step()
        self.assertFalse(result)

    def test_timeout_scheduling(self):
        env = Environment()
        timeout = env.timeout(5)
        env.step()
        self.assertEqual(env.now, 5)
        self.assertTrue(timeout._triggered)

    def test_process_generator(self):
        env = Environment()
        def my_proc():
            yield env.timeout(2)
            yield env.timeout(3)
        p = env.process(my_proc())
        env.step()  # process starts
        env.step()  # first timeout
        self.assertEqual(env.now, 2)
        env.step()  # second timeout
        self.assertEqual(env.now, 5)
        self.assertFalse(p.is_alive)

    def test_event_succeed(self):
        env = Environment()
        evt = Event(env)
        triggered = []
        evt.callbacks.append(lambda e: triggered.append(True))
        evt.succeed(42)
        self.assertTrue(triggered)
        self.assertEqual(evt._value, 42)


if __name__ == '__main__':
    unittest.main()
