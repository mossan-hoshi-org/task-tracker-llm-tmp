from datetime import datetime, timedelta

from src.models.session import Session
from src.utils.markdown import format_sessions_to_markdown


class TestMarkdown:
    def test_format_single_session(self) -> None:
        session = Session("Test Task")
        session.start_time = datetime(2024, 1, 1, 10, 0, 0)
        session.end_time = datetime(2024, 1, 1, 10, 30, 0)
        session.is_running = False

        markdown = format_sessions_to_markdown([session])

        assert "# Task Summary" in markdown
        assert "Test Task" in markdown
        assert "00:30:00" in markdown

    def test_format_multiple_sessions(self) -> None:
        sessions = []
        for i in range(3):
            session = Session(f"Task {i+1}")
            session.start_time = datetime(2024, 1, 1, 10, 0, 0) + timedelta(hours=i)
            session.end_time = session.start_time + timedelta(minutes=30)
            session.is_running = False
            sessions.append(session)

        markdown = format_sessions_to_markdown(sessions)

        assert "# Task Summary" in markdown
        for i in range(3):
            assert f"Task {i+1}" in markdown
        assert markdown.count("00:30:00") == 3

    def test_format_includes_total_time(self) -> None:
        sessions = []
        for i in range(2):
            session = Session(f"Task {i+1}")
            session.start_time = datetime(2024, 1, 1, 10, 0, 0)
            session.end_time = session.start_time + timedelta(hours=1)
            session.is_running = False
            sessions.append(session)

        markdown = format_sessions_to_markdown(sessions)

        assert "Total Time: 02:00:00" in markdown

    def test_format_empty_sessions(self) -> None:
        markdown = format_sessions_to_markdown([])

        assert "# Task Summary" in markdown
        assert "No tasks recorded." in markdown
