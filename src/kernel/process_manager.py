#!/usr/bin/env python3
"""
OS System / Process Manager
Orchestrates the kernel, scheduler, memory, and process lifecycle.
"""

from kernel.engine import Environment
from kernel.scheduler import CPU
from kernel.pcb import OSProcess
from memory.memory_manager import MemoryManager


class OSSystem:
    def __init__(self):
        self.env = Environment()
        self.cpu = CPU(self.env)
        self.memory = MemoryManager()
        self.processes = []
        self.stats_history = []
        self.logs = []
        self.cpu_process = self.env.process(self.cpu.run())

    def add_process(self, name, burst, priority, mem_size):
        pid = f"P{len(self.processes)+1}"
        proc = OSProcess(pid, name, burst, priority, mem_size)
        proc.arrival_time = self.env.now
        if not self.memory.allocate(proc):
            self.logs.append((self.env.now, f"OOM: Cannot allocate {mem_size}MB for {name}", 'error'))
            return False
        self.processes.append(proc)
        self.cpu.add_process(proc)
        self.logs.append((self.env.now, f"Process {name} injected", 'success'))
        return True

    def set_algorithm(self, algo, quantum):
        self.cpu.set_algorithm(algo, quantum)

    def tick(self):
        self.env.step()
        cpu_util = 100 if self.cpu.busy else 0
        mem_util = (self.memory.used / self.memory.total) * 100
        self.stats_history.append({'time': self.env.now, 'cpu': cpu_util, 'mem': mem_util})
        if len(self.stats_history) > 100:
            self.stats_history.pop(0)
        # Clean up memory for completed processes
        for p in self.processes:
            if p.status == 'completed' and p.pid in self.memory.allocations:
                self.memory.deallocate(p)
                self.logs.append((self.env.now, f"Process {p.name} completed", 'success'))

    def get_stats(self):
        completed = [p for p in self.processes if p.status == 'completed']
        total_wait = sum((p.end_time - p.arrival_time - p.burst_time) for p in completed if p.end_time is not None)
        total_turnaround = sum((p.end_time - p.arrival_time) for p in completed if p.end_time is not None)
        return {
            'completed': len(completed),
            'total': len(self.processes),
            'avg_wait': total_wait / len(completed) if completed else 0,
            'avg_turnaround': total_turnaround / len(completed) if completed else 0,
            'throughput': len(completed) / max(1, self.env.now),
            'cpu_util': 100 if self.cpu.busy else 0,
            'mem_util': (self.memory.used / self.memory.total) * 100,
            'running': self.cpu.running_process.name if self.cpu.running_process else "Idle",
        }
