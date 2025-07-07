import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main_window import MainWindow


def main():
    window = MainWindow()
    window.run()


if __name__ == "__main__":
    main()