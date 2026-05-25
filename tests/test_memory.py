#!/usr/bin/env python3
"""Unit tests for the Memory Manager."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from memory.memory_manager import MemoryManager
from kernel.pcb import OSProcess


class TestMemory(unittest.TestCase):
    def test_allocate_success(self):
        mm = MemoryManager(1024)
        p = OSProcess('P1', 'Test', 5, 1, 512)
        self.assertTrue(mm.allocate(p))
        self.assertEqual(mm.used, 512)
        self.assertIn('P1', mm.allocations)

    def test_allocate_fail(self):
        mm = MemoryManager(256)
        p = OSProcess('P1', 'Test', 5, 1, 512)
        self.assertFalse(mm.allocate(p))
        self.assertEqual(mm.used, 0)

    def test_deallocate(self):
        mm = MemoryManager(1024)
        p = OSProcess('P1', 'Test', 5, 1, 256)
        mm.allocate(p)
        mm.deallocate(p)
        self.assertEqual(mm.used, 0)
        self.assertNotIn('P1', mm.allocations)

    def test_multiple_allocations(self):
        mm = MemoryManager(1000)
        p1 = OSProcess('P1', 'A', 2, 1, 300)
        p2 = OSProcess('P2', 'B', 2, 1, 400)
        self.assertTrue(mm.allocate(p1))
        self.assertTrue(mm.allocate(p2))
        self.assertEqual(mm.used, 700)
        mm.deallocate(p1)
        self.assertEqual(mm.used, 400)


if __name__ == '__main__':
    unittest.main()
