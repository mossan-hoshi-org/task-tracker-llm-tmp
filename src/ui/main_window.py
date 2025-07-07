import tkinter as tk


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Task Tracker")
        self.root.minsize(600, 400)

    def run(self) -> None:
        self.root.mainloop()
