#!/usr/bin/env python3
"""
Simulation Exporter
Export simulation statistics to CSV or JSON.
"""

import csv
import json
import os


class SimulationExporter:
    @staticmethod
    def to_csv(stats_history, filepath):
        if not stats_history:
            return
        keys = stats_history[0].keys()
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(stats_history)

    @staticmethod
    def to_json(stats_history, summary, filepath):
        payload = {
            "summary": summary,
            "history": stats_history
        }
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
