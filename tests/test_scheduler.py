#!/usr/bin/env python3
"""Unit tests for the CPU Scheduler."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from kernel.engine import Environment
from kernel.pcb import OSProcess
from kernel.scheduler import CPU


class TestScheduler(unittest.TestCase):
    def test_fcfs_order(self):
        env = Environment()
        cpu = CPU(env, 'FCFS')
        p1 = OSProcess('P1', 'A', 3, 1, 64)
        p2 = OSProcess('P2', 'B', 2, 1, 64)
        cpu.add_process(p1)
        cpu.add_process(p2)
        self.assertEqual(cpu.queue, [p1, p2])

    def test_sjf_sort(self):
        env = Environment()
        cpu = CPU(env, 'SJF')
        p1 = OSProcess('P1', 'A', 5, 1, 64)
        p2 = OSProcess('P2', 'B', 1, 1, 64)
        cpu.add_process(p1)
        cpu.add_process(p2)
        cpu._sort_queue()
        self.assertEqual(cpu.queue[0], p2)

    def test_priority_sort(self):
        env = Environment()
        cpu = CPU(env, 'Priority')
        p1 = OSProcess('P1', 'A', 5, 2, 64)
        p2 = OSProcess('P2', 'B', 5, 8, 64)
        cpu.add_process(p1)
        cpu.add_process(p2)
        cpu._sort_queue()
        self.assertEqual(cpu.queue[0], p2)

    def test_round_robin_preemption(self):
        env = Environment()
        cpu = CPU(env, 'Round Robin', quantum=2)
        p1 = OSProcess('P1', 'A', 5, 1, 64)
        cpu.add_process(p1)
        cpu.running_process = p1
        p1.status = 'running'
        cpu.time_slice = 2
        nxt = cpu._select_next_process()
        # After quantum expiry, running process goes back to queue and is re-selected
        self.assertEqual(nxt, p1)
        self.assertEqual(cpu.time_slice, 0)
        # Status is 'ready' until run() promotes it back to 'running'
        self.assertEqual(p1.status, 'ready')

    def test_srtf_preemption(self):
        env = Environment()
        cpu = CPU(env, 'SRTF')
        p_long = OSProcess('P1', 'Long', 10, 1, 64)
        p_short = OSProcess('P2', 'Short', 2, 1, 64)
        cpu.add_process(p_long)
        cpu.running_process = p_long
        p_long.status = 'running'
        cpu.add_process(p_short)
        nxt = cpu._select_next_process()
        self.assertEqual(nxt, p_short)


if __name__ == '__main__':
    unittest.main()
