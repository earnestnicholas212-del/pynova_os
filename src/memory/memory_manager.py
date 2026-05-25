#!/usr/bin/env python3
"""
Memory Manager
Handles allocation and deallocation of memory for processes.
"""


class MemoryManager:
    def __init__(self, total=1024):
        self.total = total
        self.used = 0
        self.allocations = {}

    def allocate(self, proc):
        if self.used + proc.memory_size > self.total:
            return False
        self.used += proc.memory_size
        self.allocations[proc.pid] = proc.memory_size
        return True

    def deallocate(self, proc):
        if proc.pid in self.allocations:
            self.used -= self.allocations[proc.pid]
            del self.allocations[proc.pid]
