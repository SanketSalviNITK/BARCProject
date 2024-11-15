import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QRadioButton,
    QGroupBox
)

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFrame,
)

class ChannelData(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout()

        # Button to show channel data options
        self.channel_data_button = QPushButton("Channel Data")
        self.channel_data_button.setFixedWidth(300)
        self.channel_data_button.clicked.connect(self.show_channel_data_buttons)

        # Layout for the channel data button
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.channel_data_button)
        self.button_layout.addStretch()

        # Add button layout to the main layout
        self.layout.addLayout(self.button_layout)

        # Initialize frames for different inputs
        self.pt_geometry_frame = self.create_pt_geometry_frame()
        self.material_properties_frame = self.create_material_properties_frame()
        self.service_level_frame = self.create_service_level_frame()
        self.channel_level_frame = self.create_channel_level_frame()
        self.stress_flow_frame = self.create_stress_flow_frame()
        self.circumferential_flaw_frame = self.create_circumferential_flaw_frame()
        self.volumetric_flaw_frame = self.create_volumetric_flaw_frame()
        self.stress_volumetric_flaw_frame = self.create_stress_volumetric_flaw_frame()  # New frame for Stress Volumetric Flaw
        self.axial_stress_frame = self.create_axial_stress_frame()  # New frame for Axial Stress calculation

        # Set the main layout for the widget
        self.setLayout(self.layout)

        # Hide all frames initially
        self.hide_all_frames()

        # Create buttons for different data options
        self.button_names = [
            "PT Geometry",
            "Material Properties",
            "Service Level",
            "Channel Level",
            "Stress at Flow Location",
            "Circumferential Planar Flaw",
            "Volumetric Flaw",
            "Stress Volumetric Flaw",  # New button added here
            "Calculate Axial Stress"  # New button for calculating axial stress
        ]
        self.buttons = []

    def hide_all_frames(self):
        """Hide all input frames initially."""
        self.pt_geometry_frame.setVisible(False)
        self.material_properties_frame.setVisible(False)
        self.service_level_frame.setVisible(False)
        self.channel_level_frame.setVisible(False)
        self.stress_flow_frame.setVisible(False)
        self.circumferential_flaw_frame.setVisible(False)
        self.volumetric_flaw_frame.setVisible(False)
        self.stress_volumetric_flaw_frame.setVisible(False)  # Hide new frame initially
        self.axial_stress_frame.setVisible(False)  # Hide axial stress frame initially

    def show_channel_data_buttons(self):
        """Display all buttons for channel data options at once."""
        # Clear existing buttons if any
        self.clear_channel_data_buttons()

        # Create and show each button
        for button_name in self.button_names:
            button = QPushButton(button_name)
            button.setFixedSize(250, 60)  # Set a larger fixed size for buttons
            button.clicked.connect(lambda _, name=button_name: self.toggle_button_info(name, button))
            self.layout.addWidget(button)
            self.buttons.append(button)  # Keep track of created buttons

    def clear_channel_data_buttons(self):
        """Clear existing buttons from the main layout."""
        for button in self.buttons:
            button.deleteLater()
        self.buttons.clear()

    def toggle_button_info(self, button_name, button):
        """Toggle relevant input fields based on the clicked button."""
        # Hide all frames initially
        self.hide_all_frames()

        # Change button color to indicate selection
        for b in self.buttons:
            b.setStyleSheet("")  # Reset all button styles
        button.setStyleSheet("background-color: lightblue;")  # Change color of the selected button

        # Display only the selected button's input section
        if button_name == "PT Geometry":
            self.pt_geometry_frame.setVisible(True)
            self.layout.addWidget(self.pt_geometry_frame)
        elif button_name == "Material Properties":
            self.material_properties_frame.setVisible(True)
            self.layout.addWidget(self.material_properties_frame)
        elif button_name == "Service Level":
            self.service_level_frame.setVisible(True)
            self.layout.addWidget(self.service_level_frame)
        elif button_name == "Channel Level":
            self.channel_level_frame.setVisible(True)
            self.layout.addWidget(self.channel_level_frame)
        elif button_name == "Stress at Flow Location":
            self.stress_flow_frame.setVisible(True)
            self.layout.addWidget(self.stress_flow_frame)
        elif button_name == "Circumferential Planar Flaw":
            self.circumferential_flaw_frame.setVisible(True)
            self.layout.addWidget(self.circumferential_flaw_frame)
        elif button_name == "Volumetric Flaw":
            self.volumetric_flaw_frame.setVisible(True)
            self.layout.addWidget(self.volumetric_flaw_frame)
        elif button_name == "Stress Volumetric Flaw":  # New condition for Stress Volumetric Flaw
            self.stress_volumetric_flaw_frame.setVisible(True)
            self.layout.addWidget(self.stress_volumetric_flaw_frame)
        elif button_name == "Calculate Axial Stress":  # New condition for Calculate Axial Stress
            self.axial_stress_frame.setVisible(True)
            self.layout.addWidget(self.axial_stress_frame)

    

        
    def create_pt_geometry_frame(self):
        """Create PT Geometry input frame."""
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        # Set the background color of the frame to light blue
        frame.setStyleSheet("background-color: lightblue;")

        # Thickness input field with DB and MPE buttons
        thickness_label = QLabel("Pressure Tube Thickness (mm):")
        thickness_label.setStyleSheet("color: navy;")  # Set label color to dark blue
        thickness_input = QLineEdit()
        thickness_input.setPlaceholderText("Enter thickness")
        thickness_input.setFixedSize(200, 25)  # Set fixed size for thickness input
        thickness_input.setStyleSheet("background-color: white; color: black;")  # White background for input
        thickness_db_button = QPushButton("DB")
        thickness_mpe_button = QPushButton("MPE")
        thickness_db_button.setStyleSheet("background-color: darkblue; color: white;")  # Dark blue buttons
        thickness_mpe_button.setStyleSheet("background-color: darkblue; color: white;")
        thickness_db_button.clicked.connect(lambda: self.on_db_button_click("Pressure Tube Thickness"))
        thickness_mpe_button.clicked.connect(lambda: self.on_mpe_button_click("Pressure Tube Thickness"))

        # Diameter input field with DB and MPE buttons
        diameter_label = QLabel("Pressure Tube Inside Diameter (mm):")
        diameter_label.setStyleSheet("color: navy;")  # Set label color to dark blue
        diameter_input = QLineEdit()
        diameter_input.setPlaceholderText("Enter diameter")
        diameter_input.setFixedSize(200, 25)  # Set fixed size for diameter input
        diameter_input.setStyleSheet("background-color: white; color: black;")  # White background for input
        diameter_db_button = QPushButton("DB")
        diameter_mpe_button = QPushButton("MPE")
        diameter_db_button.setStyleSheet("background-color: darkblue; color: white;")  # Dark blue buttons
        diameter_mpe_button.setStyleSheet("background-color: darkblue; color: white;")
        diameter_db_button.clicked.connect(lambda: self.on_db_button_click("Pressure Tube Inside Diameter"))
        diameter_mpe_button.clicked.connect(lambda: self.on_mpe_button_click("Pressure Tube Inside Diameter"))

        # Layout for Thickness field, input, and buttons
        thickness_layout = QHBoxLayout()
        thickness_layout.addWidget(thickness_label)
        thickness_layout.addWidget(thickness_input)
        thickness_layout.addWidget(thickness_db_button)
        thickness_layout.addWidget(thickness_mpe_button)

        # Layout for Diameter field, input, and buttons
        diameter_layout = QHBoxLayout()
        diameter_layout.addWidget(diameter_label)
        diameter_layout.addWidget(diameter_input)
        diameter_layout.addWidget(diameter_db_button)
        diameter_layout.addWidget(diameter_mpe_button)

        # Add layouts to the frame
        layout.addLayout(thickness_layout)
        layout.addLayout(diameter_layout)

        return frame


    def create_material_properties_frame(self):
        """Create Material Properties input frame."""
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        labels = [
            "Material Stress Intensity (MPa√m):",
            "Young's Modulus (MPa):",
            "Poisson's Ratio:",
            "Yield Strength (MPa):",
            "Ultimate Tensile Strength (MPa):",
            "Flow Stress (MPa):"
        ]

        for label_text in labels:
            # Create a horizontal layout for each input field
            horizontal_layout = QHBoxLayout()
            
            # Create and add the label
            label = QLabel(label_text)
            horizontal_layout.addWidget(label)

            # Create and add the input field
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter {label_text.lower()}")
            input_field.setFixedSize(200, 25)  # Set fixed size for input fields
            horizontal_layout.addWidget(input_field)

            # Create and add the DB button
            db_button = QPushButton("DB")
            db_button.clicked.connect(lambda: self.on_db_button_click(label_text))
            horizontal_layout.addWidget(db_button)

            # Create and add the MPE button
            mpe_button = QPushButton("MPE")
            mpe_button.clicked.connect(lambda: self.on_mpe_button_click(label_text))
            horizontal_layout.addWidget(mpe_button)

            # Add the horizontal layout to the main layout
            layout.addLayout(horizontal_layout)

        return frame

    def create_service_level_frame(self):
        """Create Service Level input frame."""
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        # Create a group box for selecting service levels
        service_level_group = QGroupBox("Select Service Level")
        service_level_layout = QVBoxLayout()
        service_level_group.setLayout(service_level_layout)

        # Create radio buttons for each service level
        self.level_a_radio = QRadioButton("Select Level A")
        self.level_b_radio = QRadioButton("Select Level B")
        self.level_c_radio = QRadioButton("Select Level C")
        self.level_d_radio = QRadioButton("Select Level D")

        # Add radio buttons to the group box layout
        service_level_layout.addWidget(self.level_a_radio)
        service_level_layout.addWidget(self.level_b_radio)
        service_level_layout.addWidget(self.level_c_radio)
        service_level_layout.addWidget(self.level_d_radio)

        # Connect radio button signals to the method to show/hide the additional panel
        self.level_a_radio.toggled.connect(self.update_additional_panel)
        self.level_b_radio.toggled.connect(self.update_additional_panel)
        self.level_c_radio.toggled.connect(self.update_additional_panel)
        self.level_d_radio.toggled.connect(self.update_additional_panel)

        # Add the group box to the main layout
        layout.addWidget(service_level_group)

        # Additional panel for Factor of Safety and Factor of Security
        self.additional_panel = self.create_additional_panel()
        layout.addWidget(self.additional_panel)

        return frame

    def create_additional_panel(self):
        """Create additional panel for Factor of Safety and Security."""
        panel = QFrame()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Factor of Safety
        fos_label = QLabel("Factor of Safety on Pressure for the selected service level is:")
        self.fos_input = QLineEdit()
        layout.addWidget(fos_label)
        layout.addWidget(self.fos_input)

        # Factor of Security
        fos_sec_label = QLabel("Factor of Safety on plastic collapse for the selected service level is:")
        self.fos_sec_input = QLineEdit()
        layout.addWidget(fos_sec_label)
        layout.addWidget(self.fos_sec_input)

        # Initially hide the additional panel
        panel.setVisible(False)
        return panel

    def update_additional_panel(self):
        """Show or hide the additional panel based on selected service level."""
        selected = self.level_a_radio.isChecked() or self.level_b_radio.isChecked() or \
                   self.level_c_radio.isChecked() or self.level_d_radio.isChecked()
        self.additional_panel.setVisible(selected)

    def create_channel_level_frame(self):
        """Create Channel Level input frame."""
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        # Channel level inputs with labels and input fields
        channel_label = QLabel("Channel Level Inputs:")
        layout.addWidget(channel_label)

        # Channel internal pressure input
        pressure_layout = QHBoxLayout()  # Horizontal layout for pressure label, input, and buttons
        pressure_label = QLabel("Channel internal pressure in MPa:")
        pressure_input = QLineEdit()
        pressure_input.setPlaceholderText("Enter Internal Pressure")
        
        # Create DB and MPE buttons for pressure
        db_button_pressure = QPushButton("DB")
        mpe_button_pressure = QPushButton("MPE")

        # Add widgets to the pressure layout
        pressure_layout.addWidget(pressure_label)
        pressure_layout.addWidget(pressure_input)
        pressure_layout.addWidget(db_button_pressure)
        pressure_layout.addWidget(mpe_button_pressure)
        layout.addLayout(pressure_layout)  # Add horizontal layout to the main layout

        # Temperature of pressure tube input
        temperature_layout = QHBoxLayout()  # Horizontal layout for temperature label, input, and buttons
        temperature_label = QLabel("Temperature of pressure tube in °C:")
        temperature_input = QLineEdit()
        temperature_input.setPlaceholderText("Enter Temperature")

        # Create DB and MPE buttons for temperature
        db_button_temp = QPushButton("DB")
        mpe_button_temp = QPushButton("MPE")

        # Add widgets to the temperature layout
        temperature_layout.addWidget(temperature_label)
        temperature_layout.addWidget(temperature_input)
        temperature_layout.addWidget(db_button_temp)
        temperature_layout.addWidget(mpe_button_temp)
        layout.addLayout(temperature_layout)  # Add horizontal layout to the main layout

        return frame


    def create_stress_flow_frame(self):
        """Create Stress at Flow Location input frame."""
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        # Stress flow input fields with labels and input fields
        stress_label = QLabel("Stress at Flow Location Inputs:")
        layout.addWidget(stress_label)

        # Define a fixed width for all input fields
        input_field_width = 200

        # Nominal hoop stress input
        nominal_stress_layout = QHBoxLayout()  # Horizontal layout for the label and input
        nominal_stress_label = QLabel("Nominal hoop stress (far field) due to internal pressure in MPa:")
        nominal_stress_input = QLineEdit()
        nominal_stress_input.setPlaceholderText("Enter Nominal Hoop Stress")
        nominal_stress_input.setFixedWidth(input_field_width)  # Set fixed width
        nominal_stress_layout.addWidget(nominal_stress_label)
        nominal_stress_layout.addWidget(nominal_stress_input)
        layout.addLayout(nominal_stress_layout)  # Add horizontal layout to the main layout

        # Hoop stress at flaw location input
        flaw_stress_layout = QHBoxLayout()  # Horizontal layout for the label and input
        flaw_stress_label = QLabel("Hoop stress at flaw location due to internal pressure in MPa:")
        flaw_stress_input = QLineEdit()
        flaw_stress_input.setPlaceholderText("Enter Hoop Stress at Flaw Location")
        flaw_stress_input.setFixedWidth(input_field_width)  # Set fixed width
        flaw_stress_layout.addWidget(flaw_stress_label)
        flaw_stress_layout.addWidget(flaw_stress_input)
        layout.addLayout(flaw_stress_layout)  # Add horizontal layout to the main layout

        return frame

    def create_circumferential_flaw_frame(self):
        """Create Circumferential Planar Flaw input frame."""
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        # Label for Circumferential Planar Flaw Inputs
        flaw_label = QLabel("Circumferential Planar Flaw Inputs:")
        layout.addWidget(flaw_label)

        # Additional input fields
        prompts = [
            "Enter dead weight primary bending moment at the end of pressure tube design life in Nmm:",
            "Enter Current evaluation time in years of reactor operation:",
            "Enter Reactor life at the time of pressure tube installation in years:",
            "Enter Pressure tube design life in years:",
            "Enter primary bending moment in the vertical plane of the pressure tube due to a seismic event in Nmm:",
            "Enter primary bending moment in the horizontal plane of the pressure tube due to a seismic event in Nmm:",
            "Enter secondary bending moment at the start of pressure tube design life in Nmm:",
            "Enter secondary bending moment at the end of pressure tube design life in Nmm:",
            "Enter primary axial force due to thrust from fuelling machine, friction of moving fuel bundles, feeder pipe reactions, hydraulic drag force, channel bellows force etc. in N:",
            "Enter Secondary axial force due to bearing friction from the fuelling machine, longitudinal creep expansion of the pressure tube, thermal loads etc. in N:",
            "Enter channel internal pressure in MPa:"
        ]

        for prompt in prompts:
            # Create a horizontal layout for each label-input pair
            h_layout = QHBoxLayout()

            # Create label and input field
            label = QLabel(prompt)
            input_field = QLineEdit()
            input_field.setPlaceholderText("Enter value")
            
            # Set a fixed size for input fields
            input_field.setFixedSize(200, 25)  # Set width and height to your desired size

            # Add label and input field to horizontal layout
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)

            # Add the horizontal layout to the main vertical layout
            layout.addLayout(h_layout)

        return frame

    
    def create_volumetric_flaw_frame(self):
        """Create a frame for Volumetric Flaw input with detailed entries displayed side-by-side with their labels."""
        frame = QFrame()
        layout = QVBoxLayout()
        
        # Helper function to create a horizontal layout for label and input field
        def add_labeled_input(label_text, with_buttons=False):
            labeled_layout = QHBoxLayout()
            labeled_layout.addWidget(QLabel(label_text))
            
            # Create QLineEdit with a fixed size
            line_edit = QLineEdit()
            line_edit.setFixedSize(200, 25)  # Set fixed size for all input fields

            if with_buttons:
                # Create buttons for DB and MPE
                db_button = QPushButton("DB")
                mpe_button = QPushButton("MPE")
                labeled_layout.addWidget(line_edit)
                labeled_layout.addWidget(db_button)
                labeled_layout.addWidget(mpe_button)
            else:
                labeled_layout.addWidget(line_edit)
            
            layout.addLayout(labeled_layout)

        # Add input fields with labels
        add_labeled_input("Channel internal pressure in MPa:", with_buttons=True)
        add_labeled_input("Temperature of pressure tube in C:", with_buttons=True)
        add_labeled_input("Enter dead weight primary bending moment at the end of pressure tube design life in Nmm:")
        add_labeled_input("Enter Current evaluation time in years of reactor operation:")
        add_labeled_input("Enter Reactor life at the time of pressure tube installation in years:")
        add_labeled_input("Enter Pressure tube design life in years:")
        add_labeled_input("Enter primary bending moment in the vertical plane of the pressure tube due to a seismic event in Nmm:")
        add_labeled_input("Enter primary bending moment in the horizontal plane of the pressure tube due to a seismic event in Nmm:")
        add_labeled_input("Enter secondary bending moment at the start of pressure tube design life in Nmm:")
        add_labeled_input("Enter secondary bending moment at the end of pressure tube design life in Nmm:")
        add_labeled_input("Enter primary axial force due to thrust from fuelling machine, friction of moving fuel bundles, feeder pipe reactions, hydraulic drag force, channel bellows force etc. in N:")
        add_labeled_input("Enter Secondary axial force due to bearing friction from the fuelling machine, longitudinal creep expansion of the pressure tube, thermal loads etc. in N:")
        add_labeled_input("Enter channel internal pressure in MPa:")

        frame.setLayout(layout)
        self.layout.addWidget(frame)
        return frame    

    def create_stress_volumetric_flaw_frame(self):
        """Create the frame for Calculated Hoop Stress and Calculated Axial Stress with titled group boxes and input fields."""
        # Main frame setup
        frame = QFrame()
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)

        # Define a fixed width for all input fields to ensure uniformity
        input_field_width = 200

        # Group box for Calculated Hoop Stress Data
        group_box_hoop = QGroupBox("Calculated Hoop Stress")
        group_box_hoop.setStyleSheet("font-size: 14px;")
        group_box_hoop_layout = QVBoxLayout()
        group_box_hoop.setLayout(group_box_hoop_layout)

        # Section for Nominal Hoop Stress (Far Field)
        nominal_hoop_stress_layout = QHBoxLayout()
        
        # Label for Nominal Hoop Stress
        nominal_hoop_stress_label = QLabel("Nominal Hoop Stress (Far Field) due to Internal Pressure in MPa:")
        nominal_hoop_stress_layout.addWidget(nominal_hoop_stress_label)
        
        # Input field for Nominal Hoop Stress
        self.nominal_hoop_stress_input = QLineEdit()
        self.nominal_hoop_stress_input.setPlaceholderText("Enter Nominal Hoop Stress")
        self.nominal_hoop_stress_input.setFixedWidth(input_field_width)  # Set fixed width
        nominal_hoop_stress_layout.addWidget(self.nominal_hoop_stress_input)
        
        # Add to group box layout
        group_box_hoop_layout.addLayout(nominal_hoop_stress_layout)

        # Section for Hoop Stress at Flaw Location
        flaw_hoop_stress_layout = QHBoxLayout()
        
        # Label for Hoop Stress at Flaw Location
        flaw_hoop_stress_label = QLabel("Hoop Stress at Flaw Location due to Internal Pressure in MPa:")
        flaw_hoop_stress_layout.addWidget(flaw_hoop_stress_label)
        
        # Input field for Hoop Stress at Flaw Location
        self.flaw_hoop_stress_input = QLineEdit()
        self.flaw_hoop_stress_input.setPlaceholderText("Enter Hoop Stress at Flaw Location")
        self.flaw_hoop_stress_input.setFixedWidth(input_field_width)  # Set fixed width
        flaw_hoop_stress_layout.addWidget(self.flaw_hoop_stress_input)
        
        # Add to group box layout
        group_box_hoop_layout.addLayout(flaw_hoop_stress_layout)

        # Add Calculated Hoop Stress group box to main frame layout
        frame_layout.addWidget(group_box_hoop)

        # Group box for Calculated Axial Stress Data
        group_box_axial = QGroupBox("Calculated Axial Stress")
        group_box_axial.setStyleSheet("font-size: 14px;")
        group_box_axial_layout = QVBoxLayout()
        group_box_axial.setLayout(group_box_axial_layout)

        # List of labels for each input field in Calculated Axial Stress
        axial_stress_labels = [
            "Nominal primary axial stress due to internal pressure in Nm:",
            "Nominal primary bending stress due to dead weight and seismic loads in Nm:",
            "Nominal secondary bending stress in Nm:",
            "Primary axial stress due to primary axial forces in N:",
            "Secondary axial stress due to secondary axial forces in N:",
            "Total nominal primary axial stress on the pressure tube in N:",
            "Total nominal axial stress on the pressure tube in N:"
        ]

        # Add the seven specific input fields with labels to the Calculated Axial Stress group box
        for label_text in axial_stress_labels:
            axial_stress_layout = QHBoxLayout()
            
            # Label for each input field
            axial_stress_label = QLabel(label_text)
            axial_stress_layout.addWidget(axial_stress_label)
            
            # Input field for Axial Stress
            axial_stress_input = QLineEdit()
            axial_stress_input.setPlaceholderText("Enter " + label_text.split(" in ")[0])
            axial_stress_input.setFixedWidth(input_field_width)  # Set fixed width
            axial_stress_layout.addWidget(axial_stress_input)
            
            # Add each axial stress layout to the group box layout
            group_box_axial_layout.addLayout(axial_stress_layout)

        # Add Calculated Axial Stress group box to main frame layout
        frame_layout.addWidget(group_box_axial)

        return frame
    
    def create_axial_stress_frame(self):
        """Create Axial Stress calculation frame with multiple input fields."""
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        # Title label for Axial Stress
        title_label = QLabel("Calculate Axial Stress:")
        layout.addWidget(title_label)

        # Input fields for different stresses
        input_fields = [
            ("Nominal primary axial stress due to internal pressure in Nm:", "Nominal Axial Stress"),
            ("Nominal primary bending stress due to dead weight and seismic loads in Nm:", "Bending Stress"),
            ("Nominal secondary bending stress in Nm:", "Secondary Bending Stress"),
            ("Primary axial stress due to primary axial forces in N:", "Primary Axial Forces"),
            ("Secondary axial stress due to secondary axial forces in N:", "Secondary Axial Forces"),
            ("Total nominal primary axial stress on the pressure tube in N:", "Total Primary Axial Stress"),
            ("Total nominal axial stress on the pressure tube in N:", "Total Axial Stress"),
        ]

        # Create input fields dynamically
        self.axial_stress_inputs = {}
        for label_text, field_name in input_fields:
            input_layout = QHBoxLayout()
            input_label = QLabel(label_text)
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter {field_name}")
            input_layout.addWidget(input_label)
            input_layout.addWidget(input_field)
            layout.addLayout(input_layout)
            self.axial_stress_inputs[field_name] = input_field  # Store input field references

      

        # Label to display the result
        self.axial_stress_result_label = QLabel("")
        layout.addWidget(self.axial_stress_result_label)

        return frame    
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Channel Data Input")
        self.setGeometry(100, 100, 1200, 900)

        # Create ChannelData widget and set it as central widget
        self.channel_data_widget = ChannelData()
        self.setCentralWidget(self.channel_data_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    channel_data = ChannelData()
    main_window.setCentralWidget(channel_data)
    main_window.setWindowTitle("Channel Data Input")
    main_window.setGeometry(100, 100, 1200, 900)  # Set window size
    main_window.show()
    sys.exit(app.exec_())