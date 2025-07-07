import tkinter as tk

from src.ui.main_window import MainWindow


class TestMainWindow:
    def test_main_window_creates_tkinter_root(self) -> None:
        window = MainWindow()

        assert window.root is not None
        assert isinstance(window.root, tk.Tk)

    def test_main_window_has_correct_title(self) -> None:
        window = MainWindow()

        assert window.root.title() == "Task Tracker"

    def test_main_window_has_minimum_size(self) -> None:
        window = MainWindow()

        assert window.root.minsize() == (600, 400)
