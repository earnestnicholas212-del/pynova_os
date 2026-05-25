# PyNova OS — Software Engineering Aspects

---

## 1. Software Architecture

### 1.1 Architectural Pattern: Layered + Plugin Architecture

PyNova OS uses a **Layered Architecture** mirroring the structure of a real operating system, combined with a **Plugin/Strategy Pattern** for swappable algorithm policies.

```
┌──────────────────────────────────────────────────────────────┐
│                    PyNova CLI / Dashboard                      │  ← Presentation Layer
├──────────────────────────────────────────────────────────────┤
│            PyNova Shell (System Call Dispatcher)              │  ← API / Service Layer
├──────────────────────────────────────────────────────────────┤
│  Process  │  Thread   │  Scheduler │  Sync      │  Deadlock  │
│  Manager  │  Manager  │  Engine    │  Manager   │  Detector  │  ← OS Core Layer
├──────────────────────────────────────────────────────────────┤
│  Memory   │  Virtual  │  File Sys  │  I/O       │  Security  │
│  Manager  │  Memory   │  Manager   │  Manager   │  Manager   │  ← Resource Layer
├──────────────────────────────────────────────────────────────┤
│  VM Hypervisor Layer                                          │  ← Virtualisation Layer
├──────────────────────────────────────────────────────────────┤
│  PyNova Simulation Kernel (Event Loop, Clock, Resource Bus)   │  ← Simulation Core
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Key Architectural Decisions

**Decision 1 — Strategy Pattern for Algorithms**  
All scheduling, page replacement, and disk scheduling algorithms are implemented as interchangeable strategy objects conforming to a common interface. This allows runtime switching and comparison without code changes.

```python
class SchedulerPolicy(ABC):
    @abstractmethod
    def select_next(self, ready_queue: List[Process]) -> Process:
        pass

class RoundRobinPolicy(SchedulerPolicy):
    def __init__(self, quantum: int = 4):
        self.quantum = quantum

    def select_next(self, ready_queue: List[Process]) -> Process:
        return ready_queue.pop(0)
```

**Decision 2 — Observer Pattern for Events**  
The simulation uses an event bus so that components can observe and react to system events (e.g., page fault triggers memory manager and logger simultaneously) without tight coupling.

**Decision 3 — Singleton Kernel**  
The PyNova Simulation Kernel is a singleton — one simulation clock, one resource bus, one event loop — to enforce a single consistent simulation state.

---

## 2. Design Principles

### 2.1 SOLID Principles

| Principle | Application in PyNova |
|---|---|
| **Single Responsibility** | `ProcessManager` manages processes only; `Scheduler` handles scheduling only; they communicate via interfaces |
| **Open/Closed** | Algorithm classes are open for extension (new policy) but closed for modification (base interface unchanged) |
| **Liskov Substitution** | All `SchedulerPolicy` subclasses can replace the base without altering `SchedulerEngine` behaviour |
| **Interface Segregation** | `FileSystemInterface` is split from `FileSystemImplementation`; consumers depend only on the interface they use |
| **Dependency Inversion** | `SchedulerEngine` depends on the `SchedulerPolicy` abstraction, not concrete `RoundRobinPolicy` |

### 2.2 DRY (Don't Repeat Yourself)
All PCB and TCB field initialisation is centralised in factory methods. Resource tracking logic is not duplicated across `DeadlockDetector` and `ResourceManager`.

### 2.3 Separation of Concerns
Each OS subsystem is a fully isolated Python package. Cross-subsystem communication occurs only through the defined event bus or explicit API calls, never through direct attribute access across package boundaries.

---

## 3. Software Design

### 3.1 Core Data Structures

**Process Control Block (PCB)**
```python
@dataclass
class PCB:
    pid: int
    name: str
    state: ProcessState          # NEW, READY, RUNNING, WAITING, TERMINATED
    priority: int
    program_counter: int
    registers: Dict[str, int]
    memory_base: int
    memory_limit: int
    open_files: List[int]        # File descriptor table
    parent_pid: Optional[int]
    children_pids: List[int]
    cpu_burst_remaining: int
    arrival_time: float
    total_cpu_time: float
    waiting_time: float
```

**Page Table Entry**
```python
@dataclass
class PageTableEntry:
    frame_number: Optional[int]
    valid: bool
    dirty: bool
    referenced: bool
    protection: int              # read=4, write=2, execute=1
```

**Inode (File System)**
```python
@dataclass
class Inode:
    inode_number: int
    file_type: FileType          # REGULAR, DIRECTORY, SYMLINK
    size: int
    owner: str
    permissions: int             # Unix-style rwxrwxrwx
    created_at: float
    modified_at: float
    direct_blocks: List[int]     # 12 direct block pointers
    single_indirect: Optional[int]
    double_indirect: Optional[int]
    triple_indirect: Optional[int]
```

### 3.2 Module Design

```
pynova/
├── kernel/
│   ├── core.py          # Simulation kernel, event loop, simulation clock
│   ├── syscall.py       # System call dispatcher
│   └── events.py        # Event bus and observer interfaces
│
├── process/
│   ├── manager.py       # ProcessManager: create, fork, exec, terminate
│   ├── pcb.py           # PCB dataclass and ProcessState enum
│   ├── ipc.py           # Shared memory and message passing
│   └── scheduler/
│       ├── engine.py    # SchedulerEngine (policy consumer)
│       ├── policy.py    # SchedulerPolicy ABC
│       ├── fcfs.py      # FCFS implementation
│       ├── sjf.py       # SJF (preemptive + non-preemptive)
│       ├── rr.py        # Round Robin
│       ├── priority.py  # Priority Scheduling
│       ├── mlq.py       # Multilevel Queue
│       └── mlfq.py      # Multilevel Feedback Queue
│
├── thread/
│   ├── manager.py       # ThreadManager
│   ├── tcb.py           # Thread Control Block
│   └── models.py        # OneToOne, ManyToOne, ManyToMany models
│
├── sync/
│   ├── mutex.py         # Mutex implementation
│   ├── semaphore.py     # Counting and binary semaphores
│   ├── monitor.py       # Condition variables and monitors
│   └── problems/
│       ├── producer_consumer.py
│       ├── readers_writers.py
│       └── dining_philosophers.py
│
├── deadlock/
│   ├── detector.py      # RAG-based deadlock detection
│   ├── avoidance.py     # Banker's Algorithm
│   └── recovery.py      # Process termination and preemption
│
├── memory/
│   ├── main_memory.py   # Physical memory simulation
│   ├── allocator.py     # First-Fit, Best-Fit, Worst-Fit
│   ├── paging.py        # Page table, TLB
│   ├── segmentation.py  # Segment table
│   └── virtual/
│       ├── demand_paging.py
│       ├── page_fault.py
│       ├── replacement/
│       │   ├── fifo.py
│       │   ├── lru.py
│       │   ├── optimal.py
│       │   ├── lfu.py
│       │   └── clock.py
│       └── frame_allocator.py
│
├── storage/
│   ├── disk.py          # Virtual disk model
│   ├── scheduling/      # Disk scheduling algorithms
│   └── raid.py          # RAID 0, 1, 5 simulation
│
├── filesystem/
│   ├── interface.py     # VFS interface (open, read, write, etc.)
│   ├── inode.py         # Inode structure
│   ├── directory.py     # Directory structure simulation
│   ├── allocation/      # Contiguous, linked, indexed
│   └── free_space.py    # Bitmap and free list
│
├── io/
│   ├── device_driver.py # Device driver framework
│   ├── dma.py           # DMA simulation
│   └── scheduler.py     # I/O queue scheduling
│
├── protection/
│   ├── access_matrix.py # Domain and access matrix
│   └── acl.py           # ACL and capability lists
│
├── security/
│   ├── auth.py          # Authentication simulation
│   ├── threats.py       # Threat simulation
│   └── audit.py         # Security audit log
│
├── vm/
│   ├── hypervisor.py    # Type 1 / Type 2 hypervisor model
│   └── guest.py         # Guest OS instance
│
└── ui/
    ├── cli.py           # Command-line interface
    └── dashboard.py     # Rich terminal dashboard
```

---

## 4. Software Testing Strategy

### 4.1 Testing Levels

**Unit Testing**
- Every class and method is tested in isolation
- Mocks are used for inter-module dependencies
- Framework: `pytest`
- Target coverage: ≥ 80% for all modules

**Integration Testing**
- Tests cross-module interactions: e.g., Scheduler → ProcessManager → MemoryManager
- Tests system call dispatcher end-to-end
- Framework: `pytest` with integration test markers

**System Testing**
- Full end-to-end simulation scenarios
- Scenario: "Process P1 creates file, writes data, forks P2, P2 reads file, page fault occurs"
- Validates PyNova OS as a complete coherent simulation

**Acceptance Testing**
- Academic scenarios validated by instructors
- Textbook example outputs compared to PyNova simulation outputs
- Performance benchmarks (scheduling, memory page fault rates)

### 4.2 Testing Techniques

| Technique | Application |
|---|---|
| Black-box Testing | Scheduling output vs. textbook expected output |
| White-box Testing | Banker's Algorithm safe-state detection path coverage |
| Boundary Value Analysis | Memory allocation at min/max sizes; quantum = 0 and quantum = MAX_INT |
| Equivalence Partitioning | Process states (valid transitions vs. invalid transitions) |
| Regression Testing | Automated re-run of all tests on every increment merge |
| Stress Testing | 1000 concurrent simulated processes; 100,000 page references |

### 4.3 Sample Test Cases

**TC-001: Round Robin Scheduling Correctness**
- Input: P1(burst=8), P2(burst=4), P3(burst=9), quantum=4
- Expected: Gantt chart P1(0-4), P2(4-8), P3(8-12), P1(12-16), P3(16-21)
- Expected average turnaround time: 15.67 ms

**TC-002: Banker's Algorithm Safe State Detection**
- Input: 3 processes, 3 resources, Allocation/Max/Available matrices (textbook Example 8.7)
- Expected: Safe sequence [P1, P3, P4, P0, P2]

**TC-003: LRU Page Replacement**
- Input: Reference string [7,0,1,2,0,3,0,4,2,3,0,3,2], 4 frames
- Expected: 8 page faults

**TC-004: Deadlock Detection (Circular Wait)**
- Input: RAG with circular dependency P0→R1→P1→R2→P0
- Expected: Deadlock detected; affected processes: {P0, P1}

---

## 5. Software Quality Assurance

### 5.1 Code Quality Standards

- **Style:** PEP 8 enforced via `flake8` and `black` auto-formatter
- **Type Safety:** All public APIs annotated with Python type hints; checked with `mypy`
- **Docstrings:** Every public class and method has a Google-style docstring
- **Complexity:** Cyclomatic complexity ≤ 10 per method (enforced via `radon`)
- **Dependency Management:** `pyproject.toml` with pinned dependencies

### 5.2 Code Review Process

1. Developer branches from `main` into `feature/<component-name>`
2. Implementation + unit tests written together (TDD encouraged)
3. Pull Request opened; requires at least 1 peer reviewer
4. All CI checks must pass (linting, type checking, tests, coverage)
5. Reviewer approves; maintainer merges

### 5.3 Continuous Integration Pipeline

```
Trigger: Push to any branch / Pull Request

Steps:
1. Lint (flake8 + black --check)
2. Type check (mypy)
3. Unit Tests (pytest --cov)
4. Integration Tests
5. Coverage Gate (fail if < 80%)
6. Complexity Analysis (radon cc)
7. Build Validation (python -m build)
```

Tool: GitHub Actions

---

## 6. Software Configuration Management

### 6.1 Version Control
- **Tool:** Git with GitHub
- **Branching Strategy:** Gitflow
  - `main` — stable releases only
  - `develop` — integration branch
  - `feature/<name>` — per-increment development branches
  - `release/<version>` — release preparation branches
  - `hotfix/<issue>` — critical bug fixes

### 6.2 Version Numbering
Format: `MAJOR.MINOR.PATCH`
- `1.0.0` — Full system v1 (all 6 increments complete)
- `0.x.0` — Increment milestones during development
- `0.x.y` — Patch releases within an increment

### 6.3 Configuration Items Under Management
- Source code (all Python modules)
- Test suite
- Requirements Specification
- Architecture Documents
- SDLC Plan
- CI/CD pipeline configuration (`.github/workflows/`)
- `pyproject.toml` (dependencies and build config)

---

## 7. Risk Management

| Risk ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R-001 | Algorithm implementation diverges from textbook | Medium | High | Cross-validate all outputs against textbook examples in test suite |
| R-002 | Inter-module coupling makes integration difficult | Medium | High | Strict interface-only communication; enforced by code review |
| R-003 | Python GIL limits concurrency simulation realism | High | Medium | Document the limitation; use simulation clock for logical concurrency |
| R-004 | Performance inadequate for stress tests | Low | Medium | Profile early; use efficient data structures (heaps, bitmaps) |
| R-005 | Scope creep from new OS features | Medium | Medium | Change control board; all new requirements go through formal intake |
| R-006 | Key developer unavailability | Low | High | Knowledge sharing; all design decisions documented; pair programming |

---

## 8. Software Metrics

| Metric | Target | Measurement Tool |
|---|---|---|
| Code Coverage | ≥ 80% | pytest-cov |
| Cyclomatic Complexity | ≤ 10 per method | radon |
| Lines of Code (LOC) | Tracked per module | cloc |
| Defect Density | < 1 defect per 100 LOC post-release | GitHub Issues |
| Build Success Rate | ≥ 95% | GitHub Actions |
| Average Scheduling Accuracy | 100% match to textbook | Custom test assertions |
| Page Fault Rate Accuracy | ±0 from textbook examples | Custom test assertions |

---

## 9. Documentation Plan

| Document | Audience | Format | Delivery |
|---|---|---|---|
| Requirements Elicitation | All Stakeholders | Markdown | Increment 0 |
| SDLC Plan | Team | Markdown | Increment 0 |
| Architecture Design Document | Developers | Markdown + UML | Before Increment 1 |
| Module API Docs | Developers | Python docstrings + Sphinx | Per increment |
| User Guide (CLI) | Students / Instructors | Markdown | v1.0 release |
| Algorithm Reference | All | Markdown | v1.0 release |
| Test Reports | QA / Instructors | HTML (pytest-html) | Per increment |

---

## 10. Tools Summary

| Category | Tool | Purpose |
|---|---|---|
| Language | Python 3.10+ | Core implementation |
| Testing | pytest | Unit and integration tests |
| Coverage | pytest-cov | Code coverage measurement |
| Linting | flake8 + black | Style enforcement |
| Type Checking | mypy | Static type verification |
| Complexity | radon | Cyclomatic complexity |
| CI/CD | GitHub Actions | Automated pipeline |
| Documentation | Sphinx | API documentation generation |
| CLI UI | Rich | Terminal dashboard and formatting |
| Diagrams | PlantUML / draw.io | Architecture and UML diagrams |
| Version Control | Git + GitHub | Source control and collaboration |

---

*Document Version: 1.0 | Project: PyNova OS | Date: 2026*
