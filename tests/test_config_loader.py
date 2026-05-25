#!/usr/bin/env python3
"""Unit tests for ConfigLoader."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from utils.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    def test_validate_ok(self):
        cfg = {
            "algorithm": "SJF",
            "ticks": 100,
            "processes": [
                {"name": "A", "burst": 5, "priority": 1, "memory": 64}
            ]
        }
        self.assertTrue(ConfigLoader.validate(cfg))

    def test_validate_missing_key(self):
        cfg = {"algorithm": "FCFS", "ticks": 10}
        with self.assertRaises(ValueError):
            ConfigLoader.validate(cfg)

    def test_validate_bad_algo(self):
        cfg = {
            "algorithm": "INVALID",
            "ticks": 10,
            "processes": [{"name": "A", "burst": 5, "priority": 1, "memory": 64}]
        }
        with self.assertRaises(ValueError):
            ConfigLoader.validate(cfg)

    def test_load_and_validate(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'batch_simulation.json')
        if os.path.exists(path):
            cfg = ConfigLoader.load(path)
            self.assertTrue(ConfigLoader.validate(cfg))
            self.assertEqual(cfg['algorithm'], "Round Robin")


if __name__ == '__main__':
    unittest.main()
