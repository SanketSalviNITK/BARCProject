from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Login Screen")
        self.setGeometry(100, 100, 600, 400)
        #self.setStyleSheet("background-color: #f4f6f9;")  # Light grey background for a modern look
    
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #a0c4ff,  /* Soft blue */
                    stop: 1 #f8f9fa   /* Very light grey, almost white */
                );
            }
        """)

        # Create the title label with bold text
        self.label = QLabel("Login")
        font = QFont("Arial", 20, QFont.Bold)  # Set font to Arial, size 20, bold
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #2c3e50;")  # Dark grey color for the title

        # Create labels and input fields for username and password with styles
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("font-size: 14px; color: #34495e;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px;
                background-color: #ecf0f1;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: #ffffff;
            }
        """)

        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("font-size: 14px; color: #34495e;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px;
                background-color: #ecf0f1;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: #ffffff;
            }
        """)

        # Create the login button with styling and hover effects
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.login_button.clicked.connect(self.check_login)

        # Connect Enter key to login
        self.username_input.returnPressed.connect(self.check_login)
        self.password_input.returnPressed.connect(self.check_login)

        # Layout setup for form elements
        form_layout = QGridLayout()
        form_layout.addWidget(self.label, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.username_label, 1, 0, alignment=Qt.AlignRight)
        form_layout.addWidget(self.username_input, 1, 1)
        form_layout.addWidget(self.password_label, 2, 0, alignment=Qt.AlignRight)
        form_layout.addWidget(self.password_input, 2, 1)
        form_layout.addWidget(self.login_button, 3, 1, alignment=Qt.AlignRight)

        # Wrap the form in a widget with fixed size and margins for better alignment
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setFixedSize(600, 200)

        # Create the company label and set its alignment to the left
        self.company_label = QLabel("Developed by SVR Infotech")
        self.company_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        self.company_label.setAlignment(Qt.AlignLeft)

        # Center the form widget in the window using a VBox layout
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)

        # Footer layout for the company label
        footer_layout = QHBoxLayout()
        footer_layout.addWidget(self.company_label)
        footer_layout.addStretch(1)  # Push the company name to the left

        # Add the footer layout to the main layout
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    def check_login(self):
        # List of valid username-password pairs (as per the names you've provided)
        valid_credentials = [
            ("bhavika", "bhavika"),
            ("ankita", "ankita"),
            ("pooja", "pooja"),
            ("vinod", "vinod"),
            ("rahul", "rahul")
        ]

        # Get entered username and password
        username = self.username_input.text()
        password = self.password_input.text()

        # Check if entered credentials match any valid pair
        if (username, password) in valid_credentials:
            print("Login successful")
            self.open_main_window(username)  # Open the main application window
            self.close()  # Close the login window
        else:
            print("Invalid username or password")

    def open_main_window(self, username):
        # Create and display the main window with the username
        self.main_window = MainWindow(username)
        self.main_window.show()

