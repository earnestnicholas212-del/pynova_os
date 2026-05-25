#!/usr/bin/env python3
"""
PyNova OS Simulator
Main entry point. Boot the GUI from here.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import tkinter as tk
from gui.app import PyNovaGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = PyNovaGUI(root)
    root.mainloop()
