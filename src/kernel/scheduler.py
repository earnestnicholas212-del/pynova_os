#!/usr/bin/env python3
"""
CPU Scheduler
Implements FCFS, SJF, SRTF, Priority, Priority (Preemptive), and Round Robin.
"""

from kernel.engine import Environment
from kernel.pcb import OSProcess


class CPU:
    def __init__(self, env, algorithm='Round Robin', quantum=2):
        self.env = env
        self.algorithm = algorithm
        self.quantum = quantum
        self.queue = []
        self.running_process = None
        self.busy = False
        self.time_slice = 0

    def add_process(self, proc):
        proc.status = 'ready'
        self.queue.append(proc)
        self._sort_queue()

    def set_algorithm(self, algo, quantum=2):
        self.algorithm = algo
        self.quantum = quantum
        self.time_slice = 0
        self._sort_queue()

    def _sort_queue(self):
        if self.algorithm == 'SJF':
            self.queue.sort(key=lambda p: p.burst_time)
        elif self.algorithm == 'SRTF':
            self.queue.sort(key=lambda p: p.remaining_time)
        elif self.algorithm in ('Priority', 'Priority (Preemptive)'):
            self.queue.sort(key=lambda p: p.priority, reverse=True)

    def _select_next_process(self):
        if self.running_process and self.running_process.status == 'running':
            if self.algorithm == 'Round Robin':
                if self.time_slice < self.quantum:
                    return self.running_process
                self.running_process.status = 'ready'
                self.queue.append(self.running_process)
                self.running_process = None
                self.time_slice = 0
            elif self.algorithm == 'SRTF' and self.queue:
                self._sort_queue()
                candidate = self.queue[0]
                if candidate.remaining_time < self.running_process.remaining_time:
                    self.running_process.status = 'ready'
                    self.queue.append(self.running_process)
                    self.running_process = None
                    self.time_slice = 0
                    self._sort_queue()
                    return self.queue.pop(0)
                return self.running_process
            elif self.algorithm == 'Priority (Preemptive)' and self.queue:
                self._sort_queue()
                candidate = self.queue[0]
                if candidate.priority > self.running_process.priority:
                    self.running_process.status = 'ready'
                    self.queue.append(self.running_process)
                    self.running_process = None
                    self.time_slice = 0
                    self._sort_queue()
                    return self.queue.pop(0)
                return self.running_process
            else:
                return self.running_process

        if not self.queue:
            return None

        if self.algorithm == 'FCFS':
            return self.queue.pop(0)
        if self.algorithm == 'SJF':
            self._sort_queue()
            return self.queue.pop(0)
        if self.algorithm == 'SRTF':
            self._sort_queue()
            return self.queue.pop(0)
        if self.algorithm in ('Priority', 'Priority (Preemptive)'):
            self._sort_queue()
            return self.queue.pop(0)
        if self.algorithm == 'Round Robin':
            return self.queue.pop(0)
        return self.queue.pop(0)

    def run(self):
        while True:
            if not self.queue and not self.running_process:
                self.busy = False
                yield self.env.timeout(1)
                continue

            proc = self._select_next_process()
            if proc is None:
                self.busy = False
                yield self.env.timeout(1)
                continue

            self.busy = True
            if proc is not self.running_process:
                self.running_process = proc
                proc.status = 'running'
                if proc.start_time is None:
                    proc.start_time = self.env.now
                self.time_slice = 0

            yield self.env.timeout(1)
            proc.remaining_time -= 1
            self.time_slice += 1

            if proc.remaining_time <= 0:
                proc.status = 'completed'
                proc.end_time = self.env.now
                if self.running_process is proc:
                    self.running_process = None
                self.time_slice = 0
                continue

            if self.algorithm == 'Round Robin' and self.time_slice >= self.quantum:
                proc.status = 'ready'
                self.queue.append(proc)
                self.running_process = None
                self.time_slice = 0
                continue
