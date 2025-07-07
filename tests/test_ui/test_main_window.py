import pytest
import tkinter as tk
from unittest.mock import Mock, patch

from src.ui.main_window import MainWindow


class TestMainWindow:
    def test_main_window_creates_tkinter_root(self):
        window = MainWindow()
        
        assert window.root is not None
        assert isinstance(window.root, tk.Tk)
    
    def test_main_window_has_correct_title(self):
        window = MainWindow()
        
        assert window.root.title() == "Task Tracker"
    
    def test_main_window_has_minimum_size(self):
        window = MainWindow()
        
        assert window.root.minsize() == (600, 400)