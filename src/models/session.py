from datetime import datetime
from typing import Optional


class Session:
    def __init__(self, task_name: str) -> None:
        assert task_name.strip(), "Task name cannot be empty"
        self.task_name = task_name
        self.is_running = False
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.paused_time = 0

    def start(self) -> None:
        assert not self.is_running, "Session is already running"
        self.is_running = True
        self.start_time = datetime.now()

    def stop(self) -> None:
        assert self.is_running, "Session is not running"
        assert self.start_time is not None, "Start time must be set"
        self.is_running = False
        self.end_time = datetime.now()

    def get_duration(self) -> float:
        assert self.start_time is not None, "Session has not been started"

        if self.end_time is None:
            end = datetime.now()
        else:
            end = self.end_time

        duration = (end - self.start_time).total_seconds() - self.paused_time
        assert duration >= 0, "Duration cannot be negative"

        return duration
