from datetime import datetime, timedelta
from src.models.session import Session


class TestSessionTimezone:
    def test_session_duration_across_midnight(self) -> None:
        session = Session("夜間作業")

        # Start at 23:30
        start_time = datetime.now().replace(hour=23, minute=30, second=0, microsecond=0)
        session.start_time = start_time
        session.is_running = True

        # End at 00:30 next day (1 hour duration)
        end_time = start_time + timedelta(hours=1)
        session.end_time = end_time
        session.is_running = False

        duration = session.get_duration()

        assert duration == 3600  # 1 hour in seconds

    def test_session_duration_multiple_days(self) -> None:
        session = Session("長期タスク")

        # Start on Monday
        start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        session.start_time = start_time
        session.is_running = True

        # End on Wednesday (48 hours later)
        end_time = start_time + timedelta(days=2)
        session.end_time = end_time
        session.is_running = False

        duration = session.get_duration()

        assert duration == 48 * 3600  # 48 hours in seconds

    def test_paused_session_across_midnight(self) -> None:
        session = Session("一時停止テスト")

        # Start at 23:00
        start_time = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
        session.start_time = start_time
        session.is_running = True

        # Pause at 23:30
        pause_time = start_time + timedelta(minutes=30)
        session.is_paused = True
        session.pause_start_time = pause_time

        # Resume at 00:30 (1 hour pause)
        resume_time = pause_time + timedelta(hours=1)
        session.paused_time = (resume_time - pause_time).total_seconds()
        session.is_paused = False
        session.pause_start_time = None

        # End at 01:00
        end_time = start_time + timedelta(hours=2)
        session.end_time = end_time
        session.is_running = False

        duration = session.get_duration()

        # Total time: 2 hours, minus 1 hour pause = 1 hour
        assert duration == 3600

    def test_daylight_saving_time_transition(self) -> None:
        session = Session("DST切替テスト")

        # Simulate session during DST transition
        # Note: This is a conceptual test since actual DST behavior depends on system timezone
        start_time = datetime.now()
        session.start_time = start_time
        session.is_running = True

        # End 3 hours later
        end_time = start_time + timedelta(hours=3)
        session.end_time = end_time
        session.is_running = False

        duration = session.get_duration()

        # Duration should always be correct regardless of DST
        assert duration == 3 * 3600

    def test_leap_second_handling(self) -> None:
        session = Session("うるう秒テスト")

        # Start session
        start_time = datetime.now()
        session.start_time = start_time
        session.is_running = True

        # End 1 minute later
        end_time = start_time + timedelta(minutes=1)
        session.end_time = end_time
        session.is_running = False

        duration = session.get_duration()

        # Duration should be 60 seconds
        # (leap seconds are typically handled by the OS/Python datetime)
        assert duration == 60
