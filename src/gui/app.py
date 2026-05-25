#!/usr/bin/env python3
"""
Tkinter GUI for PyNova OS Simulator
Provides real-time visualization of CPU scheduling, memory usage, and process tables.
"""

import sys
import os

# Ensure src is in path when running gui module directly
_src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from kernel.process_manager import OSSystem


class PyNovaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyNova OS Simulator")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1d23")

        self.system = OSSystem()
        self.running = False
        self.speed = 500  # ms per tick

        self._build_ui()
        self._update_visuals()

    def _build_ui(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Card.TLabelframe", background="#1a1d23", foreground="#00d9ff", borderwidth=1)
        style.configure("Card.TLabelframe.Label", font=("Consolas", 10, "bold"))
        style.configure("Card.TLabel", background="#1a1d23", foreground="#e0e5ec")
        style.configure("Treeview", background="#1a1d23", fieldbackground="#1a1d23", foreground="#e0e5ec", rowheight=24, bordercolor="#2a2f38", borderwidth=0)
        style.map("Treeview", background=[("selected", "#00d9ff")], foreground=[("selected", "#1a1d23")])
        style.configure("Treeview.Heading", background="#2a2f38", foreground="#00d9ff", relief="flat", font=("Consolas", 9, "bold"))

        # Top Bar
        top = tk.Frame(self.root, bg="#1a1d23", height=50)
        top.pack(fill=tk.X, padx=12, pady=8)
        tk.Label(top, text="PyNova OS Simulator", fg="#00d9ff", bg="#1a1d23", font=("Consolas", 18, "bold")).pack(side=tk.LEFT)
        self.status_label = tk.Label(top, text="STATUS: HALTED", fg="#8a92a3", bg="#1a1d23", font=("Consolas", 10))
        self.status_label.pack(side=tk.RIGHT)

        # Main Paned Window
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#1a1d23", sashrelief=tk.FLAT, sashpad=6)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left: Controls
        left = tk.Frame(paned, bg="#21252b", width=300)
        left.pack_propagate(False)
        paned.add(left)

        # Spawn Process
        spawn_frame = ttk.LabelFrame(left, text="SPAWN PROCESS", style="Card.TLabelframe", labelanchor="n")
        spawn_frame.pack(fill=tk.X, padx=12, pady=12)
        tk.Label(spawn_frame, text="Burst Time (s)", fg="#e0e5ec", bg="#21252b", font=("Consolas", 9)).pack(anchor=tk.W, padx=8, pady=(10, 2))
        self.burst_var = tk.StringVar(value="5")
        tk.Entry(spawn_frame, textvariable=self.burst_var, bg="#2d3340", fg="#e0e5ec", insertbackground="#e0e5ec", relief=tk.FLAT, font=("Consolas", 10)).pack(fill=tk.X, padx=8)
        tk.Label(spawn_frame, text="Priority (1-10)", fg="#e0e5ec", bg="#21252b", font=("Consolas", 9)).pack(anchor=tk.W, padx=8, pady=(10, 2))
        self.priority_var = tk.StringVar(value="1")
        tk.Entry(spawn_frame, textvariable=self.priority_var, bg="#2d3340", fg="#e0e5ec", insertbackground="#e0e5ec", relief=tk.FLAT, font=("Consolas", 10)).pack(fill=tk.X, padx=8)
        tk.Label(spawn_frame, text="Memory (MB)", fg="#e0e5ec", bg="#21252b", font=("Consolas", 9)).pack(anchor=tk.W, padx=8, pady=(10, 2))
        self.mem_var = tk.StringVar(value="128")
        tk.Entry(spawn_frame, textvariable=self.mem_var, bg="#2d3340", fg="#e0e5ec", insertbackground="#e0e5ec", relief=tk.FLAT, font=("Consolas", 10)).pack(fill=tk.X, padx=8)
        tk.Button(spawn_frame, text="INJECT PROCESS", command=self._spawn, bg="#00d9ff", fg="#1a1d23", relief=tk.FLAT, cursor="hand2", font=("Consolas", 10, "bold")).pack(fill=tk.X, padx=8, pady=12)

        # Config
        cfg_frame = ttk.LabelFrame(left, text="SYSTEM CONFIG", style="Card.TLabelframe", labelanchor="n")
        cfg_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        tk.Label(cfg_frame, text="Scheduler", fg="#e0e5ec", bg="#21252b", font=("Consolas", 9)).pack(anchor=tk.W, padx=8, pady=(10, 2))
        self.algo_var = tk.StringVar(value="Round Robin")
        algo_combo = ttk.Combobox(cfg_frame, textvariable=self.algo_var, values=["Round Robin", "FCFS", "SJF", "SRTF", "Priority", "Priority (Preemptive)"], state="readonly", font=("Consolas", 10))
        algo_combo.pack(fill=tk.X, padx=8)
        algo_combo.bind("<<ComboboxSelected>>", self._change_algo)
        tk.Label(cfg_frame, text="Time Quantum", fg="#e0e5ec", bg="#21252b", font=("Consolas", 9)).pack(anchor=tk.W, padx=8, pady=(10, 2))
        self.quantum_var = tk.StringVar(value="2")
        tk.Entry(cfg_frame, textvariable=self.quantum_var, bg="#2d3340", fg="#e0e5ec", insertbackground="#e0e5ec", relief=tk.FLAT, font=("Consolas", 10)).pack(fill=tk.X, padx=8)
        self.btn_toggle = tk.Button(cfg_frame, text="BOOT OS", command=self._toggle, bg="#39ff14", fg="#1a1d23", relief=tk.FLAT, cursor="hand2", font=("Consolas", 10, "bold"))
        self.btn_toggle.pack(fill=tk.X, padx=8, pady=12)

        # Logs
        log_frame = ttk.LabelFrame(left, text="KERNEL LOG", style="Card.TLabelframe", labelanchor="n")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.log_text = tk.Text(log_frame, bg="#1a1d23", fg="#8a92a3", font=("Consolas", 9), relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD, bd=0)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(8, 0), pady=8)
        log_scroll = tk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scroll.pack(fill=tk.Y, side=tk.RIGHT, padx=(0, 8), pady=8)
        self.log_text.config(yscrollcommand=log_scroll.set)

        # Center: Visualization
        center = tk.Frame(paned, bg="#1a1d23")
        paned.add(center)
        center.columnconfigure(0, weight=1)

        overview_frame = tk.Frame(center, bg="#1a1d23")
        overview_frame.pack(fill=tk.X, padx=10, pady=(8, 5))
        overview_frame.columnconfigure(0, weight=1)
        overview_frame.columnconfigure(1, weight=1)

        cpu_frame = ttk.LabelFrame(overview_frame, text="CPU PIPELINE", style="Card.TLabelframe", labelanchor="n")
        cpu_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=2)
        self.cpu_canvas = tk.Canvas(cpu_frame, bg="#1a1d23", height=120, highlightthickness=0)
        self.cpu_canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        mem_frame = ttk.LabelFrame(overview_frame, text="MEMORY MATRIX", style="Card.TLabelframe", labelanchor="n")
        mem_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=2)
        self.mem_canvas = tk.Canvas(mem_frame, bg="#1a1d23", height=120, highlightthickness=0)
        self.mem_canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        charts_container = tk.Frame(center, bg="#1a1d23")
        charts_container.pack(fill=tk.BOTH, padx=10, pady=5)
        charts_container.columnconfigure(0, weight=1)
        charts_container.columnconfigure(1, weight=1)

        chart1_frame = ttk.LabelFrame(charts_container, text="CPU UTILIZATION", style="Card.TLabelframe", labelanchor="n")
        chart1_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=2)
        self.fig_cpu = Figure(figsize=(4.5, 2.2), dpi=80, facecolor="#2a2f38")
        self.ax_cpu = self.fig_cpu.add_subplot(111)
        self.ax_cpu.set_facecolor("#1a1d23")
        self.ax_cpu.tick_params(colors="#8a92a3", labelsize=9)
        self.ax_cpu.set_ylim(0, 100)
        self.line_cpu, = self.ax_cpu.plot([], [], color="#00d9ff", linewidth=3)
        self.fig_cpu.tight_layout()
        self.canvas_cpu = FigureCanvasTkAgg(self.fig_cpu, master=chart1_frame)
        self.canvas_cpu.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        chart2_frame = ttk.LabelFrame(charts_container, text="MEMORY UTILIZATION", style="Card.TLabelframe", labelanchor="n")
        chart2_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=2)
        self.fig_mem = Figure(figsize=(4.5, 2.2), dpi=80, facecolor="#2a2f38")
        self.ax_mem = self.fig_mem.add_subplot(111)
        self.ax_mem.set_facecolor("#1a1d23")
        self.ax_mem.tick_params(colors="#8a92a3", labelsize=9)
        self.ax_mem.set_ylim(0, 100)
        self.line_mem, = self.ax_mem.plot([], [], color="#39ff14", linewidth=3)
        self.fig_mem.tight_layout()
        self.canvas_mem = FigureCanvasTkAgg(self.fig_mem, master=chart2_frame)
        self.canvas_mem.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        list_frame = ttk.LabelFrame(center, text="PROCESS TABLE", style="Card.TLabelframe", labelanchor="n")
        list_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)
        self.proc_tree = ttk.Treeview(list_frame, columns=("name", "status", "priority", "burst", "remain", "memory"), show="headings", selectmode="none", height=10)
        self.proc_tree.heading("name", text="Name")
        self.proc_tree.heading("status", text="Status")
        self.proc_tree.heading("priority", text="PRI")
        self.proc_tree.heading("burst", text="Burst")
        self.proc_tree.heading("remain", text="Remain")
        self.proc_tree.heading("memory", text="Memory")
        self.proc_tree.column("name", width=160, anchor="w")
        self.proc_tree.column("status", width=100, anchor="center")
        self.proc_tree.column("priority", width=50, anchor="center")
        self.proc_tree.column("burst", width=70, anchor="center")
        self.proc_tree.column("remain", width=70, anchor="center")
        self.proc_tree.column("memory", width=70, anchor="center")
        self.proc_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(8, 0), pady=8)
        proc_scroll = tk.Scrollbar(list_frame, command=self.proc_tree.yview)
        proc_scroll.pack(fill=tk.Y, side=tk.RIGHT, padx=(0, 8), pady=8)
        self.proc_tree.configure(yscrollcommand=proc_scroll.set)

        # Right: Live Statistics
        right = tk.Frame(paned, bg="#2a2f38", width=320)
        paned.add(right)

        stats_frame = ttk.LabelFrame(right, text="LIVE STATISTICS", style="Card.TLabelframe", labelanchor="n")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.stats_text = tk.Text(stats_frame, bg="#2a2f38", fg="#e0e5ec", font=("Consolas", 10), relief=tk.FLAT, state=tk.DISABLED, height=12)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _spawn(self):
        try:
            burst = int(self.burst_var.get())
            priority = int(self.priority_var.get())
            mem = int(self.mem_var.get())
            name = f"Process {len(self.system.processes)+1}"
            success = self.system.add_process(name, burst, priority, mem)
            if not success:
                self._log("Failed to spawn process: Out of Memory", "error")
        except ValueError:
            self._log("Invalid input values", "error")

    def _change_algo(self, event=None):
        algo = self.algo_var.get()
        try:
            q = int(self.quantum_var.get())
        except ValueError:
            q = 2
        self.system.set_algorithm(algo, q)
        self._log(f"Scheduler switched to {algo} (Quantum: {q})", "info")

    def _toggle(self):
        self.running = not self.running
        if self.running:
            self.btn_toggle.config(text="HALT SYSTEM", bg="#ff6b35")
            self.status_label.config(text="STATUS: RUNNING", fg="#39ff14")
            self._run_step()
        else:
            self.btn_toggle.config(text="BOOT OS", bg="#39ff14")
            self.status_label.config(text="STATUS: HALTED", fg="#8a92a3")

    def _run_step(self):
        if not self.running:
            return
        self.system.tick()
        self._update_visuals()
        self.root.after(self.speed, self._run_step)

    def _log(self, msg, level="info"):
        tag = level
        color = "#8a92a3"
        if level == "success":
            color = "#39ff14"
        elif level == "error":
            color = "#ff6b35"
        self.log_text.tag_config(tag, foreground=color)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{msg}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _update_visuals(self):
        # Update CPU Canvas
        self.cpu_canvas.delete("all")
        running = self.system.cpu.running_process
        if running:
            self.cpu_canvas.create_rectangle(10, 10, 140, 100, fill=running.color, outline="#00d9ff", width=2)
            self.cpu_canvas.create_text(75, 55, text=running.name, fill="white", font=("Consolas", 10, "bold"))
            self.cpu_canvas.create_text(75, 75, text=f"Remain: {running.remaining_time}s", fill="white", font=("Consolas", 8))
        else:
            self.cpu_canvas.create_text(75, 55, text="IDLE", fill="#3d4451", font=("Consolas", 14, "bold"))

        # Ready Queue
        x = 160
        for proc in self.system.cpu.queue:
            self.cpu_canvas.create_rectangle(x, 20, x+80, 90, fill=proc.color, outline="#3d4451", width=1)
            self.cpu_canvas.create_text(x+40, 55, text=proc.name, fill="white", font=("Consolas", 8))
            x += 90

        # Memory Canvas
        self.mem_canvas.delete("all")
        w = self.mem_canvas.winfo_width() or 600
        total = self.system.memory.total
        used = self.system.memory.used
        free = total - used
        bar_w = w - 20
        used_w = (used / total) * bar_w if total else 0
        self.mem_canvas.create_rectangle(10, 20, 10 + used_w, 60, fill="#00d9ff", outline="")
        self.mem_canvas.create_rectangle(10 + used_w, 20, 10 + bar_w, 60, fill="#3d4451", outline="")
        self.mem_canvas.create_text(w//2, 80, text=f"Used: {used}MB / Free: {free}MB", fill="#8a92a3", font=("Consolas", 9))

        # Process List
        for item in self.proc_tree.get_children():
            self.proc_tree.delete(item)
        self.proc_tree.tag_configure("new", foreground="#8a92a3")
        self.proc_tree.tag_configure("ready", foreground="#e0e5ec")
        self.proc_tree.tag_configure("running", foreground="#00d9ff")
        self.proc_tree.tag_configure("completed", foreground="#39ff14")
        for p in self.system.processes:
            self.proc_tree.insert("", tk.END, iid=p.pid, values=(p.name, p.status, p.priority, p.burst_time, p.remaining_time, p.memory_size), tags=(p.status,))

        # Charts
        times = [s['time'] for s in self.system.stats_history]
        cpus = [s['cpu'] for s in self.system.stats_history]
        mems = [s['mem'] for s in self.system.stats_history]
        self.line_cpu.set_data(times, cpus)
        self.ax_cpu.set_xlim(max(0, self.system.env.now-30), max(30, self.system.env.now+5))
        self.ax_cpu.set_ylim(0, 100)
        self.canvas_cpu.draw()

        self.line_mem.set_data(times, mems)
        self.ax_mem.set_xlim(max(0, self.system.env.now-30), max(30, self.system.env.now+5))
        self.ax_mem.set_ylim(0, 100)
        self.canvas_mem.draw()

        # Stats
        stats = self.system.get_stats()
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Current Time:     {self.system.env.now}s\n")
        self.stats_text.insert(tk.END, f"Running Process:  {stats['running']}\n")
        self.stats_text.insert(tk.END, f"Total Processes:  {stats['total']}\n")
        self.stats_text.insert(tk.END, f"Completed:        {stats['completed']}\n")
        self.stats_text.insert(tk.END, f"Avg Wait Time:    {stats['avg_wait']:.2f}s\n")
        self.stats_text.insert(tk.END, f"Avg Turnaround:   {stats['avg_turnaround']:.2f}s\n")
        self.stats_text.insert(tk.END, f"Throughput:       {stats['throughput']:.2f} p/s\n")
        self.stats_text.insert(tk.END, f"CPU Utilization:  {stats['cpu_util']}%\n")
        self.stats_text.insert(tk.END, f"Memory Util:      {stats['mem_util']:.1f}%\n")
        self.stats_text.config(state=tk.DISABLED)

        # Sync logs
        for t, msg, level in self.system.logs:
            self._log(f"[T+{t}] {msg}", level)
        self.system.logs.clear()
