import pytest

from src.models.task_tracker import TaskTracker


class TestTaskTracker:
    def test_task_tracker_initialization(self) -> None:
        tracker = TaskTracker()

        assert tracker.current_session is None
        assert tracker.sessions == []

    def test_start_first_task(self) -> None:
        tracker = TaskTracker()
        tracker.start_task("Task 1")

        assert tracker.current_session is not None
        assert tracker.current_session.task_name == "Task 1"
        assert tracker.current_session.is_running is True
        assert len(tracker.sessions) == 1

    def test_switch_to_second_task_stops_first(self) -> None:
        tracker = TaskTracker()
        tracker.start_task("Task 1")
        first_session = tracker.current_session

        tracker.start_task("Task 2")

        assert first_session is not None
        assert first_session.is_running is False
        assert first_session.end_time is not None
        assert tracker.current_session is not None
        assert tracker.current_session.task_name == "Task 2"
        assert tracker.current_session.is_running is True
        assert len(tracker.sessions) == 2

    def test_cannot_start_empty_task(self) -> None:
        tracker = TaskTracker()

        with pytest.raises(AssertionError, match="Task name cannot be empty"):
            tracker.start_task("")

    def test_stop_all_sessions(self) -> None:
        tracker = TaskTracker()
        tracker.start_task("Task 1")
        tracker.start_task("Task 2")

        tracker.stop_all()

        assert tracker.current_session is None
        assert all(not session.is_running for session in tracker.sessions)
        assert len(tracker.sessions) == 2

    def test_get_all_sessions(self) -> None:
        tracker = TaskTracker()
        tracker.start_task("Task 1")
        tracker.start_task("Task 2")

        sessions = tracker.get_all_sessions()

        assert len(sessions) == 2
        assert sessions[0].task_name == "Task 1"
        assert sessions[1].task_name == "Task 2"

    def test_cannot_stop_when_no_active_session(self) -> None:
        tracker = TaskTracker()

        with pytest.raises(AssertionError, match="No active session to stop"):
            tracker.stop_all()

    def test_session_ordering_preserved(self) -> None:
        tracker = TaskTracker()
        task_names = ["Task 1", "Task 2", "Task 3"]

        for name in task_names:
            tracker.start_task(name)

        sessions = tracker.get_all_sessions()
        assert [s.task_name for s in sessions] == task_names

    def test_pause_current_session(self) -> None:
        tracker = TaskTracker()
        tracker.start_task("Task 1")

        tracker.pause_current()

        assert tracker.current_session is not None
        assert tracker.current_session.is_paused is True

    def test_resume_current_session(self) -> None:
        tracker = TaskTracker()
        tracker.start_task("Task 1")
        tracker.pause_current()

        tracker.resume_current()

        assert tracker.current_session is not None
        assert tracker.current_session.is_paused is False

    def test_cannot_pause_when_no_session(self) -> None:
        tracker = TaskTracker()

        with pytest.raises(AssertionError, match="No active session to pause"):
            tracker.pause_current()

    def test_cannot_resume_when_no_session(self) -> None:
        tracker = TaskTracker()

        with pytest.raises(AssertionError, match="No active session to resume"):
            tracker.resume_current()
