from datetime import datetime
import pytest

from src.models.session import Session


class TestSession:
    def test_session_initialization(self) -> None:
        session = Session("Test Task")

        assert session.task_name == "Test Task"
        assert session.is_running is False
        assert session.start_time is None
        assert session.end_time is None
        assert session.paused_time == 0

    def test_session_start(self) -> None:
        session = Session("Test Task")
        start_time = datetime.now()
        session.start()

        assert session.is_running is True
        assert session.start_time is not None
        assert session.start_time >= start_time
        assert session.end_time is None

    def test_session_stop(self) -> None:
        session = Session("Test Task")
        session.start()
        start_time = session.start_time
        session.stop()

        assert session.is_running is False
        assert session.end_time is not None
        assert session.start_time == start_time
        assert session.start_time is not None
        assert session.end_time >= session.start_time

    def test_session_duration_calculation(self) -> None:
        session = Session("Test Task")
        session.start()
        session.stop()

        duration = session.get_duration()
        assert duration >= 0

    def test_session_cannot_start_twice(self) -> None:
        session = Session("Test Task")
        session.start()

        with pytest.raises(AssertionError, match="Session is already running"):
            session.start()

    def test_session_cannot_stop_without_start(self) -> None:
        session = Session("Test Task")

        with pytest.raises(AssertionError, match="Session is not running"):
            session.stop()

    def test_session_task_name_cannot_be_empty(self) -> None:
        with pytest.raises(AssertionError, match="Task name cannot be empty"):
            Session("")

        with pytest.raises(AssertionError, match="Task name cannot be empty"):
            Session("   ")

    def test_session_pause(self) -> None:
        session = Session("Test Task")
        session.start()
        session.pause()

        assert session.is_paused is True
        assert session.pause_start_time is not None

    def test_session_resume(self) -> None:
        session = Session("Test Task")
        session.start()
        session.pause()
        session.resume()

        assert session.is_paused is False
        assert session.pause_start_time is None
        assert session.paused_time > 0

    def test_cannot_pause_without_start(self) -> None:
        session = Session("Test Task")

        with pytest.raises(AssertionError, match="Session is not running"):
            session.pause()

    def test_cannot_pause_when_already_paused(self) -> None:
        session = Session("Test Task")
        session.start()
        session.pause()

        with pytest.raises(AssertionError, match="Session is already paused"):
            session.pause()

    def test_cannot_resume_when_not_paused(self) -> None:
        session = Session("Test Task")
        session.start()

        with pytest.raises(AssertionError, match="Session is not paused"):
            session.resume()

    def test_paused_time_not_counted_in_duration(self) -> None:
        import time

        session = Session("Test Task")
        session.start()
        time.sleep(0.1)
        session.pause()
        time.sleep(0.1)
        session.resume()
        time.sleep(0.1)
        session.stop()

        duration = session.get_duration()
        assert 0.15 < duration < 0.25
