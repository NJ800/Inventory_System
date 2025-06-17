from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
import hashlib

class LoginDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Operator Login")
        self.setFixedSize(300, 150)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        user_label = QLabel("Username:")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")

        pass_label = QLabel("Password:")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Enter your password")

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.authenticate)

        layout.addWidget(user_label)
        layout.addWidget(self.username)
        layout.addWidget(pass_label)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def authenticate(self):
        username = self.username.text().strip()
        password = self.password.text()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor = self.db_manager.get_connection().cursor()
        cursor.execute(
            'SELECT * FROM Operators WHERE username = ? AND password = ?',
            (username, hashed_password)
        )
        if cursor.fetchone():
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            self.password.clear()
            self.username.setFocus()
