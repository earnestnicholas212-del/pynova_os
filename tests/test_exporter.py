#!/usr/bin/env python3
"""Unit tests for SimulationExporter."""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from utils.exporter import SimulationExporter


class TestExporter(unittest.TestCase):
    def test_csv_export(self):
        history = [
            {"time": 0, "cpu": 100, "mem": 50.0},
            {"time": 1, "cpu": 0, "mem": 25.0},
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            path = f.name
        SimulationExporter.to_csv(history, path)
        with open(path) as f:
            lines = f.readlines()
        self.assertEqual(lines[0].strip(), "time,cpu,mem")
        self.assertEqual(lines[1].strip(), "0,100,50.0")
        os.remove(path)

    def test_json_export(self):
        history = [{"time": 0, "cpu": 100}]
        summary = {"total": 1, "completed": 1}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            path = f.name
        SimulationExporter.to_json(history, summary, path)
        import json
        with open(path) as f:
            data = json.load(f)
        self.assertEqual(data['summary']['total'], 1)
        self.assertEqual(data['history'][0]['cpu'], 100)
        os.remove(path)


if __name__ == '__main__':
    unittest.main()
