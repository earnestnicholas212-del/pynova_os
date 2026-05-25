# PyNova OS Simulator

A pure Python educational operating system simulator using a custom discrete-event simulation (DES) engine, Tkinter GUI, and Matplotlib real-time analytics.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **6 CPU Scheduling Algorithms**: FCFS, SJF, SRTF, Priority, Priority (Preemptive), Round Robin
- **Live Dashboard**: CPU pipeline visualization, memory matrix, utilization charts, process table, kernel logs
- **Virtual File System**: In-memory hierarchical filesystem with mkdir, create, read, write, delete, ls, cd, stat
- **I/O Device Manager**: Simulated blocking I/O with device queues and latency
- **Discrete Event Simulation**: Custom SimPy-like engine under the hood
- **Modular Architecture**: Clean separation of kernel, memory, filesystem, I/O, and GUI layers
- **CLI Mode**: Headless batch simulation and interactive VFS shell
- **Benchmark Suite**: Compare all schedulers under identical workloads

## Project Structure

```
PyNovaOS/
├── docs/
│   ├── UML_Diagrams/
│   ├── Flowcharts/
│   └── Design_Document.md
├── src/
│   ├── kernel/
│   │   ├── engine.py           # DES engine (Event, Process, Environment)
│   │   ├── pcb.py              # Process Control Block
│   │   ├── scheduler.py        # CPU & scheduling algorithms
│   │   └── process_manager.py  # OSSystem orchestrator
│   ├── memory/
│   │   └── memory_manager.py   # Contiguous memory allocator
│   ├── filesystem/
│   │   └── vfs.py              # Virtual file system
│   ├── iodev/
│   │   └── device_manager.py   # I/O device simulation
│   └── gui/
│       └── app.py              # Tkinter + Matplotlib dashboard
├── tests/
│   ├── test_engine.py
│   ├── test_scheduler.py
│   ├── test_memory.py
│   ├── test_vfs.py
│   └── test_io.py
├── main.py                     # GUI entry point
├── cli.py                      # Command-line interface
├── benchmark.py                # Scheduler benchmark suite
├── requirements.txt
├── pyproject.toml
├── Makefile
└── README.md
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the GUI Simulator
```bash
python main.py
```

### 3. Run Headless Simulation
```bash
python cli.py sim --algo SJF --ticks 100 --processes 5,1,128 8,2,64
```

### 4. Interactive VFS Shell
```bash
python cli.py vfs
```

### 5. Run Benchmarks
```bash
python benchmark.py
```

### 6. Run Tests
```bash
make test
# or
PYTHONPATH=src python -m unittest discover -s tests -v
```

## CLI Usage

### Simulation Mode
```bash
python cli.py sim --algo Round_Robin --ticks 200 --quantum 3 \
  --processes 5,1,128 8,2,64 3,3,256 --report-interval 10
```

Options:
- `--algo`: Scheduling algorithm
- `--quantum`: Time quantum for Round Robin
- `--ticks`: Simulation duration
- `--processes`: List of `burst,priority,mem` specs
- `--disk-size`: VFS disk size in bytes
- `--report-interval`: Tick interval for status prints
- `--delay`: Millisecond delay between ticks (for demo)

### VFS Shell Commands
```
mkdir <dir>       create <file> [text]    read <file>
write <file> <text>    ls [dir]    cd <dir>    pwd
stat <path>    rm <path>    help    exit
```

## Scheduling Algorithms

| Algorithm | Preemptive | Selection Criteria |
|-----------|-----------|-------------------|
| FCFS | No | Arrival order |
| SJF | No | Shortest burst time |
| SRTF | Yes | Shortest remaining time |
| Priority | No | Highest priority value |
| Priority (Preemptive) | Yes | Highest priority value |
| Round Robin | Yes | Fixed time quantum |

## Extending PyNovaOS

- **New Scheduler**: Extend `CPU._select_next_process()` in `src/kernel/scheduler.py`.
- **Paged Memory**: Replace `MemoryManager` in `src/memory/memory_manager.py` with a page-table implementation.
- **New I/O Devices**: Add device types in `src/iodev/device_manager.py`.
- **VFS Features**: Extend `VirtualFileSystem` in `src/filesystem/vfs.py` with permissions, symlinks, etc.

## License

MIT License — Educational use encouraged.
