from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt

from fetch_data_window import FetchWindow
from load_220_iphwr import load_220_iphwr
from load_540_iphwr import load_540_iphwr
from load_700_iphwr import load_700_iphwr

class IPHWRDatabase(QWidget):
    def __init__(self,username):
        super().__init__()

        # Set window title and size
        self.username=username
        self.setWindowTitle("IPHWR Channel Health Analysis System")
        self.setGeometry(100, 100, 800, 600)  # Adjusted size for better visibility

        # Main layout
        self.main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("IPHWR Channel Health Analysis System")
        title_label.setAlignment(Qt.AlignCenter)

        # Add title label to main layout
        self.main_layout.addWidget(title_label)

        # Create sub layouts
        self.sub_layout_1 = QVBoxLayout()  # 20% width
        self.sub_layout_2 = QVBoxLayout()  # 60% width
        self.sub_layout_3 = QVBoxLayout()  # 20% width

        # Set sub layouts' minimum widths
        sub_layout_1_widget = QWidget()
        sub_layout_2_widget = QWidget()
        sub_layout_3_widget = QWidget()

        sub_layout_1_widget.setMinimumWidth(160)  # 20% of 800
        sub_layout_2_widget.setMinimumWidth(480)  # 60% of 800
        sub_layout_3_widget.setMinimumWidth(160)  # 20% of 800

        # Set background colors for the sub layout widgets
        sub_layout_1_widget.setStyleSheet("background-color: #f0f0f0;")  # Light grey
        sub_layout_2_widget.setStyleSheet("background-color: #d0e0ff;")  # Light blue
        sub_layout_3_widget.setStyleSheet("background-color: #f0f0f0;")  # Light grey

        # Label for selected module (Database)
        selected_module_label = QLabel("Selected Module: Database")
        selected_module_label.setAlignment(Qt.AlignCenter)

        # Add the selected module label to the left sub layout
        self.sub_layout_1.addWidget(selected_module_label)

        # Centered label for Reactor Category
        reactor_category_label = QLabel("Reactor Category")
        reactor_category_label.setAlignment(Qt.AlignCenter)
        self.sub_layout_1.addWidget(reactor_category_label)

        # Buttons for Reactor Categories
        reactor_buttons = [
            "220 IPHWR", "540 IPHWR", "700 IPHWR", "Fetch", "Logout", "Help"
        ]
        for button_name in reactor_buttons:
            button = QPushButton(button_name)
            button.clicked.connect(self.reactor_button_clicked)
            self.sub_layout_1.addWidget(button)

        # Set size policy for main widgets to take full height
        sub_layout_1_widget.setLayout(self.sub_layout_1)
        sub_layout_2_widget.setLayout(self.sub_layout_2)
        sub_layout_3_widget.setLayout(self.sub_layout_3)

        # Create a horizontal layout for the sub layouts
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(sub_layout_1_widget)
        horizontal_layout.addWidget(sub_layout_2_widget)
        horizontal_layout.addWidget(sub_layout_3_widget)

        # Add the horizontal layout to the main layout
        self.main_layout.addLayout(horizontal_layout)

        # Go back button
        go_back_button = QPushButton("Go Back")
        
        go_back_button.clicked.connect(self.open_main_window)  # Close the current window
        go_back_button.clicked.connect(self.close)  # Close the current window
        go_back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.main_layout.addWidget(go_back_button, alignment=Qt.AlignBottom | Qt.AlignRight)

        # Set the main layout to the window
        self.setLayout(self.main_layout)

        # Track if 220 IPHWR grid is loaded
        self.is_220_loaded = False
        self.is_540_loaded = False
        self.is_700_loaded = False
    
    def open_main_window(self):
        # Create and display the main window with the username
        
        from main_window import MainWindow
        self.main_window = MainWindow(self.username)
        self.main_window.show()


    def reactor_button_clicked(self):
        sender = self.sender()
        
        if sender.text() == "220 IPHWR":
            self.reactor_type = sender.text()
            if not self.is_220_loaded:  # Check if already loaded
                self.clear_layout()  # Call the method correctly
                load_220_iphwr(self, self.sub_layout_2, self.reactor_type,self.username)
                self.is_540_loaded = False
                self.is_700_loaded = False
                self.is_220_loaded = True  # Mark as loaded
        elif sender.text() == "540 IPHWR":
            self.reactor_type = sender.text()
            if not self.is_540_loaded:  # Check if already loaded
                self.clear_layout()  # Call the method correctly
                load_540_iphwr(self, self.sub_layout_2, self.reactor_type,self.username)
                self.is_220_loaded = False
                self.is_700_loaded = False
                self.is_540_loaded = True  # Mark as loaded
        elif sender.text() == "700 IPHWR":
            self.reactor_type = sender.text()
            if not self.is_700_loaded:  # Check if already loaded
                self.clear_layout()  # Call the method correctly
                load_700_iphwr(self, self.sub_layout_2, self.reactor_type,self.username)
                self.is_220_loaded = False
                self.is_540_loaded = False
                self.is_700_loaded = True  # Mark as loaded
        elif sender.text()=="Fetch":
            self.fetch_window = FetchWindow()
            self.fetch_window.show()
        else:
            self.load_work_in_progress(sender.text())
            self.is_220_loaded = False
            self.is_540_loaded = False
            self.is_700_loaded = False

    def clear_layout(self):
        """Clear all widgets from the layout."""
        while self.sub_layout_2.count():
            item = self.sub_layout_2.takeAt(0)
            if item is not None:
                if item.widget():
                    item.widget().setParent(None)  # Removes the widget from the layout
                elif item.layout():
                    self.clear_layout_recursive(item.layout())  # If there's a sublayout, clear it recursively

    def clear_layout_recursive(self, layout):
        """Recursively clear a nested layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)  # Removes widget from the layout
                elif item.layout():
                    self.clear_layout_recursive(item.layout())

    def load_work_in_progress(self, button_name):
        self.clear_layout()

        # Display work in progress message
        work_in_progress_label = QLabel(f"Work in Progress for {button_name}")
        work_in_progress_label.setAlignment(Qt.AlignCenter)
        self.sub_layout_2.addWidget(work_in_progress_label)
