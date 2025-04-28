import sys

from PySide6.QtWidgets import QApplication

from utils.assets_path import resource_path
from views.main_window import MainWindow


def load_stylesheet(file_path: str) -> str:
    path = resource_path(file_path)
    with open(path, "r") as file:
        return file.read()


def center_window(window) -> None:
    """Centers the window on the screen."""
    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    screen_center = screen_geometry.center()
    window_geometry = window.frameGeometry()
    window_geometry.moveCenter(screen_center)
    window.move(window_geometry.topLeft())


def main():
    app = QApplication()
    app.setStyleSheet(load_stylesheet("assets/style.qss"))
    window = MainWindow()
    center_window(window)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
