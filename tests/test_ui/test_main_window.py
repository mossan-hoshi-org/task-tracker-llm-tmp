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
        mock_tracker.get_all_sessions.return_value = []
        mock_tracker.current_session = None
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

    def test_main_window_has_pause_button(self) -> None:
        window = MainWindow()

        assert hasattr(window, "pause_button")
        assert isinstance(window.pause_button, tk.Button)
        assert window.pause_button["text"] == "⏸ 一時停止"
        assert window.pause_button["state"] == "disabled"

    def test_pause_button_enabled_when_task_running(self) -> None:
        window = MainWindow()
        window.task_input.insert(0, "Test Task")
        window._on_start_click()

        assert window.pause_button["state"] == "normal"

    def test_pause_button_toggles_to_resume(self) -> None:
        window = MainWindow()
        window.task_input.insert(0, "Test Task")
        window._on_start_click()
        window._on_pause_click()

        assert window.pause_button["text"] == "▶ 再開"
        assert window.task_tracker.current_session is not None
        assert window.task_tracker.current_session.is_paused is True

    def test_resume_button_toggles_back_to_pause(self) -> None:
        window = MainWindow()
        window.task_input.insert(0, "Test Task")
        window._on_start_click()
        window._on_pause_click()
        window._on_pause_click()

        assert window.pause_button["text"] == "⏸ 一時停止"
        assert window.task_tracker.current_session is not None
        assert window.task_tracker.current_session.is_paused is False

    def test_main_window_has_task_list(self) -> None:
        window = MainWindow()

        assert hasattr(window, "task_list")
        assert isinstance(window.task_list, tk.Listbox)

    def test_task_list_shows_started_tasks(self) -> None:
        window = MainWindow()
        window.task_input.insert(0, "Task 1")
        window._on_start_click()

        assert window.task_list.size() == 1
        assert "Task 1" in window.task_list.get(0)

    def test_task_list_shows_multiple_tasks(self) -> None:
        window = MainWindow()

        for i in range(3):
            window.task_input.insert(0, f"Task {i+1}")
            window._on_start_click()

        assert window.task_list.size() == 3
        for i in range(3):
            assert f"Task {i+1}" in window.task_list.get(i)

    def test_main_window_has_stop_button(self) -> None:
        window = MainWindow()

        assert hasattr(window, "stop_button")
        assert isinstance(window.stop_button, tk.Button)
        assert window.stop_button["text"] == "⏹ 停止"
        assert window.stop_button["state"] == "disabled"

    def test_stop_button_enabled_when_task_running(self) -> None:
        window = MainWindow()
        window.task_input.insert(0, "Test Task")
        window._on_start_click()

        assert window.stop_button["state"] == "normal"
