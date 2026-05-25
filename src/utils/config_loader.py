#!/usr/bin/env python3
"""
Configuration Loader
Load simulation batches from JSON files.
"""

import json
import os


class ConfigLoader:
    @staticmethod
    def load(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def validate(cfg):
        required = ['algorithm', 'ticks', 'processes']
        for key in required:
            if key not in cfg:
                raise ValueError(f"Missing required key: {key}")
        if cfg['algorithm'] not in ["Round Robin", "FCFS", "SJF", "SRTF", "Priority", "Priority (Preemptive)"]:
            raise ValueError(f"Invalid algorithm: {cfg['algorithm']}")
        for i, p in enumerate(cfg['processes']):
            for key in ['name', 'burst', 'priority', 'memory']:
                if key not in p:
                    raise ValueError(f"Process {i} missing key: {key}")
        return True

    @staticmethod
    def from_dict(cfg):
        ConfigLoader.validate(cfg)
        return cfg
