from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QIntValidator, QAction
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QProgressBar, \
    QGridLayout, QMenu

from utils.assets_path import resource_path


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RRC Tool - ASSTEC")
        self.setFixedSize(QSize(400, 400))

        # Components
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap(resource_path("assets/logo.png")))
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(QSize(300, 200))

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)

        self.asstec_search_bar = QLineEdit()
        self.asstec_search_bar.setValidator(QIntValidator())
        self.asstec_search_bar.setPlaceholderText("Nº da ASSTEC")

        self.status_label = QLabel("Placeholder...")
        self.status_label.setObjectName("status_label")

        self.generate_document_button = QPushButton(QIcon(resource_path("assets/icons/document-add.svg")), " Gerar RRC")
        self.generate_document_button.setIconSize(QSize(30, 30))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self._setup_layout()

    def _show_context_menu(self, pos):
        menu = QMenu(self)

        settings_option = QAction(QIcon(resource_path("assets/icons/settings.svg")), "Configurações", self)
        exit_option = QAction(QIcon(resource_path("assets/icons/exit.svg")), "Sair", self)

        menu.addAction(settings_option)
        menu.addSeparator()
        menu.addAction(exit_option)

        action = menu.exec(self.mapToGlobal(pos))

        if action == settings_option:
            print("SETTINGS")
        elif action == exit_option:
            self.close()

    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        progress_widget = QWidget()
        progress_widget.setFixedHeight(10)
        progress_widget_layout = QVBoxLayout(progress_widget)
        progress_widget_layout.addWidget(self.progress_bar)
        progress_widget_layout.setContentsMargins(0, 0, 0, 0)

        g_layout = QGridLayout()
        g_layout.addWidget(self.asstec_search_bar, 0, 0, 1, 4)
        g_layout.addWidget(progress_widget, 1, 0, 1, 4)
        g_layout.addWidget(self.generate_document_button, 2, 1, 1, 2)
        g_layout.addWidget(self.status_label, 3, 0, 1, 4)

        main_layout.addWidget(self.logo)
        main_layout.addSpacing(10)
        main_layout.addLayout(g_layout)
