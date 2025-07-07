import tkinter as tk
from typing import Any

from src.models.task_tracker import TaskTracker
from src.ui.summary_screen import SummaryScreen


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Task Tracker")
        self.root.minsize(600, 400)

        self.task_tracker = TaskTracker()

        self._create_widgets()
        self._setup_bindings()
        self._update_task_list()

    def _create_widgets(self) -> None:
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(side=tk.TOP, fill=tk.X)

        self.task_input = tk.Entry(input_frame, width=40)
        self.task_input.pack(side=tk.LEFT, padx=(0, 10))

        self.start_button = tk.Button(input_frame, text="▶ 計測開始", state="disabled", command=self._on_start_click)
        self.start_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(input_frame, text="⏸ 一時停止", state="disabled", command=self._on_pause_click)
        self.pause_button.pack(side=tk.LEFT, padx=(5, 0))

        self.stop_button = tk.Button(input_frame, text="⏹ 停止", state="disabled", command=self._on_stop_click)
        self.stop_button.pack(side=tk.LEFT, padx=(5, 0))

        # Task list with scrollbar
        list_frame = tk.Frame(self.root, padx=10, pady=5)
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_list.yview)

    def _setup_bindings(self) -> None:
        self.task_input.bind("<KeyRelease>", self._on_input_change)
        self.task_input.bind(
            "<Return>", lambda e: self._on_start_click() if self.start_button["state"] == "normal" else None
        )

    def _on_input_change(self, event: Any) -> None:
        if self.task_input.get().strip():
            self.start_button.config(state="normal")
        else:
            self.start_button.config(state="disabled")

    def _on_start_click(self) -> None:
        task_name = self.task_input.get().strip()
        if task_name:
            self.task_tracker.start_task(task_name)
            self.task_input.delete(0, tk.END)
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.stop_button.config(state="normal")
            self._update_task_list()

    def _on_pause_click(self) -> None:
        if self.task_tracker.current_session and self.task_tracker.current_session.is_paused:
            self.task_tracker.resume_current()
            self.pause_button.config(text="⏸ 一時停止")
        else:
            self.task_tracker.pause_current()
            self.pause_button.config(text="▶ 再開")

    def _on_stop_click(self) -> None:
        if self.task_tracker.current_session:
            self.task_tracker.stop_all()
            self.pause_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            self._update_task_list()

            # Show summary screen
            sessions = self.task_tracker.get_all_sessions()
            if sessions:
                SummaryScreen(sessions)

    def _update_task_list(self) -> None:
        self.task_list.delete(0, tk.END)

        sessions = self.task_tracker.get_all_sessions()
        for i, session in enumerate(sessions):
            duration = session.get_duration()
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            status = ""
            if session.is_running:
                if session.is_paused:
                    status = " ⏸"
                else:
                    status = " ▶"

            task_str = f"{session.task_name} - {time_str}{status}"
            self.task_list.insert(tk.END, task_str)

        # Schedule next update if there's a running session
        if self.task_tracker.current_session and self.task_tracker.current_session.is_running:
            self.root.after(1000, self._update_task_list)

    def run(self) -> None:
        self.root.mainloop()
