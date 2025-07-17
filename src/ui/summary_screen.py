import tkinter as tk
from tkinter import messagebox, ttk
import os
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
        self._categorize_tasks()

    def _create_widgets(self) -> None:
        # Summary text area with scrollbar
        text_frame = tk.Frame(self.root, padx=10, pady=10)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.summary_text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=10)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.summary_text.yview)

        # Category table
        category_frame = tk.LabelFrame(self.root, text="カテゴリ別集計", padx=10, pady=10)
        category_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create Treeview for category table
        columns = ("tasks", "time")
        self.category_tree = ttk.Treeview(category_frame, columns=columns, show="tree headings", height=8)

        # Define headings
        self.category_tree.heading("#0", text="カテゴリ")
        self.category_tree.heading("tasks", text="タスク")
        self.category_tree.heading("time", text="合計時間")

        # Configure column widths
        self.category_tree.column("#0", width=150)
        self.category_tree.column("tasks", width=300)
        self.category_tree.column("time", width=100)

        # Add scrollbar for tree
        tree_scrollbar = ttk.Scrollbar(category_frame, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.category_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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

        # Add category summary to markdown
        markdown_text += "\n\n## カテゴリ別集計\n\n"

        for item in self.category_tree.get_children():
            category = self.category_tree.item(item)
            category_name = category["text"]
            values = category["values"]

            markdown_text += f"### {category_name}\n"
            markdown_text += f"- {values[0]}\n"
            markdown_text += f"- 合計時間: {values[1]}\n\n"

            # Add task details
            for child in self.category_tree.get_children(item):
                task = self.category_tree.item(child)
                task_values = task["values"]
                markdown_text += f"  - {task_values[0]}: {task_values[1]}\n"

            markdown_text += "\n"

        copy_to_clipboard(markdown_text)
        messagebox.showinfo("コピー完了", "Markdownをクリップボードにコピーしました。")

    def _categorize_tasks(self) -> None:
        if not self.sessions:
            return

        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.category_tree.insert("", "end", text="エラー", values=("APIキーが設定されていません", ""))
            return

        try:
            from src.services.gemini_client import GeminiClient
            from src.services.category_aggregator import CategoryAggregator

            # Get unique task names
            task_names = list(set(session.task_name for session in self.sessions))

            # Categorize tasks
            client = GeminiClient(api_key=api_key)
            categories = client.categorize_tasks(task_names)

            # Aggregate by category
            aggregator = CategoryAggregator()
            aggregated_data = aggregator.aggregate(self.sessions, categories)

            # Display in tree
            for category in aggregated_data:
                # Insert category
                category_item = self.category_tree.insert(
                    "",
                    "end",
                    text=category["name"],
                    values=(f"{len(category['tasks'])}個のタスク", category["total_time"]),
                )

                # Insert tasks under category
                for task in category["tasks"]:
                    self.category_tree.insert(category_item, "end", text="", values=(task["name"], task["total_time"]))

                # Expand category by default
                self.category_tree.item(category_item, open=True)

        except Exception as e:
            self.category_tree.insert("", "end", text="エラー", values=(str(e), ""))
