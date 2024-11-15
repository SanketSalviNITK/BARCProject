from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QPushButton, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices  # Import QDesktopServices to open links
from database_window import IPHWRDatabase  # Assuming this is your reactor page
from cadet import Prediction  # Assuming Prediction class is defined in cadet module
from footer_util import add_company_footer  # Import your footer utility
import random  # Import random to select random address


class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username  # Store the username
        self.setWindowTitle("Main Application")
        self.setGeometry(500, 500, 1200, 800)  # Set a larger window size for better layout handling
        self.showMaximized()
        self.setStyleSheet(""" 
            QWidget {
                background: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #a0c4ff,  
                    stop: 1 #f8f9fa
                );
            }
        """)

        # Initialize the main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)  # Center the main layout

        # Create the top bar layout for username
        self.create_top_bar()

        # Add vertical spacers to center the button section vertically
        self.main_layout.addSpacerItem(QSpacerItem(20, 600, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create the middle bar for buttons
        self.create_middle_bar()

        # Add another spacer after buttons to keep them in the middle
        self.main_layout.addSpacerItem(QSpacerItem(20, 600, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add Help and Logout buttons at the bottom-right
        self.create_help_and_logout_buttons()

        # Add footer at the bottom using utility function
        add_company_footer(self.main_layout)

        # Set the main layout to the window
        self.setLayout(self.main_layout)

        # Track the visibility of submenus
        self.submenu_visibility = {
            "Prediction Models": False,
            "Codal Evaluation": False,
            "ISI Data Processing": False
        }

    def create_top_bar(self):
        # Top bar layout for username
        top_bar_layout = QHBoxLayout()

        # Display the logged-in username on the right
        self.username_label = QLabel(f"Logged in as: {self.username}")
        self.username_label.setAlignment(Qt.AlignRight)
        self.username_label.setStyleSheet("font-size: 22px; color: #34495e; padding: 20px;")
        top_bar_layout.addWidget(self.username_label, alignment=Qt.AlignRight)

        # Add the top bar layout to the main layout
        self.main_layout.addLayout(top_bar_layout)

    def create_middle_bar(self):
        # Middle bar layout for buttons
        middle_bar_layout = QHBoxLayout()
        middle_bar_layout.setAlignment(Qt.AlignCenter)

        # Create buttons and their corresponding sub-menus
        self.create_buttons()

        # Add the button layout to the middle bar
        middle_bar_layout.addLayout(self.button_layout)

        # Add the middle bar layout to the main layout
        self.main_layout.addLayout(middle_bar_layout)

    def create_buttons(self):
        # Main menu buttons and their corresponding sub-menus
        button_labels = ["Prediction Models", "Codal Evaluation", "ISI Data Processing", "Database"]
        sub_menus = {
            "Prediction Models": ["CADET", "HYCON", "SPDP"],
            "Codal Evaluation": ["Flaw assessment", "Material property evaluator"],
            "ISI Data Processing": ["PRESAM 220", "PRESAM 540", "CT-PIU GAP"],
            "Database": []  # No submenu for Database, but you can add items if needed
        }

        # Main layout for buttons (Horizontal alignment)
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)

        button_style = """
            QPushButton {
                background-color: white;  
                color: #2980b9;  
                border: 3px solid #2980b9;
                border-radius: 10px;
                font-size: 18px;  /* Adjusted font size */
                font-weight: bold;
                padding: 20px;
                margin: 15px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
            }
        """

        # Dictionary to store buttons and their submenus
        self.buttons_and_submenus = {}

        # Create main buttons and submenus
        for label in button_labels:
            # Create the main button
            button = QPushButton(label)
            button.setStyleSheet(button_style)
            button.setFixedSize(300, 120)
            button.clicked.connect(self.button_clicked)

            # Add the button to the button layout
            self.button_layout.addWidget(button, alignment=Qt.AlignCenter)

            # Create submenu layout (initially hidden)
            submenu_layout = QVBoxLayout()
            if sub_menus[label]:
                for submenu_item in sub_menus[label]:
                    submenu_button = QPushButton(submenu_item)
                    submenu_button.setStyleSheet(button_style.replace("font-size: 20px;", "font-size: 16px;"))  # Adjusted font size
                    submenu_button.setFixedSize(250, 60)
                    submenu_button.clicked.connect(self.submenu_clicked)
                    submenu_layout.addWidget(submenu_button)

            submenu_frame = QFrame()
            submenu_frame.setLayout(submenu_layout)
            submenu_frame.setVisible(False)  # Initially hidden
            self.buttons_and_submenus[button] = (submenu_frame, button)  # Store both frame and button

    def create_help_and_logout_buttons(self):
        # Add a horizontal layout for Help and Logout buttons at the bottom-right
        help_logout_layout = QHBoxLayout()

        button_style = """
            QPushButton {
                background-color: white;  
                color: #e74c3c;  
                border: 3px solid #e74c3c;
                border-radius: 10px;
                font-size: 20px;  /* Adjusted font size */
                font-weight: bold;
                padding: 15px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
            }
        """

        # Spacer to push buttons to the right
        help_logout_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Help Button
        help_button = QPushButton("Help")
        help_button.setStyleSheet(button_style.replace("#e74c3c", "#2ecc71"))
        help_button.setFixedSize(150, 80)
        help_button.clicked.connect(self.help_clicked)
        help_logout_layout.addWidget(help_button, alignment=Qt.AlignRight)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet(button_style)
        logout_button.setFixedSize(150, 80)
        logout_button.clicked.connect(self.logout)
        help_logout_layout.addWidget(logout_button, alignment=Qt.AlignRight)

        # Add to main layout at the bottom
        self.main_layout.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.main_layout.addLayout(help_logout_layout)

    def button_clicked(self):
        button = self.sender()
        submenu_frame, original_button = self.buttons_and_submenus[button]

        # Check if the Database button was clicked
        if button.text() == "Database":
            self.open_ipwh_database_window()
            return  # Exit early, as we don't want to toggle a submenu

        # Hide all other submenus and reset their buttons
        for frame, btn in self.buttons_and_submenus.values():
            if frame != submenu_frame:
                frame.setVisible(False)
                btn.show()  # Show the original button again

        # Toggle visibility of the clicked button's submenu
        if submenu_frame.isVisible():
            submenu_frame.setVisible(False)
            button.show()  # Show the original button again
        else:
            submenu_frame.setVisible(True)
            self.button_layout.insertWidget(self.button_layout.indexOf(button) + 1, submenu_frame)

    def submenu_clicked(self):
        submenu_button = self.sender()
        submenu_text = submenu_button.text()

        if submenu_text == "CADET":
            # Open the Prediction class when the CADET button is clicked
            self.open_prediction_window()
        else:
            print(f"{submenu_text} clicked.")

    def open_prediction_window(self):
        # Create and display the Prediction window
        self.prediction_window = Prediction()  # Assuming Prediction is a QWidget or has a method to show itself
        self.prediction_window.show()

    def open_ipwh_database_window(self):
        # Create and display the IPHWR Channel Health Analysis window
        self.database_window = IPHWRDatabase(self.username)
        self.database_window.show()

    def logout(self):
        from login_window import LoginWindow  # Import LoginWindow inside the method
        self.username = ""
        self.close()
        print("Logout successful")
        self.login_window = LoginWindow()  # Show the login window again
        
        

    def help_clicked(self):
        # Company information
        company_name = "SVR Robotics Pvt. Ltd."
        address = "SVR InfoTech, 3rd Floor, Amber Plaza, Nr Bank of, Sinhgad Institute Rd, Ambegaon Budruk, Pune, Maharashtra 411046"
        contact_number = "+91-9876543210"

        # URL for Google Maps (you can customize the URL if you want a specific location)
        map_url = "https://maps.app.goo.gl/QJHZDC1T3LPWHtCY7"

        # Create a custom dialog for help
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Company Information")
        help_dialog.setGeometry(300, 300, 400, 300)  # Set size of the dialog
        help_dialog.setStyleSheet("font-size: 16px;")  # Set font size

        dialog_layout = QVBoxLayout(help_dialog)

        # Add labels with company info
        dialog_layout.addWidget(QLabel(f"<b>Company:</b> {company_name}"), alignment=Qt.AlignTop)
        dialog_layout.addWidget(QLabel(f"<b>Address:</b> {address}"), alignment=Qt.AlignTop)
        dialog_layout.addWidget(QLabel(f"<b>Contact Number:</b> {contact_number}"), alignment=Qt.AlignTop)

        # Create a button for the map link
        map_button = QPushButton("View on Map")
        map_button.setStyleSheet("color: #2980b9; font-weight: bold; text-decoration: underline;")
        map_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(map_url)))  # Open the link in a browser

        dialog_layout.addWidget(map_button, alignment=Qt.AlignTop)
        
        # Add OK button to close the dialog
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(help_dialog.accept)
        dialog_layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        help_dialog.setLayout(dialog_layout)
        help_dialog.exec_()  # Show the dialog as modal
