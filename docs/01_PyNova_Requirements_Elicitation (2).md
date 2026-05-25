# PyNova Operating System — Requirements Elicitation

---

## 1. Project Overview

**Project Name:** PyNova OS  
**Nature:** Simulated Operating System (Software Simulation)  
**Implementation Language:** Python  
**Purpose:** To simulate the full behaviour and internal workings of a modern operating system, covering all classical OS components — from process management and memory to file systems, I/O, security, and virtual machines.

PyNova OS is not a bare-metal kernel. It is a simulation layer — a Python-based OS model that faithfully reproduces the logic, data structures, algorithms, and interactions of a real operating system. It can be used for education, research, testing of OS concepts, and as a base for OS course projects.

---

## 2. Stakeholder Identification

| Stakeholder | Role | Interest |
|---|---|---|
| OS Students | Primary Users | Learning OS internals interactively |
| University Instructors | Secondary Users | Teaching and demonstration |
| Systems Programmers | Secondary Users | Prototyping OS algorithms |
| Software Researchers | Tertiary Users | Experimenting with scheduling/memory models |
| QA Engineers | Testers | Validating simulation correctness |
| Project Team | Developers | Building and maintaining PyNova |

---

## 3. Elicitation Techniques Used

- **Structured Interviews** with instructors and OS researchers
- **Document Analysis** of OS textbook chapters (Silberschatz) covering ch2–ch16
- **Observation** of existing OS simulators (NachOS, SimOS)
- **Brainstorming Sessions** with the development team
- **Prototype Review** — conceptual mockups reviewed by stakeholders
- **Survey** distributed to final-year CS students

---

## 4. Functional Requirements

### 4.1 OS Structure (ch2)
- **FR-001:** The system shall implement a layered OS architecture with user mode and kernel mode separation.
- **FR-002:** The system shall provide a simulated system call interface.
- **FR-003:** The system shall support microkernel and monolithic kernel simulation modes.
- **FR-004:** The system shall expose OS services via a defined API layer.

### 4.2 Process Management (ch3)
- **FR-005:** The system shall simulate process creation, execution, waiting, and termination.
- **FR-006:** Each process shall maintain a Process Control Block (PCB) with PID, state, priority, registers, and memory maps.
- **FR-007:** The system shall implement Inter-Process Communication (IPC) via shared memory and message passing.
- **FR-008:** The system shall support parent-child process relationships (fork/exec simulation).
- **FR-009:** The system shall transition processes through states: New → Ready → Running → Waiting → Terminated.

### 4.3 Thread Management (ch4)
- **FR-010:** The system shall implement user-level and kernel-level threads.
- **FR-011:** The system shall support the one-to-one, many-to-one, and many-to-many threading models.
- **FR-012:** Each thread shall maintain a Thread Control Block (TCB).
- **FR-013:** The system shall simulate thread creation, joining, and cancellation.

### 4.4 Process Synchronisation (ch5)
- **FR-014:** The system shall implement mutexes, semaphores, and condition variables.
- **FR-015:** The system shall simulate the critical section problem and demonstrate solutions.
- **FR-016:** The system shall implement and simulate the classic synchronisation problems: Producer-Consumer, Readers-Writers, Dining Philosophers.
- **FR-017:** The system shall detect and report race conditions in simulation.

### 4.5 CPU Scheduling (ch6)
- **FR-018:** The system shall implement the following scheduling algorithms:
  - First-Come, First-Served (FCFS)
  - Shortest Job First (SJF) — preemptive and non-preemptive
  - Round Robin (RR) with configurable quantum
  - Priority Scheduling
  - Multilevel Queue Scheduling
  - Multilevel Feedback Queue (MLFQ)
- **FR-019:** The system shall calculate and display CPU utilisation, throughput, turnaround time, waiting time, and response time for each algorithm.
- **FR-020:** The system shall support multi-processor and multi-core CPU simulation.

### 4.6 Deadlock (ch7)
- **FR-021:** The system shall model the four conditions for deadlock: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.
- **FR-022:** The system shall implement deadlock detection using a Resource Allocation Graph (RAG).
- **FR-023:** The system shall implement the Banker's Algorithm for deadlock avoidance.
- **FR-024:** The system shall simulate deadlock recovery via process termination and resource preemption.

### 4.7 Main Memory Management (ch8)
- **FR-025:** The system shall implement contiguous memory allocation with First-Fit, Best-Fit, and Worst-Fit strategies.
- **FR-026:** The system shall simulate fixed and dynamic partitioning.
- **FR-027:** The system shall implement segmentation with a segment table.
- **FR-028:** The system shall implement paging with a page table.
- **FR-029:** The system shall simulate internal and external fragmentation and compaction.

### 4.8 Virtual Memory (ch9)
- **FR-030:** The system shall implement demand paging.
- **FR-031:** The system shall implement page replacement algorithms: FIFO, LRU, Optimal, LFU, and Clock (Second-Chance).
- **FR-032:** The system shall simulate page faults and handle them via the simulated page fault handler.
- **FR-033:** The system shall detect and simulate thrashing.
- **FR-034:** The system shall implement frame allocation strategies: equal and proportional allocation.

### 4.9 Mass Storage (ch10)
- **FR-035:** The system shall simulate a virtual disk with configurable tracks, sectors, and cylinders.
- **FR-036:** The system shall implement disk scheduling algorithms: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK.
- **FR-037:** The system shall simulate RAID levels 0, 1, and 5.
- **FR-038:** The system shall model disk seek time, rotational latency, and transfer time.

### 4.10 File System Interface (ch11)
- **FR-039:** The system shall implement a virtual file system interface with create, open, read, write, close, delete, and seek operations.
- **FR-040:** The system shall support file attributes: name, type, size, permissions, timestamps.
- **FR-041:** The system shall simulate directory structures: single-level, two-level, tree, and acyclic graph.
- **FR-042:** The system shall implement file access methods: sequential, direct, and indexed.

### 4.11 File System Implementation (ch12)
- **FR-043:** The system shall simulate file allocation methods: contiguous, linked, and indexed.
- **FR-044:** The system shall implement a simulated inode structure.
- **FR-045:** The system shall simulate free-space management using bitmaps and free lists.
- **FR-046:** The system shall implement a virtual File Allocation Table (FAT) structure.
- **FR-047:** The system shall simulate buffer cache and directory caching.

### 4.12 I/O Systems (ch13)
- **FR-048:** The system shall simulate device drivers for a variety of virtual device types.
- **FR-049:** The system shall implement DMA (Direct Memory Access) simulation.
- **FR-050:** The system shall implement I/O scheduling and device queues.
- **FR-051:** The system shall simulate polling, interrupt-driven, and DMA-driven I/O modes.
- **FR-052:** The system shall support spooling simulation for print-type devices.

### 4.13 Protection (ch14)
- **FR-053:** The system shall implement a domain and access matrix model.
- **FR-054:** The system shall enforce access rights: read, write, execute.
- **FR-055:** The system shall implement capability lists and access control lists (ACLs).
- **FR-056:** The system shall simulate privilege escalation and revocation of access.

### 4.14 Security (ch15)
- **FR-057:** The system shall simulate cryptographic authentication (password hashing simulation).
- **FR-058:** The system shall implement a simulated firewall and intrusion detection hook.
- **FR-059:** The system shall simulate common threats: buffer overflow, Trojan horse, worm propagation.
- **FR-060:** The system shall log all security events to a simulated audit trail.

### 4.15 Virtual Machines (ch16)
- **FR-061:** The system shall simulate a Type 1 (bare-metal) and Type 2 (hosted) hypervisor model.
- **FR-062:** The system shall allow multiple simulated guest OS instances to run simultaneously.
- **FR-063:** The system shall simulate VM creation, suspension, resumption, and migration.
- **FR-064:** The system shall model CPU, memory, and I/O resource partitioning across VMs.

---

## 5. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-001 | Performance | Simulation of 100 concurrent processes shall complete scheduling cycles within 500 ms |
| NFR-002 | Usability | All components shall expose a command-line interface and optional visual dashboard |
| NFR-003 | Portability | PyNova shall run on Windows, Linux, and macOS with Python 3.10+ |
| NFR-004 | Reliability | The simulation shall not crash on invalid input; all errors must be handled gracefully |
| NFR-005 | Extensibility | New scheduling algorithms or memory strategies shall be pluggable via a policy interface |
| NFR-006 | Maintainability | Code shall conform to PEP 8 and maintain >80% test coverage |
| NFR-007 | Observability | All simulation steps shall be loggable with configurable verbosity levels |
| NFR-008 | Accuracy | All algorithm implementations shall produce outputs consistent with textbook examples |

---

## 6. System Constraints

- **Language Constraint:** Python 3.10+ exclusively; no compiled C/C++ extensions in the core
- **No Real Hardware Access:** Simulation only; no actual disk, memory, or CPU interaction
- **No Network Stack:** Network I/O is not in scope for v1.0
- **Single Machine:** All simulation runs on a single host machine
- **Time Constraint:** v1.0 must be delivered within a 16-week development cycle

---

## 7. Assumptions

1. Users have a basic understanding of OS concepts.
2. PyNova will be used in an academic setting initially.
3. All hardware is simulated in software; no real device interaction is expected.
4. Python's threading library may be used for concurrency simulation but is not the primary simulation model.
5. File system simulation is in-memory; no actual disk writes are made.

---

## 8. Requirements Traceability Matrix (Partial)

| Requirement ID | Source | Component | Priority |
|---|---|---|---|
| FR-005 to FR-009 | ch3 lecture / Silberschatz | Process Manager | High |
| FR-018 to FR-020 | ch6 lecture | CPU Scheduler | High |
| FR-030 to FR-034 | ch9 lecture | Virtual Memory Manager | High |
| FR-039 to FR-042 | ch11 lecture | File System Interface | Medium |
| FR-057 to FR-060 | ch15 lecture | Security Module | Medium |
| FR-061 to FR-064 | ch16 lecture | VM Hypervisor | Low |

---

*Document Version: 1.0 | Project: PyNova OS | Date: 2026*
