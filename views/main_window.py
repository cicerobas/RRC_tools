from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtGui import QIcon, QPixmap, QIntValidator, QAction
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QProgressBar, \
    QGridLayout, QMenu, QMessageBox, QFileDialog
from pandas import DataFrame

from services.gsheets_service import GSheetsService
from utils.assets_path import resource_path
from utils.constants import SHEET_ID_KEY, CREDENTIALS_KEY
from utils.pdf_document_utils import generate_pdf, handle_asstec_data
from views.settings_dialog import SettingsDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RRC Tool - ASSTEC")
        self.setFixedSize(QSize(400, 400))

        self.settings = QSettings("CEBRA", "RRC_Tool")
        self.access_data = self._load_access_data()
        self.gsheets_service = GSheetsService(self.access_data) if self._has_valid_access_data() else None

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

        self.generate_document_button = QPushButton(QIcon(resource_path("assets/icons/document-add.svg")), " Gerar RRC")
        self.generate_document_button.setIconSize(QSize(30, 30))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self.generate_document_button.clicked.connect(self._generate_document)

        self._setup_layout()

    def _generate_document(self) -> None:
        asstec_number = self.asstec_search_bar.text()
        if len(asstec_number) < 5:
            return

        self._toggle_loading_ui()
        row = self.gsheets_service.find_asstec_row(asstec_number)
        if row >= 0:
            asstec_data = self.gsheets_service.validate_asstec_required_data(row)
            if isinstance(asstec_data, str):
                QMessageBox.warning(self, "Atenção", asstec_data)
            else:
                items_data = self.gsheets_service.get_items_data(asstec_number)
                if isinstance(items_data, DataFrame):
                    save_path = QFileDialog.getExistingDirectory(self, "Select a Directory", )
                    if save_path:
                        document_data = {"CLIENTE": asstec_data[2], "GRUPO": asstec_data[3], "ASSTEC": asstec_data[1],
                                         "NFE": asstec_data[4],
                                         "RESPONSAVEL": asstec_data[8]}
                        formated_data = handle_asstec_data(document_data, items_data)
                        response = generate_pdf(formated_data, save_path)
                        QMessageBox.information(self, "Concluído", f"Arquivo salvo em:\n{response}")
                        self.asstec_search_bar.setText("")
                else:
                    QMessageBox.warning(self, "Atenção", f"Asstec Nº: {asstec_number}\nSem itens registrados!")
        else:
            QMessageBox.critical(self, "Atenção", f"Asstec Nº: {asstec_number}\nNão encontrada!")

        self._toggle_loading_ui()

    def _show_context_menu(self, pos) -> None:
        menu = QMenu(self)

        settings_option = QAction(QIcon(resource_path("assets/icons/settings.svg")), "Configurações", self)
        exit_option = QAction(QIcon(resource_path("assets/icons/exit.svg")), "Sair", self)

        menu.addAction(settings_option)
        menu.addSeparator()
        menu.addAction(exit_option)
        action = menu.exec(self.mapToGlobal(pos))

        if action == settings_option:
            self._show_settings_dialog()
        elif action == exit_option:
            self.close()

    def _show_settings_dialog(self) -> None:
        dialog = SettingsDialog(self.access_data, self)
        if dialog.exec():
            values = dialog.get_values()
            self.settings.setValue(SHEET_ID_KEY, values[0])
            self.settings.setValue(CREDENTIALS_KEY, values[1])
            self.close()

    def _load_access_data(self) -> tuple:
        """Load access data from settings."""
        return (
            self.settings.value(SHEET_ID_KEY, ""),
            self.settings.value(CREDENTIALS_KEY, "")
        )

    def _has_valid_access_data(self) -> bool:
        """Check if access data contains valid (non-empty) values."""
        return all(self.access_data)

    def _toggle_loading_ui(self) -> None:
        if self.generate_document_button.isEnabled():
            self.generate_document_button.setEnabled(False)
        else:
            self.generate_document_button.setEnabled(True)

        if self.progress_bar.isVisible():
            self.progress_bar.setVisible(False)
        else:
            self.progress_bar.setVisible(True)

    def _setup_layout(self) -> None:
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

        main_layout.addWidget(self.logo)
        main_layout.addSpacing(20)
        main_layout.addLayout(g_layout)
