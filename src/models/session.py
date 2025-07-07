from datetime import datetime
from typing import Optional


class Session:
    def __init__(self, task_name: str) -> None:
        assert task_name.strip(), "Task name cannot be empty"
        self.task_name = task_name
        self.is_running = False
        self.is_paused = False
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.pause_start_time: Optional[datetime] = None
        self.paused_time: float = 0

    def start(self) -> None:
        assert not self.is_running, "Session is already running"
        self.is_running = True
        self.start_time = datetime.now()

    def stop(self) -> None:
        assert self.is_running, "Session is not running"
        assert self.start_time is not None, "Start time must be set"

        if self.is_paused:
            self.resume()

        self.is_running = False
        self.end_time = datetime.now()

    def pause(self) -> None:
        assert self.is_running, "Session is not running"
        assert not self.is_paused, "Session is already paused"

        self.is_paused = True
        self.pause_start_time = datetime.now()

    def resume(self) -> None:
        assert self.is_running, "Session is not running"
        assert self.is_paused, "Session is not paused"
        assert self.pause_start_time is not None, "Pause start time must be set"

        pause_duration = (datetime.now() - self.pause_start_time).total_seconds()
        self.paused_time += pause_duration
        self.is_paused = False
        self.pause_start_time = None

    def get_duration(self) -> float:
        assert self.start_time is not None, "Session has not been started"

        if self.end_time is None:
            end = datetime.now()
        else:
            end = self.end_time

        current_paused_time = self.paused_time
        if self.is_paused and self.pause_start_time is not None:
            current_paused_time += (datetime.now() - self.pause_start_time).total_seconds()

        duration = (end - self.start_time).total_seconds() - current_paused_time
        assert duration >= 0, "Duration cannot be negative"

        return duration
