import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QVBoxLayout, QGridLayout,
    QCheckBox, QScrollArea, QWidget, QHBoxLayout, QRadioButton, 
    QComboBox, QPushButton, QButtonGroup, QMessageBox
)
from parameter_input import Parameter_Input_Window  # Ensure this module exists

class Prediction(QMainWindow):
    
    def __init__(self, parent=None, username="", reactor_type="", reactor_name="", mode="edit"):
        super().__init__(parent)
        self.setWindowTitle("PREDICTION MODELS/CADET")
        self.setGeometry(100, 100, 1000, 800)

        self.setStyleSheet(""" 
        QWidget {
            background: qlineargradient(
                spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                stop: 0 #a0c4ff,  /* Soft blue */
                stop: 1 #f8f9fa   /* Very light grey, almost white */
            );
        }
        """)

        self.reactor_type = reactor_type
        self.reactor_name = reactor_name
        self.username = username
        self.db_name = ""

        # Initialize variables
        self.selected_channel = None

        # Main layout
        main_layout = QHBoxLayout()

        # Left Side - Reactor Type, Reactor Name, and Channel ID (Buttons and Dropdowns)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Analysis Type (Custom Data / Reactor Specific)
        analysis_label = QLabel("Analysis Type")
        left_layout.addWidget(analysis_label)

        self.analysis_type_group = QButtonGroup(self)
        custom_data_radio = QRadioButton("Custom Data")
        reactor_specific_radio = QRadioButton("Reactor Specific")
        reactor_specific_radio.setChecked(True)

        self.analysis_type_group.addButton(custom_data_radio)
        self.analysis_type_group.addButton(reactor_specific_radio)

        left_layout.addWidget(custom_data_radio)
        left_layout.addWidget(reactor_specific_radio)

        # Reactor Type Dropdown
        reactor_type_label = QLabel("Reactor Type")
        left_layout.addWidget(reactor_type_label)

        self.reactor_type_dropdown = QComboBox()
        self.reactor_type_dropdown.addItems(["220 MWe", "540 MWe"])
        left_layout.addWidget(self.reactor_type_dropdown)

        # Reactor Name Dropdown
        reactor_name_label = QLabel("Reactor Name")
        left_layout.addWidget(reactor_name_label)

        self.reactor_name_dropdown = QComboBox()
        self.reactor_name_dropdown.addItems(["Reactor 1", "Reactor 2", "Reactor 3"])
        left_layout.addWidget(self.reactor_name_dropdown)

        # Add "Channel ID" button
        self.channel_id_button = QPushButton("Channel ID: None")
        self.channel_id_button.setFixedHeight(40)
        left_layout.addWidget(self.channel_id_button)

        main_layout.addWidget(left_widget, stretch=1)

        # Middle Part - Buttons and Checkboxes for channel selection
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)

        # Create a horizontal layout for the navigation buttons above the processing buttons
        nav_button_layout = QHBoxLayout()
        nav_button_layout.setAlignment(Qt.AlignRight)  # Align buttons to the right
        nav_button_layout.setSpacing(5)  # Decrease the spacing between the buttons

        # Home Button
        self.home_button = QPushButton("Home")
        self.home_button.setFixedWidth(80)  # Adjust the button width
        nav_button_layout.addWidget(self.home_button)

        # Help Button
        self.help_button = QPushButton("Help")
        self.help_button.setFixedWidth(80)  # Adjust the button width
        nav_button_layout.addWidget(self.help_button)

        # Logout Button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFixedWidth(80)  # Adjust the button width
        nav_button_layout.addWidget(self.logout_button)

        # Add navigation button layout to the middle layout at the top
        middle_layout.addLayout(nav_button_layout)

        # Create a horizontal layout for the buttons above the grid
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        # Parameter Input Button
        self.parameter_input_button = QPushButton("Parameter Input")
        self.parameter_input_button.setFixedWidth(150)
        self.parameter_input_button.clicked.connect(self.open_parameter_input)  # Connect to the method
        button_layout.addWidget(self.parameter_input_button)
        
        # Settings/Solve Button
        self.setting_solve_button = QPushButton("Setting/Solve")
        self.setting_solve_button.setFixedWidth(130)
        button_layout.addWidget(self.setting_solve_button)

        # Post Processing Button
        self.post_processing_button = QPushButton("Post Processing")
        self.post_processing_button.setFixedWidth(130)
        button_layout.addWidget(self.post_processing_button)

        # Open Channel Database Button
        self.open_channel_button = QPushButton("Open Channel Database")
        self.open_channel_button.setFixedWidth(200)
        self.open_channel_button.clicked.connect(self.open_channel_database)  # Connect the button to a function
        button_layout.addWidget(self.open_channel_button)

        # Add button layout to the middle layout
        middle_layout.addLayout(button_layout)

        # Scroll area for checkboxes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a frame inside the scroll area to hold the grid of checkboxes
        self.layout_frame = QWidget()
        self.scroll_area.setWidget(self.layout_frame)

        # Horizontal layout for the grid
        grid_layout = QGridLayout()
        self.layout_frame.setLayout(grid_layout)

        # Checkbox positions and skip locations
        self.checkbox_positions = {chr(row): list(range(1, 21)) for row in range(65, 85) if chr(row) != 'I'}
        self.skip_locations = {
            'A': list(range(1, 8)) + list(range(14, 21)),
            'B': list(range(1, 6)) + list(range(16, 21)),
            'C': list(range(1, 4)) + list(range(18, 21)),
            'D': list(range(1, 3)) + list(range(19, 21)),
            'E': list(range(1, 3)) + list(range(19, 21)),
            'F': [1, 20],
            'G': [1, 20],
            'N': [1, 20],
            'O': [1, 20],
            'P': [1, 20],
            'Q': list(range(1, 3)) + list(range(19, 21)),
            'R': list(range(1, 3)) + list(range(19, 21)),
            'S': list(range(1, 5)) + list(range(17, 21)),
            'T': list(range(1, 6)) + list(range(16, 21)),
        }

        # Add labels for the horizontal axis
        for col in range(1, 21):
            grid_layout.addWidget(QLabel(f"{col:02}"), 0, col)

        # Add labels for the vertical axis and checkboxes
        self.checkboxes = {}
        for row, cols in self.checkbox_positions.items():
            grid_layout.addWidget(QLabel(row), ord(row) - 64, 0)
            for col in cols:
                if row in self.skip_locations and col in self.skip_locations[row]:
                    continue

                checkbox = QCheckBox()
                checkbox.setMinimumHeight(40)
                checkbox.stateChanged.connect(lambda state, r=row, c=col: self.update_selected_channels(state, r, c))
                grid_layout.addWidget(checkbox, ord(row) - 64, col)
                self.checkboxes[f"{row}{col:02}"] = checkbox

        middle_layout.addWidget(self.scroll_area)

        # Add "CADET Documentation" button to the bottom-right corner
        documentation_button = QPushButton("CADET Documentation")
        documentation_button.setFixedWidth(180)

        # Create a layout at the bottom right for the documentation button
        bottom_right_layout = QHBoxLayout()
        bottom_right_layout.addStretch()  # Push the button to the right
        bottom_right_layout.addWidget(documentation_button)
        
        middle_layout.addLayout(bottom_right_layout)  # Add this layout to the middle layout

        main_layout.addWidget(middle_widget, stretch=7)

        # Set main layout in the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def open_parameter_input(self):
        """Open the parameter input window."""
        self.parameter_input = Parameter_Input_Window()  # Create an instance of Parameter_Input_Window
        self.parameter_input.show()  # Show the window

    def open_channel_database(self):
        """Open the channel database - implement this method according to your needs."""
        QMessageBox.information(self, "Info", "Channel Database opened!")  # Placeholder for actual database functionality

    def update_selected_channels(self, state, row, col):
        """Update the selected channels based on checkbox state changes."""
        if state == Qt.Checked:
            self.selected_channel = f"{row}{col:02}"
            self.channel_id_button.setText(f"Channel ID: {self.selected_channel}")
        else:
            self.selected_channel = None
            self.channel_id_button.setText("Channel ID: None")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    prediction = Prediction()
    prediction.show()
    sys.exit(app.exec_())