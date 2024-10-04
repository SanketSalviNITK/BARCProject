from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from main_window import MainWindow
from PyQt5.QtGui import QFont


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Login Screen")
        self.setGeometry(100, 100, 600, 400)

        # First label that spans two columns and is center-aligned with bold text
        self.label = QLabel("Login Form")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        # Create labels and text fields for username and password
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        # Layout setup for form elements
        form_layout = QGridLayout()
        form_layout.addWidget(self.label, 0, 0, 1, 2, alignment=Qt.AlignCenter)  # Spanning across both columns
        form_layout.addWidget(self.username_label, 1, 0)
        form_layout.addWidget(self.username_input, 1, 1)
        form_layout.addWidget(self.password_label, 2, 0)
        form_layout.addWidget(self.password_input, 2, 1)
        form_layout.addWidget(self.login_button, 3, 1)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setFixedSize(300, 150)  # Set fixed size for the login box

        # Main layout to center the form in the window
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def check_login(self):
        # Check login credentials
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "a" and password == "a":
            print("Login successful")
            self.open_main_window(username)  # Open the main application window
            self.close()  # Close the login window
        else:
            print("Invalid username or password")

    def open_main_window(self, username):
        # Create and display the main window with the username
        self.main_window = MainWindow(username)
        self.main_window.show()
