# PyNova OS — Software Development Life Cycle (SDLC)

---

## 1. Selected SDLC Model: Incremental Iterative Development Model

### Justification

PyNova OS is a large, multi-component simulation system that mirrors the complexity of a real operating system. The project spans 15+ distinct OS subsystems, each with well-understood requirements (drawn directly from established OS theory and textbook chapters) but with significant interdependencies between components.

The **Incremental Iterative Model** was selected for the following reasons:

**1. Component Independence Permits Incremental Delivery**  
Each OS component (Process Manager, Scheduler, Memory Manager, File System, etc.) can be developed, tested, and delivered as a working increment independently. A user can run the Process Management simulation before the Virtual Memory module is complete. This aligns with the incremental model's core principle: deliver functional software frequently.

**2. Requirements Are Well-Understood But Deep**  
Unlike exploratory research projects (which would favour Agile/Spiral), PyNova has stable, textbook-derived requirements from day one. However, the implementation complexity of algorithms such as Banker's Algorithm, MLFQ, LRU page replacement, and FAT file allocation warrants iterative refinement rather than a waterfall single-pass. The iterative dimension accommodates feedback and algorithm tuning without scope instability.

**3. Risk Reduction Through Early Testing**  
By delivering and testing the Process Management and CPU Scheduling core early (Increments 1 and 2), the team validates the simulation framework architecture before committing to the heavier Memory and File System layers. This is consistent with how the Incremental model manages technical risk.

**4. Academic and Demonstration Milestones**  
The project's academic context demands that each subsystem be demonstrable at a course milestone. The incremental model naturally produces milestone-ready deliverables at the end of each increment.

**5. Why Not Pure Waterfall?**  
Waterfall would require all components to be designed and implemented before any testing. Given the algorithmic depth of modules like Virtual Memory (page replacement, thrashing, frame allocation) and Deadlock (Banker's Algorithm), defects discovered late in testing would be expensive to fix.

**6. Why Not Pure Agile/Scrum?**  
Agile is excellent for projects with evolving or poorly-understood requirements. PyNova's requirements are derived from established OS theory (Silberschatz), making them stable and comprehensive. Pure Scrum's sprint-based iteration without architectural planning would lead to poor subsystem integration in a system as interdependent as an OS simulation.

---

## 2. SDLC Phases and Activities

### Phase 1: Requirements & Planning (Weeks 1–2)

**Objective:** Define the full scope of all OS components to be simulated.

**Activities:**
- Stakeholder identification (students, instructors, researchers)
- Requirements elicitation via document analysis of ch2–ch16 slides
- Functional and non-functional requirements documentation
- Risk analysis and mitigation planning
- Definition of increment boundaries and delivery schedule
- Technology stack selection (Python 3.10+, pytest, Rich CLI library)

**Deliverables:**
- Requirements Specification Document
- Project Plan & Increment Schedule
- Risk Register

---

### Phase 2: System Architecture Design (Weeks 3–4)

**Objective:** Design the overall PyNova simulation architecture that all increments will build upon.

**Activities:**
- Design the PyNova Core Framework: simulation clock, event loop, inter-module communication bus
- Define the base abstractions: `Process`, `Thread`, `Resource`, `Device`, `FileNode`
- Design the system call dispatcher
- Define the plugin/policy interface for swappable algorithms (e.g., `SchedulerPolicy`, `PageReplacementPolicy`)
- Design the visualisation and logging layer
- Produce Architecture Design Document (ADD) and component diagrams

**Deliverables:**
- System Architecture Document
- UML Component and Class Diagrams
- Interface Specifications for all modules

---

### Phase 3: Increment 1 — OS Core + Process & Thread Management (Weeks 5–6)

**Scope:** ch2 (OS Structures), ch3 (Processes), ch4 (Threads)

**Development Activities:**
- Implement PyNova Core simulation engine (kernel mode/user mode, system call interface)
- Implement `ProcessManager` with full PCB data structure
- Implement process state machine (New → Ready → Running → Waiting → Terminated)
- Implement IPC: shared memory and message passing channels
- Implement `ThreadManager` with TCB and three threading models
- Implement fork/exec simulation

**Testing Activities:**
- Unit tests for PCB and TCB structures
- Process lifecycle tests (creation to termination)
- IPC correctness tests
- Threading model tests (one-to-one, many-to-one, many-to-many)

**Review:** Increment 1 demo to stakeholders. Feedback incorporated.

---

### Phase 4: Increment 2 — Synchronisation, Scheduling & Deadlock (Weeks 7–8)

**Scope:** ch5 (Synchronisation), ch6 (CPU Scheduling), ch7 (Deadlock)

**Development Activities:**
- Implement synchronisation primitives: Mutex, Semaphore, Condition Variable
- Simulate critical section problems and their solutions
- Implement classic problems: Producer-Consumer, Readers-Writers, Dining Philosophers
- Implement all 6 CPU scheduling algorithms (FCFS, SJF, RR, Priority, MLQ, MLFQ)
- Build scheduling metrics dashboard (utilisation, throughput, turnaround time, etc.)
- Implement deadlock detection (RAG), avoidance (Banker's Algorithm), and recovery

**Testing Activities:**
- Race condition detection tests
- Scheduling algorithm output vs. textbook reference tests
- Banker's Algorithm safe-state detection tests
- RAG cycle detection correctness tests

**Review:** Increment 2 demo. Scheduling comparison dashboard validated.

---

### Phase 5: Increment 3 — Memory Management (Weeks 9–10)

**Scope:** ch8 (Main Memory), ch9 (Virtual Memory)

**Development Activities:**
- Implement contiguous allocation (First-Fit, Best-Fit, Worst-Fit)
- Implement segmentation with segment table simulation
- Implement paging with page table and TLB simulation
- Implement demand paging and page fault handler
- Implement all page replacement algorithms (FIFO, LRU, Optimal, LFU, Clock)
- Simulate thrashing detection and working-set model
- Frame allocation (equal and proportional)

**Testing Activities:**
- Memory fragmentation tests
- Page fault rate benchmarking per algorithm
- Belady's Anomaly demonstration test
- Thrashing onset detection test

**Review:** Increment 3 demo to academic stakeholders.

---

### Phase 6: Increment 4 — Storage & File Systems (Weeks 11–12)

**Scope:** ch10 (Mass Storage), ch11 (File System Interface), ch12 (File System Implementation)

**Development Activities:**
- Implement virtual disk model (tracks, sectors, cylinders)
- Implement disk scheduling algorithms (FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK)
- Simulate RAID 0, 1, and 5
- Implement virtual file system interface (CRUD operations, file attributes)
- Simulate directory structures (single-level, two-level, tree, acyclic graph)
- Implement file allocation methods (contiguous, linked, indexed / FAT)
- Implement inode structure and free-space management (bitmap and free list)

**Testing Activities:**
- Disk scheduling algorithm seek-distance comparison tests
- RAID 1 fault-tolerance simulation tests
- File allocation correctness and fragmentation tests
- Directory traversal and path resolution tests

---

### Phase 7: Increment 5 — I/O, Protection & Security (Weeks 13–14)

**Scope:** ch13 (I/O Systems), ch14 (Protection), ch15 (Security)

**Development Activities:**
- Implement virtual device driver framework
- Simulate DMA, interrupt-driven, and polling I/O modes
- Implement device queues, spooling, and I/O scheduling
- Implement domain and access matrix model
- Implement ACLs and capability lists; simulate privilege escalation
- Simulate security threats (buffer overflow, Trojan, worm)
- Implement audit trail and security event logging
- Simulate password hashing and authentication

**Testing Activities:**
- I/O throughput and DMA correctness tests
- ACL enforcement tests (positive and negative access scenarios)
- Security audit log completeness tests
- Threat simulation containment tests

---

### Phase 8: Increment 6 — Virtual Machines (Week 15)

**Scope:** ch16 (Virtual Machines)

**Development Activities:**
- Implement Type 1 and Type 2 hypervisor simulation models
- Implement VM lifecycle: creation, suspension, resumption, migration
- Implement CPU, memory, and I/O resource partitioning across VMs
- Run multiple guest OS instances (PyNova instances) concurrently

**Testing Activities:**
- VM isolation tests (one VM cannot access another VM's resources)
- Resource partitioning correctness tests
- VM migration state consistency tests

---

### Phase 9: System Integration & Full Testing (Week 15–16)

**Objective:** Integrate all increments into a cohesive PyNova OS simulation.

**Activities:**
- Full system integration testing across all modules
- End-to-end scenario tests (e.g., process creates file, accesses disk, triggers page fault)
- Performance benchmarking
- Regression testing for all previously passed tests
- Documentation finalization
- User Acceptance Testing (UAT) with student and instructor stakeholders

**Deliverables:**
- Integration Test Report
- Performance Benchmarking Report
- Final PyNova OS Release v1.0

---

### Phase 10: Maintenance & Extension (Post-Week 16)

**Activities:**
- Bug fixes identified during UAT
- Algorithm plugin extensions (new scheduling or replacement policies)
- Documentation updates
- v1.1 planning (e.g., network stack simulation, real-time OS simulation mode)

---

## 3. SDLC Summary Gantt (High-Level)

```
Week:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
Phase 1:  [==========]
Phase 2:           [==========]
Incr 1:                    [==========]
Incr 2:                             [==========]
Incr 3:                                      [==========]
Incr 4:                                               [==========]
Incr 5:                                                        [======]
Incr 6:                                                              [==]
Phase 9:                                                           [=====]
```

---

## 4. SDLC Model Alternatives Considered

| Model | Considered? | Rejection Reason |
|---|---|---|
| Waterfall | Yes | Too rigid; late defect discovery risk in deep algorithm modules |
| Agile / Scrum | Yes | Requirements are stable and OS-theory-derived; not exploratory |
| Spiral | Yes | Risk-driven spirals add overhead unnecessary for textbook-defined scope |
| Prototype | Yes | Appropriate for UI/UX; overkill as primary model for a simulation engine |
| **Incremental Iterative** | **Selected** | Best match for stable, modular, component-oriented OS simulation |

---

*Document Version: 1.0 | Project: PyNova OS | Date: 2026*
