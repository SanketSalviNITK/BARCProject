from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from database_window import IPHWRDatabase

class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username  # Store the username
        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        box_widget = QWidget()
        box_layout = QVBoxLayout()

        # Display the logged-in username
        self.username_label = QLabel(f"Logged in as: {username}")
        box_layout.addWidget(self.username_label, alignment=Qt.AlignRight)

        # Create buttons
        self.create_buttons(box_layout)

        box_widget.setLayout(box_layout)
        layout.addWidget(box_widget, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def create_buttons(self, layout):
        button_labels = ["Database", "Analysis", "Training Manual", "Documentation", "Help", "Logout"]
        grid_layout = QGridLayout()

        # Create buttons and add them to the grid layout
        for i, label in enumerate(button_labels):
            button = QPushButton(label)
            button.clicked.connect(self.button_clicked)
            grid_layout.addWidget(button, i // 2, i % 2)  # 2 columns

        layout.addLayout(grid_layout)

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Database":
            self.open_ipwh_database_window()
            self.close()
        elif button.text() == "Logout":
            self.logout()

    def open_ipwh_database_window(self):
        # Create and display the IPHWR Channel Health Analysis window
        self.database_window = IPHWRDatabase(self.username)
        self.database_window.show()

    def logout(self):
        # Delayed import to avoid circular dependency
        from login_window import LoginWindow  # Import LoginWindow inside the method

        # Set username to an empty string (or any action to reset user state)
        self.username = ""

        # Close the current window (MainWindow)
        self.close()
        print("Logout successful")
        # Show the login window again
        self.login_window = LoginWindow()
        self.login_window.show()
