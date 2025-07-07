import tkinter as tk
from tkinter import messagebox
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.session import Session


class SummaryScreen:
    def __init__(self, sessions: List["Session"]) -> None:
        self.sessions = sessions
        self.root = tk.Toplevel()
        self.root.title("Task Summary")
        self.root.minsize(600, 400)

        self._create_widgets()
        self._display_summary()

    def _create_widgets(self) -> None:
        # Summary text area with scrollbar
        text_frame = tk.Frame(self.root, padx=10, pady=10)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.summary_text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.summary_text.yview)

        # Button frame
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.copy_button = tk.Button(button_frame, text="Copy Markdown", command=self._on_copy_click)
        self.copy_button.pack(side=tk.LEFT)

        self.close_button = tk.Button(button_frame, text="閉じる", command=self.root.destroy)
        self.close_button.pack(side=tk.RIGHT)

    def _display_summary(self) -> None:
        from src.utils.markdown import format_sessions_to_markdown

        markdown_text = format_sessions_to_markdown(self.sessions)
        self.summary_text.insert(tk.END, markdown_text)
        self.summary_text.config(state="disabled")

    def _on_copy_click(self) -> None:
        from src.utils.clipboard import copy_to_clipboard

        markdown_text = self.summary_text.get("1.0", tk.END).strip()
        copy_to_clipboard(markdown_text)
        messagebox.showinfo("コピー完了", "Markdownをクリップボードにコピーしました。")
