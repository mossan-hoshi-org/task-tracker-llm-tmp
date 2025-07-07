import tkinter as tk
from unittest.mock import Mock, patch

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

    def test_main_window_has_task_input_field(self) -> None:
        window = MainWindow()

        assert hasattr(window, "task_input")
        assert isinstance(window.task_input, tk.Entry)

    def test_main_window_has_start_button(self) -> None:
        window = MainWindow()

        assert hasattr(window, "start_button")
        assert isinstance(window.start_button, tk.Button)
        assert window.start_button["text"] == "▶ 計測開始"

    def test_start_button_is_disabled_when_input_is_empty(self) -> None:
        window = MainWindow()
        window.task_input.delete(0, tk.END)

        assert window.start_button["state"] == "disabled"

    def test_start_button_is_enabled_when_input_has_text(self) -> None:
        window = MainWindow()
        window.task_input.insert(0, "テストタスク")
        window._on_input_change(None)

        assert window.start_button["state"] == "normal"

    def test_main_window_has_task_tracker(self) -> None:
        window = MainWindow()

        assert hasattr(window, "task_tracker")
        assert window.task_tracker is not None

    @patch("src.ui.main_window.TaskTracker")
    def test_start_button_starts_new_task(self, mock_tracker_class: Mock) -> None:
        mock_tracker = Mock()
        mock_tracker_class.return_value = mock_tracker

        window = MainWindow()
        window.task_input.insert(0, "New Task")
        window._on_start_click()

        mock_tracker.start_task.assert_called_once_with("New Task")

    def test_start_button_clears_input_after_click(self) -> None:
        window = MainWindow()
        window.task_input.insert(0, "Task to clear")
        window._on_start_click()

        assert window.task_input.get() == ""
        assert window.start_button["state"] == "disabled"
