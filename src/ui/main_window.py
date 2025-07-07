import tkinter as tk
from typing import Any


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Task Tracker")
        self.root.minsize(600, 400)

        self._create_widgets()
        self._setup_bindings()

    def _create_widgets(self) -> None:
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(side=tk.TOP, fill=tk.X)

        self.task_input = tk.Entry(input_frame, width=40)
        self.task_input.pack(side=tk.LEFT, padx=(0, 10))

        self.start_button = tk.Button(input_frame, text="▶ 計測開始", state="disabled")
        self.start_button.pack(side=tk.LEFT)

    def _setup_bindings(self) -> None:
        self.task_input.bind("<KeyRelease>", self._on_input_change)

    def _on_input_change(self, event: Any) -> None:
        if self.task_input.get().strip():
            self.start_button.config(state="normal")
        else:
            self.start_button.config(state="disabled")

    def run(self) -> None:
        self.root.mainloop()
