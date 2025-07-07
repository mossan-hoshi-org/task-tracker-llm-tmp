from typing import List, Optional

from src.models.session import Session


class TaskTracker:
    def __init__(self) -> None:
        self.current_session: Optional[Session] = None
        self.sessions: List[Session] = []

    def start_task(self, task_name: str) -> None:
        assert task_name.strip(), "Task name cannot be empty"

        if self.current_session is not None:
            assert self.current_session.is_running, "Current session must be running"
            self.current_session.stop()

        new_session = Session(task_name)
        new_session.start()
        self.current_session = new_session
        self.sessions.append(new_session)

        assert self.current_session.is_running, "New session must be running"
        assert self.current_session.task_name == task_name, "Task name must match"

    def stop_all(self) -> None:
        assert self.current_session is not None, "No active session to stop"
        assert self.current_session.is_running, "Current session must be running"

        self.current_session.stop()
        self.current_session = None

        assert all(not session.is_running for session in self.sessions), "All sessions must be stopped"

    def get_all_sessions(self) -> List[Session]:
        return self.sessions.copy()
