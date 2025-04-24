from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox, \
    QPushButton


class SettingsDialog(QDialog):
    def __init__(self, saved_data: tuple, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurações")
        self.setFixedSize(QSize(400, 400))

        self.sheet_id_field = QLineEdit(saved_data[0])
        self.credentials_field = QTextEdit(saved_data[1])

        self.buttons = QDialogButtonBox()
        self.save_button = QPushButton("Salvar")
        self.cancel_button = QPushButton("Cancelar")
        self.buttons.addButton(self.save_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttons.addButton(self.cancel_button, QDialogButtonBox.ButtonRole.RejectRole)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self._setup_layout()

    def get_values(self) -> tuple[str, str]:
        return self.sheet_id_field.text(), self.credentials_field.toPlainText()

    def _setup_layout(self) -> None:
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(QLabel("ID da Planilha:"))
        v_layout.addWidget(self.sheet_id_field)
        v_layout.addWidget(QLabel("Credenciais:"))
        v_layout.addWidget(self.credentials_field)
        v_layout.addWidget(self.buttons)
