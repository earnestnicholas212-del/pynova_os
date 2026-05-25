# PyNova OS - Design Document

## 1. Overview
PyNova OS is a pure-Python educational operating system simulator built around a discrete-event simulation (DES) engine. It visualizes CPU scheduling algorithms, memory allocation, filesystem operations, and I/O device management in real time via a Tkinter GUI or headless CLI.

## 2. Architecture

### 2.1 Discrete Event Simulation Engine (`src/kernel/engine.py`)
- **Event**: Base class for all simulation events.
- **Timeout**: Scheduled future event (represents time delay).
- **Process**: Generator-driven simulation process.
- **Environment**: Event queue manager that advances simulation time.

### 2.2 Kernel (`src/kernel/`)
- **PCB** (`pcb.py`): Process Control Block holding process metadata (PID, burst time, priority, memory, color).
- **Scheduler** (`scheduler.py`): CPU class implementing FCFS, SJF, SRTF, Priority, Priority (Preemptive), and Round Robin.
- **Process Manager** (`process_manager.py`): `OSSystem` class that ties the DES engine, CPU, memory, and process table together.

### 2.3 Memory (`src/memory/`)
- **Memory Manager** (`memory_manager.py`): Simple contiguous allocation tracker with O(1) allocate/deallocate.

### 2.4 Filesystem (`src/filesystem/`)
- **VFS** (`vfs.py`): In-memory hierarchical filesystem supporting directories, files, create, read, write, delete, ls, cd, stat, and disk quota enforcement.

### 2.5 I/O Devices (`src/iodev/`)
- **Device Manager** (`device_manager.py`): Simulated blocking I/O with device queues, latency modeling, and flush operations.

### 2.6 GUI (`src/gui/`)
- **App** (`app.py`): Tkinter + Matplotlib dashboard showing CPU pipeline, memory matrix, live charts, process table, and kernel logs.

### 2.7 CLI (`cli.py`)
- **Simulation Mode**: Headless batch execution with configurable algorithms and workloads.
- **VFS Shell**: Interactive command-line filesystem explorer.

## 3. Scheduling Algorithms
| Algorithm | Preemptive | Selection Criteria |
|-----------|-----------|-------------------|
| FCFS | No | Arrival order |
| SJF | No | Shortest burst time |
| SRTF | Yes | Shortest remaining time |
| Priority | No | Highest priority value |
| Priority (Preemptive) | Yes | Highest priority value |
| Round Robin | Yes | Fixed time quantum |

## 4. Memory Model
Contiguous allocation with a simple used/free counter. No paging or segmentation (extensible in future versions).

## 5. Virtual File System
- Hierarchical tree structure with `VFSNode` objects
- Path resolution supports absolute and relative paths
- Disk size enforcement with `OSError` on overflow
- Metadata tracking: size, created time, modified time, permissions

## 6. I/O Device Model
- Each device has a configurable latency and request queue
- Requests are blocking: processes wait in queue until device is free
- `IOManager` registers and multiplexes multiple device types

## 7. Extensibility
- Add new scheduling algorithms by subclassing `CPU` or extending `_select_next_process`.
- Replace `MemoryManager` with paging/segmentation implementations.
- Add new device types (network, display) under `src/iodev/`.
- Extend VFS with symlinks, ACLs, or journaling.
