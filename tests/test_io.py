#!/usr/bin/env python3
"""Unit tests for the I/O Device Manager."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from kernel.engine import Environment
from kernel.pcb import OSProcess
from iodev.device_manager import IOManager, IODevice


class TestIO(unittest.TestCase):
    def test_device_registration(self):
        env = Environment()
        mgr = IOManager(env)
        mgr.register("disk", latency=3)
        self.assertIn("disk", mgr.devices)
        self.assertEqual(mgr.devices["disk"].latency, 3)

    def test_device_queue(self):
        env = Environment()
        dev = IODevice(env, "printer", latency=2)
        p1 = OSProcess('P1', 'A', 5, 1, 64)
        p2 = OSProcess('P2', 'B', 5, 1, 64)
        gen1 = dev.request(p1, duration=1)
        gen2 = dev.request(p2, duration=1)
        next(gen1)
        next(gen2)
        self.assertEqual(len(dev.queue), 2)
        self.assertTrue(dev.busy)

    def test_io_manager_request(self):
        env = Environment()
        mgr = IOManager(env)
        mgr.register("disk", latency=1)
        p = OSProcess('P1', 'A', 5, 1, 64)

        def io_task():
            yield from mgr.request("disk", p, duration=1)
            return "done"

        proc = env.process(io_task())
        env.step()  # process starts, yields latency timeout
        env.step()  # latency timeout fires, yields duration timeout
        env.step()  # duration timeout fires, process completes
        self.assertFalse(proc.is_alive)

    def test_flush(self):
        env = Environment()
        dev = IODevice(env, "tty", latency=1)
        p = OSProcess('P1', 'A', 5, 1, 64)
        gen = dev.request(p, duration=1)
        next(gen)
        dev.flush()
        self.assertEqual(len(dev.queue), 0)
        self.assertFalse(dev.busy)


if __name__ == '__main__':
    unittest.main()
