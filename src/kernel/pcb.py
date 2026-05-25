#!/usr/bin/env python3
"""
Process Control Block (PCB)
Represents a single process in the OS simulation.
"""

import random


class OSProcess:
    def __init__(self, pid, name, burst_time, priority, memory_size):
        self.pid = pid
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.memory_size = memory_size
        self.status = 'new'
        self.start_time = None
        self.end_time = None
        self.arrival_time = 0
        self.color = f"#{random.randint(50, 200):02x}{random.randint(50, 200):02x}{random.randint(50, 200):02x}"
