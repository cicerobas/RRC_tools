from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RRC Tool")
        self.setFixedSize(QSize(400,400))