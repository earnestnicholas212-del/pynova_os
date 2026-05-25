#!/usr/bin/env python3
"""
PyNova OS - Command Line Interface
Headless simulation mode for batch processing and automated testing.
"""

import sys
import os
import argparse
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from kernel.process_manager import OSSystem
from filesystem.vfs import VirtualFileSystem
from utils.config_loader import ConfigLoader
from utils.exporter import SimulationExporter


def run_simulation(args):
    osys = OSSystem()
    vfs = VirtualFileSystem(disk_size=args.disk_size)

    # Load from JSON config if provided
    if args.config:
        cfg = ConfigLoader.load(args.config)
        ConfigLoader.validate(cfg)
        args.algo = cfg.get('algorithm', args.algo)
        args.quantum = cfg.get('quantum', args.quantum)
        args.ticks = cfg.get('ticks', args.ticks)
        args.report_interval = cfg.get('report_interval', args.report_interval)
        args.delay = cfg.get('delay_ms', args.delay)
        args.disk_size = cfg.get('disk_size', args.disk_size)
        if 'memory_total' in cfg:
            osys.memory.total = cfg['memory_total']
        for p in cfg.get('processes', []):
            ok = osys.add_process(p['name'], p['burst'], p['priority'], p['memory'])
            if not ok:
                print(f"[WARN] Failed to allocate {p['memory']}MB for {p['name']}")
    elif args.processes:
        for spec in args.processes:
            try:
                burst, priority, mem = map(int, spec.split(","))
                name = f"Batch-{len(osys.processes)+1}"
                ok = osys.add_process(name, burst, priority, mem)
                if not ok:
                    print(f"[WARN] Failed to allocate {mem}MB for {name}")
            except Exception as e:
                print(f"[WARN] Invalid process spec '{spec}': {e}")

    osys.set_algorithm(args.algo, args.quantum)
    print(f"[BOOT] Algorithm={args.algo} Quantum={args.quantum}")
    print(f"[BOOT] Running for {args.ticks} ticks...")

    for tick in range(args.ticks):
        osys.tick()
        if tick % args.report_interval == 0:
            stats = osys.get_stats()
            print(f"[T+{osys.env.now:04d}] CPU={stats['cpu_util']:3d}% MEM={stats['mem_util']:5.1f}% "
                  f"RUN={stats['running']:12s} COMPLETED={stats['completed']}/{stats['total']}")
        if args.delay > 0:
            time.sleep(args.delay / 1000.0)

    stats = osys.get_stats()
    print("\n[HALT] Final Statistics")
    print(f"  Total Processes : {stats['total']}")
    print(f"  Completed       : {stats['completed']}")
    print(f"  Avg Wait Time   : {stats['avg_wait']:.2f}s")
    print(f"  Avg Turnaround  : {stats['avg_turnaround']:.2f}s")
    print(f"  Throughput      : {stats['throughput']:.4f} p/s")
    print(f"  CPU Utilization : {stats['cpu_util']}%")
    print(f"  Memory Util     : {stats['mem_util']:.1f}%")

    if args.export_csv:
        SimulationExporter.to_csv(osys.stats_history, args.export_csv)
        print(f"[EXPORT] CSV saved to {args.export_csv}")
    if args.export_json:
        SimulationExporter.to_json(osys.stats_history, stats, args.export_json)
        print(f"[EXPORT] JSON saved to {args.export_json}")


def vfs_shell(args):
    vfs = VirtualFileSystem(disk_size=args.disk_size)
    print("PyNova VFS Shell. Type 'help' for commands.")
    while True:
        try:
            cmd = input(f"{vfs.pwd()} $ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[EXIT]")
            break
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0]
        try:
            if op == "exit":
                break
            elif op == "help":
                print("mkdir <dir>  create <file> [text]  read <file>  write <file> <text>")
                print("ls [dir]     cd <dir>     pwd        stat <path>  rm <path>")
            elif op == "mkdir":
                vfs.mkdir(parts[1])
                print("OK")
            elif op == "create":
                content = " ".join(parts[2:]).encode() if len(parts) > 2 else b""
                vfs.create(parts[1], content)
                print("OK")
            elif op == "read":
                data = vfs.read(parts[1])
                print(data.decode(errors="replace"))
            elif op == "write":
                content = " ".join(parts[2:]).encode()
                vfs.write(parts[1], content)
                print("OK")
            elif op == "ls":
                entries = vfs.ls(parts[1] if len(parts) > 1 else ".")
                for name, is_dir, size, mod in entries:
                    t = "D" if is_dir else "F"
                    print(f"{t} {size:6d} {name}")
            elif op == "cd":
                path = vfs.cd(parts[1])
                print(path)
            elif op == "pwd":
                print(vfs.pwd())
            elif op == "stat":
                info = vfs.stat(parts[1])
                for k, v in info.items():
                    print(f"  {k}: {v}")
            elif op == "rm":
                vfs.delete(parts[1])
                print("OK")
            else:
                print(f"Unknown command: {op}")
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="PyNova OS Simulator CLI")
    sub = parser.add_subparsers(dest="mode", required=True)

    sim = sub.add_parser("sim", help="Run headless simulation")
    sim.add_argument("--algo", default="Round Robin", choices=["Round Robin","FCFS","SJF","SRTF","Priority","Priority (Preemptive)"])
    sim.add_argument("--quantum", type=int, default=2)
    sim.add_argument("--ticks", type=int, default=100)
    sim.add_argument("--processes", nargs="*", help="Process specs: burst,priority,mem (e.g. 5,1,128)")
    sim.add_argument("--config", help="Path to JSON config file")
    sim.add_argument("--disk-size", type=int, default=4096)
    sim.add_argument("--report-interval", type=int, default=10)
    sim.add_argument("--delay", type=int, default=0, help="Tick delay in ms")
    sim.add_argument("--export-csv", help="Export tick history to CSV file")
    sim.add_argument("--export-json", help="Export summary and history to JSON file")

    shell = sub.add_parser("vfs", help="Interactive VFS shell")
    shell.add_argument("--disk-size", type=int, default=4096)

    args = parser.parse_args()
    if args.mode == "sim":
        run_simulation(args)
    elif args.mode == "vfs":
        vfs_shell(args)


if __name__ == "__main__":
    main()
