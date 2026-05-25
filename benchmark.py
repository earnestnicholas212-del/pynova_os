#!/usr/bin/env python3
"""
PyNova OS Benchmark Suite
Compare scheduling algorithms under identical workloads.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from kernel.process_manager import OSSystem


def benchmark(algorithms, workload, ticks=200):
    print(f"{'Algorithm':<22} {'Completed':>10} {'Avg Wait':>10} {'Avg Turn':>10} {'Throughput':>12} {'CPU%':>6}")
    print("-" * 72)
    for algo in algorithms:
        osys = OSSystem()
        for burst, priority, mem in workload:
            osys.add_process(f"P-{burst}-{priority}", burst, priority, mem)
        quantum = 2 if algo == "Round Robin" else 0
        osys.set_algorithm(algo, quantum)
        for _ in range(ticks):
            osys.tick()
        s = osys.get_stats()
        print(f"{algo:<22} {s['completed']:>10} {s['avg_wait']:>10.2f} {s['avg_turnaround']:>10.2f} "
              f"{s['throughput']:>12.4f} {s['cpu_util']:>6.1f}")


if __name__ == "__main__":
    # Mixed workload: short interactive jobs + long batch jobs
    workload = [
        (3, 5, 64),   # short, high priority
        (5, 3, 128),  # medium
        (2, 8, 32),   # very short, highest priority
        (10, 1, 256), # long batch
        (4, 4, 64),   # short
        (7, 2, 128),  # medium-long
    ]
    algorithms = ["FCFS", "SJF", "SRTF", "Priority", "Priority (Preemptive)", "Round Robin"]
    benchmark(algorithms, workload, ticks=200)
