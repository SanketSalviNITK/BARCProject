from PyQt5.QtWidgets import QApplication,QDesktopWidget,QMessageBox,QLineEdit, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QLabel, QWidget
from PyQt5.QtCore import Qt
class FlawAssessment(QMainWindow):
    def __init__(self):
        super().__init__()
        # Enable High DPI Scaling for better display on high resolution screens
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        # Set up the main window
        self.setWindowTitle("Flaw Assessment")

        # Set initial window size dynamically (based on screen geometry)
        screen_geometry = QDesktopWidget().screenGeometry()  # Get screen geometry
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Resize the window to fit within the screen boundaries, leaving margins
        self.resize(int(screen_width * 0.8), int(screen_height * 0.7))   # Window size is 80% of screen width/height

        # Optionally, set a minimum window size based on screen dimensions
        self.setMinimumSize(600, 400)

        main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(main_widget)  # Main layout
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Create the top row layout to hold both left and right button groups
        top_row_layout = QHBoxLayout()
        top_row_layout.setAlignment(Qt.AlignTop)

        # Left-side buttons layout (Flaw Details, Channel Data, Calculation Log)
        left_side_layout = QHBoxLayout()  # Horizontal layout for left buttons
        left_side_layout.setAlignment(Qt.AlignLeft)

        flaw_details_button = self.create_button("Flaw Details")
        flaw_details_button.clicked.connect(self.toggle_flaw_buttons)  # Connect the button click event
        channel_data_button = self.create_button("Channel Data")
        calculation_log_button = self.create_button("Calculation Log")

        # Add left-side buttons to the layout
        left_side_layout.addWidget(flaw_details_button)
        left_side_layout.addWidget(channel_data_button)
        left_side_layout.addWidget(calculation_log_button)

        # Right-side buttons layout (Home, Help, Documentation, Logout)
        right_side_layout = QHBoxLayout()
        right_side_layout.setAlignment(Qt.AlignRight)

        home_button = self.create_button("Home")
        help_button = self.create_button("Help")
        documentation_button = self.create_button("Documentation")
        logout_button = self.create_button("Logout")

        right_side_layout.addWidget(home_button)
        right_side_layout.addWidget(help_button)
        right_side_layout.addWidget(documentation_button)
        right_side_layout.addWidget(logout_button)

        # Add the left and right side layouts to the top row layout
        top_row_layout.addLayout(left_side_layout)
        top_row_layout.addStretch()  # This will push the right-side buttons to the right
        top_row_layout.addLayout(right_side_layout)

        # Add the top row layout to the main layout
        self.main_layout.addLayout(top_row_layout)

        # Flaw Details Sub-buttons layout (initially hidden)
        self.flaw_buttons_layout = QVBoxLayout()  # Use QVBoxLayout for vertical arrangement
        self.flaw_buttons_layout.setAlignment(Qt.AlignLeft)
        self.flaw_buttons_layout.setSpacing(100)  # Adjust spacing between buttons
        
        
        self.flaw_buttons_layout.setContentsMargins(10, 250, 30, 40)

        # Create buttons for Flaw Details section
        self.type_of_flaw_button = self.create_button("Type of Flaw")
        self.type_of_flaw_button.clicked.connect(self.toggle_type_of_flaw_input)
        self.flaw_location_button = self.create_button("Flaw Location")
        self.flaw_dimension_button = self.create_button("Flaw Dimension")
        #self.flaw_dimension_button.clicked.connect(self.show_flaw_dimension_inputs)
        self.flaw_dimension_button.clicked.connect(self.toggle_flaw_dimension_input)


        # Initially hide these buttons
        self.type_of_flaw_button.setVisible(False)
        self.flaw_location_button.setVisible(False)
        self.flaw_dimension_button.setVisible(False)

        # Add the sub-buttons to the layout
        self.flaw_buttons_layout.addWidget(self.type_of_flaw_button)
        self.flaw_buttons_layout.addWidget(self.flaw_location_button)
        self.flaw_buttons_layout.addWidget(self.flaw_dimension_button)

        # Add the flaw buttons layout to the main layout (left side)
        self.main_layout.addLayout(self.flaw_buttons_layout)

        self.create_bottom_buttons()

        # Set the main layout as the central widget
        self.setCentralWidget(main_widget)
        self.show()        

    def toggle_flaw_buttons(self):
        """Toggle the visibility of the flaw details sub-buttons."""
        # If the buttons are currently hidden, show them
        are_buttons_visible = self.type_of_flaw_button.isVisible()

        if are_buttons_visible:
            self.type_of_flaw_button.setVisible(False)
            self.flaw_location_button.setVisible(False)
            self.flaw_dimension_button.setVisible(False)
        else:
            self.type_of_flaw_button.setVisible(True)
            self.flaw_location_button.setVisible(True)
            self.flaw_dimension_button.setVisible(True)
                # Ensure the layout is updated to reflect changes
            self.main_layout.update()

    def toggle_type_of_flaw_input(self):
        """Toggle the visibility of the flaw type input fields in the main window."""
        try:
            # Create the input layout only once
            if not hasattr(self, 'input_layout'):
                self.input_layout = QVBoxLayout()

                # Create radio buttons for flaw selection
                self.planar_flaw_radio = QRadioButton("Planar Flaw / Laminar Flaw")
                self.volumetric_flaw_radio = QRadioButton("Volumetric Flaw")

                # Set default selection
                self.planar_flaw_radio.setChecked(True)

                # Add them to the layout
                self.input_layout.addWidget(self.planar_flaw_radio)
                self.input_layout.addWidget(self.volumetric_flaw_radio)

                # Add a label for clarity
                heading_label = QLabel("Please select the type of flaw to be assessed:")
                self.input_layout.insertWidget(0, heading_label)

                # Create a wrapper widget for the input layout
                input_widget = QWidget(self)
                input_widget.setLayout(self.input_layout)

                # Set a fixed size for the input widget
                input_widget.setFixedSize(300, 200)

                # Add the input widget to the main layout at the top-center
                self.main_layout.insertWidget(1, input_widget, 0, Qt.AlignTop | Qt.AlignHCenter)
                self.input_widget = input_widget  # Save reference for toggling visibility

                # Connect the toggled signal to the function that shows/hides the additional options
                self.planar_flaw_radio.toggled.connect(self.show_planar_flaw_options)

            # Toggle visibility of the main flaw selection widget
            self.input_widget.setVisible(not self.input_widget.isVisible())

            self.main_layout.update()

        except Exception as e:
            print(f"Error occurred: {e}")
            # Handle the error (optional, display a message or log it)

    def show_planar_flaw_options(self):
        """Show additional options for planar flaws when selected."""
        try:
            # Check if the "Planar Flaw / Laminar Flaw" radio button is selected
            if self.planar_flaw_radio.isChecked():
                if not hasattr(self, 'planar_flaw_options_layout'):
                    # Create layout for additional radio buttons
                    self.planar_flaw_options_layout = QVBoxLayout()

                    # Create the radio buttons for additional options
                    self.axial_planar_flaw_radio = QRadioButton("Axial Planar Flaw")
                    self.circumferential_planar_flaw_radio = QRadioButton("Circumferential Planar Flaw")
                    
                    # Set default selection for the planar flaw options
                    self.axial_planar_flaw_radio.setChecked(False)

                    # Add them to the layout
                    self.planar_flaw_options_layout.addWidget(self.axial_planar_flaw_radio)
                    self.planar_flaw_options_layout.addWidget(self.circumferential_planar_flaw_radio)

                    # Add a label for clarity
                    options_label = QLabel("Please select the type of Planar Flaw:")
                    self.planar_flaw_options_layout.insertWidget(0, options_label)

                    # Create a wrapper widget for the planar flaw options
                    planar_flaw_options_widget = QWidget(self)
                    planar_flaw_options_widget.setLayout(self.planar_flaw_options_layout)
                    planar_flaw_options_widget.setFixedSize(200, 120)
                    
                    # Add the options widget to the main layout
                    self.main_layout.insertWidget(2, planar_flaw_options_widget, 0, Qt.AlignTop | Qt.AlignHCenter)
                    self.planar_flaw_options_widget = planar_flaw_options_widget  # Save reference for toggling visibility

                # Show the additional options widget
                self.planar_flaw_options_widget.setVisible(True)

                # Connect "Axial Planar Flaw" radio button to show flaw dimension inputs
                self.axial_planar_flaw_radio.toggled.connect(self.flaw_dimension_button)

            else:
                # Hide the additional planar flaw options when "Planar Flaw / Laminar Flaw" is not selected
                if hasattr(self, 'planar_flaw_options_widget'):
                    self.planar_flaw_options_widget.setVisible(False)
            self.main_layout.update()
        except Exception as e:
            print(f"Error occurred in show_planar_flaw_options: {e}")

    def toggle_flaw_dimension_input(self):
        """Toggle the visibility of flaw dimension input fields when 'Axial Planar Flaw' is selected."""
        try:
            # Check if "Axial Planar Flaw" radio button is selected
            if hasattr(self, 'axial_planar_flaw_radio') and self.axial_planar_flaw_radio.isChecked():
                # If the flaw dimension inputs have not been created yet, create them
                if not hasattr(self, 'flaw_dimension_widget'):
                    # Create the layout for flaw dimension inputs
                    self.flaw_dimension_layout = QVBoxLayout()

                    # Label for flaw depth in radial direction
                    flaw_depth_label = QLabel("Enter Flaw Depth in Radial Direction (mm):")
                    self.flaw_dimension_layout.addWidget(flaw_depth_label)

                    # Textbox for flaw depth input
                    self.flaw_depth_input = QLineEdit(self)
                    self.flaw_depth_input.setPlaceholderText("Enter depth in mm")
                    self.flaw_dimension_layout.addWidget(self.flaw_depth_input)

                    # Create layout for part wall flaw options
                    self.part_wall_flaw_layout = QVBoxLayout()

                    # Finite length and infinitely long options for part wall flaw
                    self.finite_length_radio = QRadioButton("Finite Length")
                    self.infinitely_long_radio = QRadioButton("Infinitely Long")
                    self.finite_length_radio.setChecked(True)

                    # Add the radio buttons to the layout
                    self.part_wall_flaw_layout.addWidget(self.finite_length_radio)
                    self.part_wall_flaw_layout.addWidget(self.infinitely_long_radio)

                    # Label for part wall flaw
                    part_wall_flaw_label = QLabel("Please select the part wall flaw type:")
                    self.part_wall_flaw_layout.insertWidget(0, part_wall_flaw_label)

                    # Create a widget to hold flaw dimension layout
                    flaw_dimension_widget = QWidget(self)
                    flaw_dimension_widget.setLayout(self.flaw_dimension_layout)
                    flaw_dimension_widget.setFixedSize(300, 120)

                    # Create a widget to hold part wall flaw layout
                    part_wall_flaw_widget = QWidget(self)
                    part_wall_flaw_widget.setLayout(self.part_wall_flaw_layout)
                    part_wall_flaw_widget.setFixedSize(300, 120)

                    # **Center the flaw dimension and part wall flaw widgets**
                    # Add both widgets to the main layout with alignment
                    self.main_layout.addWidget(flaw_dimension_widget, 0, Qt.AlignCenter)  # Center the flaw dimension widget
                    self.main_layout.addWidget(part_wall_flaw_widget, 0, Qt.AlignCenter)  # Center the part wall flaw widget

                    # Store references for toggling visibility
                    self.flaw_dimension_widget = flaw_dimension_widget
                    self.part_wall_flaw_widget = part_wall_flaw_widget

                    self.finite_length_radio.toggled.connect(self.toggle_flaw_length_input)


                # Make widgets visible
                self.flaw_dimension_widget.setVisible(True)
                self.part_wall_flaw_widget.setVisible(True)

            else:
                # Show a message or alert if "Axial Planar Flaw" is not selected
                QMessageBox.warning(self, "Selection Required", "Please select 'Axial Planar Flaw' before entering dimensions.")
            self.main_layout.update()
        except Exception as e:
            print(f"Error in toggle_flaw_dimension_input: {e}")



    
    def toggle_flaw_length_input(self):
        """Toggle the visibility of the flaw length input field when 'Finite Length' is selected."""
        try:
            # If "Finite Length" is selected, show the flaw length input field
            if self.finite_length_radio.isChecked():
                if not hasattr(self, 'flaw_length_input_widget'):
                    # Create the layout for flaw length input
                    flaw_length_layout = QVBoxLayout()

                    # Label for flaw length in axial direction
                    flaw_length_label = QLabel("Enter Flaw Length in Axial Direction (mm):")
                    flaw_length_layout.addWidget(flaw_length_label)

                    # Textbox for flaw length input
                    flaw_length_input = QLineEdit(self)
                    flaw_length_input.setPlaceholderText("Enter length in mm")
                    flaw_length_layout.addWidget(flaw_length_input)

                    # Create a widget to hold the flaw length input layout
                    flaw_length_input_widget = QWidget(self)
                    flaw_length_input_widget.setLayout(flaw_length_layout)
                    flaw_length_input_widget.setFixedSize(300, 120)

                    # Add the flaw length input widget to the main layout
                    self.main_layout.addWidget(flaw_length_input_widget, 0, Qt.AlignCenter)

                    # Store the reference for toggling visibility
                    self.flaw_length_input_widget = flaw_length_input_widget

                # Make flaw length input visible
                self.flaw_length_input_widget.setVisible(True)
            else:
                # Hide the flaw length input widget if "Finite Length" is not selected
                if hasattr(self, 'flaw_length_input_widget'):
                    self.flaw_length_input_widget.setVisible(False)

        except Exception as e:
            print(f"Error in toggle_flaw_length_input: {e}")
            


    def create_button(self, text):
        """Creates a styled button with the desired effects."""
        button = QPushButton(text)
        
        # Set the styles for the button
        button.setStyleSheet("""
            QPushButton {
                background-color: #e8eff5;
                color: #2e3d49;
                border: 2px solid #a0b2c1;
                border-radius: 6px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d1dce6;
            }
            QPushButton:pressed {
                background-color: #b8c8d8;
            }
        """)
        return button
    
    def create_bottom_buttons(self):
        """Create and arrange the buttons at the bottom of the window."""
        try:
            # Create buttons for auto-populate, clear input, and wipe all inputs
            self.auto_populate_button = self.create_button("Auto-populate from text file")
            self.clear_input_button = self.create_button("Clear input")
            self.wipe_all_button = self.create_button("Wipe all inputs")

            # Arrange the buttons horizontally (using QHBoxLayout)
            button_layout = QHBoxLayout()
            button_layout.addWidget(self.auto_populate_button)
            button_layout.addWidget(self.clear_input_button)
            button_layout.addWidget(self.wipe_all_button)

            # Add the buttons layout to the main layout horizontally
            self.main_layout.addLayout(button_layout)

            # Ensure the buttons are placed at the bottom of the window
            self.main_layout.addStretch()  # This stretch will push everything above down, keeping buttons at the bottom

        except Exception as e:
            print(f"Error occurred while creating bottom buttons: {e}")
            # Handle error (optional, display message or log it)

if __name__ == '__main__':
    app = QApplication([])
    window = FlawAssessment()
    app.exec_()
