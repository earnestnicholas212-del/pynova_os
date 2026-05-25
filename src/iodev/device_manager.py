#!/usr/bin/env python3
"""
I/O Device Manager
Simulates blocking and non-blocking I/O operations using the DES engine.
"""

from kernel.engine import Environment, Timeout


class IODevice:
    def __init__(self, env, name, latency=2):
        self.env = env
        self.name = name
        self.latency = latency
        self.busy = False
        self.queue = []

    def request(self, proc, duration=1):
        """Simulate an I/O request. Returns a generator for DES."""
        self.queue.append((proc, duration))
        self.busy = True
        while self.queue and self.queue[0][0] != proc:
            yield self.env.timeout(1)
        # Now it's our turn
        yield self.env.timeout(self.latency)
        yield self.env.timeout(duration)
        self.queue.pop(0)
        if not self.queue:
            self.busy = False

    def flush(self):
        self.queue.clear()
        self.busy = False


class IOManager:
    def __init__(self, env):
        self.env = env
        self.devices = {}

    def register(self, name, latency=2):
        self.devices[name] = IODevice(self.env, name, latency)

    def get(self, name):
        return self.devices.get(name)

    def request(self, device_name, proc, duration=1):
        dev = self.devices.get(device_name)
        if dev is None:
            raise KeyError(f"No such device: {device_name}")
        return dev.request(proc, duration)
