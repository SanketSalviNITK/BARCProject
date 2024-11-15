import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QRadioButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QGroupBox
)
from PyQt5.QtGui import QFont


class Parameter_Input_Window(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle('Parameter Input')
        self.setGeometry(100, 100, 1200, 700)  # Window Size

        # Main Layout
        main_layout = QVBoxLayout()

        # Top Bar
        self.top_label = QLabel("PREDICTION MODELS/ CADET", self)
        self.top_label.setFont(QFont('Arial', 14))
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.top_label)
        top_bar_layout.addStretch(1)  # Push the buttons to the right
        self.home_button = QPushButton('Home')
        self.help_button = QPushButton('Help')
        self.logout_button = QPushButton('Logout')
        top_bar_layout.addWidget(self.home_button)
        top_bar_layout.addWidget(self.help_button)
        top_bar_layout.addWidget(self.logout_button)

        # Tabs: Channel, Parameter Input, Setting/Solve, Post Processing
        tab_widget = QTabWidget()
        channel_tab = QWidget()
        parameter_tab = QWidget()
        setting_tab = QWidget()
        post_processing_tab = QWidget()

        # Setup each tab layout
        self.create_channel_tab(channel_tab)
        self.create_parameter_tab(parameter_tab)
        self.create_setting_tab(setting_tab)
        self.create_post_processing_tab(post_processing_tab)

        # Add tabs to tab widget
        tab_widget.addTab(channel_tab, "Channel For Analysis")  
        tab_widget.addTab(parameter_tab, "Parameter Input")  
        tab_widget.addTab(setting_tab, "Setting/Solve")
        tab_widget.addTab(post_processing_tab, "Post Processing")

        # Add top bar and tabs to main layout
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(tab_widget)

        # Set the layout to the window
        self.setLayout(main_layout)

    def create_channel_tab(self, channel_tab):
        """Creates layout for the Channel tab."""
        layout = QVBoxLayout()

        # Display a label instead of interactive buttons
        label = QLabel("Channel For Analysis (Functionality Disabled)", self)
        layout.addWidget(label)

        # Optionally, you can add more information or static content here
        channel_info_label = QLabel("This tab is currently disabled for analysis.", self)
        layout.addWidget(channel_info_label)

        # Set the layout for the channel tab
        channel_tab.setLayout(layout)

    def create_parameter_tab(self, parameter_tab):
        """Creates layout for the Parameter Input tab."""
        layout = QHBoxLayout()

        # Left panel buttons (540MWe, TAPS 3, A08)
        button_layout = QVBoxLayout()
        button1 = QPushButton("540MWe")
        button2 = QPushButton("TAPS 3")
        button3 = QPushButton("A08")
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)

        # Group box for Data Input Panel 1 (left side)
        data_group = QGroupBox("Data Input Panel 1")
        data_layout = QGridLayout()
        labels = [
            'Pressure Tube Length (mm)', 'Calandria Tube Length (mm)', 'Flux Length (mm)', 
            'PT Slope x = 0 (R)', 'PT Slope x = L (R)', 'PT Loading (kg/m)', 'CT Loading (kg/m)', 
            'PT Loading ISI (kg/m)', 'PT Inlet Temp (C)', 'PT Outlet Temp (C)'
        ]
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            input_field = QLineEdit()
            input_field.setFixedWidth(100)  # Set fixed width to make fields smaller
            data_layout.addWidget(label, i, 0)
            data_layout.addWidget(input_field, i, 1)

        data_group.setLayout(data_layout)

        # Group box for Data Input Panel 2 (right side)
        data_group2 = QGroupBox("Data Input Panel 2")
        data_layout2 = QGridLayout()
        labels2 = [
            'PT Operating Ys (GPa)', 'PT ISI Ys (GPa)', 'PT Original Inner Dia. (m)',
            'PT Original Thickness (mm)', 'CT Ys (GPa)', 'CT Inner Dia. (mm)',
            'CT Thickness (mm)', 'Garter Spring Dia. (mm)', 'CT/PT FFR', 'Reactor Full Power Hours'
        ]
        for i, label_text in enumerate(labels2):
            label = QLabel(label_text)
            input_field = QLineEdit()
            input_field.setFixedWidth(100)
            data_layout2.addWidget(label, i, 0)
            data_layout2.addWidget(input_field, i, 1)

        data_group2.setLayout(data_layout2)

        # Right Panel for Neutron Flux Data
        right_panel_group = QGroupBox("Neutron Flux Data")
        right_panel_layout = QVBoxLayout()
        radio1 = QRadioButton("Default 220MWe PHWR Geometry")
        radio2 = QRadioButton("Def Old GS 220MWe PHWR Geom")
        radio3 = QRadioButton("Default 540MWe PHWR Geometry")
        flux_options = QVBoxLayout()
        flux_options.addWidget(QRadioButton("Low Flux"))
        flux_options.addWidget(QRadioButton("Med Flux"))
        flux_options.addWidget(QRadioButton("Hi Flux"))
        flux_options.addWidget(QRadioButton("Custom Flux"))
        flux_options.addWidget(QRadioButton("Flux Database"))
        right_panel_layout.addWidget(radio1)
        right_panel_layout.addWidget(radio2)
        right_panel_layout.addWidget(radio3)
        right_panel_layout.addLayout(flux_options)
        right_panel_group.setLayout(right_panel_layout)

        # Bottom Buttons (for creep history and flux profile)
        bottom_button_layout = QVBoxLayout()
        button1 = QPushButton("Upld Creep Hist/WIF")
        button2 = QPushButton("Initialize State")
        button3 = QPushButton("Unload Custom Flux Profile Data")
        bottom_button_layout.addWidget(button1)
        bottom_button_layout.addWidget(button2)
        bottom_button_layout.addWidget(button3)

        # Add everything to the parameter layout
        layout.addLayout(button_layout)  # Left buttons
        layout.addWidget(data_group)  # Data Input Panel 1
        layout.addWidget(data_group2)  # Data Input Panel 2
        layout.addWidget(right_panel_group)  # Right panel for neutron flux data
        layout.addLayout(bottom_button_layout)  # Bottom buttons

        # Garter Spring Data Panel
        garter_spring_panel = self.create_garter_spring_panel()
        layout.addLayout(garter_spring_panel)  # Move garter spring panel here to the bottom

        # Set the layout for the parameter tab
        parameter_tab.setLayout(layout)

    def create_setting_tab(self, setting_tab):
        """Placeholder for Setting/Solve tab."""
        layout = QVBoxLayout()
        label = QLabel("Settings/Solve settings will be here.")
        layout.addWidget(label)
        setting_tab.setLayout(layout)

    def create_post_processing_tab(self, post_processing_tab):
        """Placeholder for Post Processing tab."""
        layout = QVBoxLayout()
        label = QLabel("Post Processing settings will be here.")
        layout.addWidget(label)
        post_processing_tab.setLayout(layout)

    def create_garter_spring_panel(self):
        """Creates a panel for garter spring data."""
        garter_spring_layout = QGridLayout()

        garter_spring_label = QLabel("Garter Spring Data Input")
        garter_spring_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        garter_spring_layout.addWidget(garter_spring_label, 0, 0, 1, 6)

        # Garter spring positions
        garter_spring_layout.addWidget(QLabel("GS1 Position"), 1, 0)
        garter_spring_layout.addWidget(QLineEdit("1525.0"), 1, 1)

        garter_spring_layout.addWidget(QLabel("GS2 Position"), 1, 2)
        garter_spring_layout.addWidget(QLineEdit("1990.0"), 1, 3)

        garter_spring_layout.addWidget(QLabel("GS3 Position"), 1, 4)
        garter_spring_layout.addWidget(QLineEdit("3210.0"), 1, 5)

        # Add an additional row for further spring data if necessary
        garter_spring_layout.addWidget(QLabel("GS4 Position"), 2, 0)
        garter_spring_layout.addWidget(QLineEdit(""), 2, 1)

        garter_spring_layout.addWidget(QLabel("GS5 Position"), 2, 2)
        garter_spring_layout.addWidget(QLineEdit(""), 2, 3)

        return garter_spring_layout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Parameter_Input_Window()
    window.show()
    sys.exit(app.exec_())