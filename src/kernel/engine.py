#!/usr/bin/env python3
"""
SimPy-like Discrete Event Simulation Engine
Drives the kernel simulation via event scheduling and process generators.
"""

class Event:
    def __init__(self, env):
        self.env = env
        self.callbacks = []
        self._value = None
        self._triggered = False

    def succeed(self, value=None):
        if self._triggered:
            return
        self._triggered = True
        self._value = value
        callbacks = self.callbacks[:]
        self.callbacks = []
        for cb in callbacks:
            cb(self)


class Timeout(Event):
    def __init__(self, env, delay):
        super().__init__(env)
        self.delay = delay
        env.schedule(self, delay)


class Process(Event):
    def __init__(self, env, generator):
        super().__init__(env)
        self.generator = generator
        self.is_alive = True
        env.schedule(self, 0)

    def _resume(self, event):
        try:
            if event._value is not None:
                self._target = self.generator.send(event._value)
            else:
                self._target = next(self.generator)
            if isinstance(self._target, Event):
                self._target.callbacks.append(self._resume)
            else:
                self.is_alive = False
                self.succeed(self._target)
        except StopIteration:
            self.is_alive = False
            self.succeed()


class Environment:
    def __init__(self):
        self.now = 0
        self._queue = []
        self._eid = 0

    def process(self, generator):
        return Process(self, generator)

    def timeout(self, delay):
        return Timeout(self, delay)

    def schedule(self, event, delay):
        self._eid += 1
        self._queue.append((self.now + delay, self._eid, event))
        self._queue.sort(key=lambda x: (x[0], x[1]))

    def step(self):
        if not self._queue:
            return False
        self.now, _, event = self._queue.pop(0)
        if isinstance(event, Process):
            event._resume(event)
        else:
            event.succeed()
        return True
