import sys
import sqlite3
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QVBoxLayout, QGridLayout,
    QCheckBox, QPushButton, QListWidget, QFrame, QScrollArea,
    QWidget, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from view_property_window import ViewPropertyWindow
from chem_view_property_window import ChemViewPropertyWindow
from thermal_property_view_window import ThermalPropertyViewWindow
from physical_data_view_window import PhysicalDataViewwindow
from reactor_flux_view_window import  ReactorFluxViewwindow
from edit_property_window import EditPropertyWindow
from view_property_window import ViewPropertyWindow

from query_data_window import QueryDataWindow  # Adjust this line according to your project structure
from thermal_electrical_property_windows import EditThermalElectricalPropertyWindow
from chem_property_window import EditChemPropertyWindow
from physical_data_window import PhysicalDataWindow
from reactor_flux import ReactorFluxWindow
from property_viewer import MechanicalPropertyViewer, ISIDataViewer


class CoreLayoutWindow(QMainWindow):
    def __init__(self, parent, username, reactor_type, reactor_name, mode="edit"):
        super().__init__(parent)
        self.setWindowTitle(f"Core Layout - {reactor_type} {reactor_name} ({mode.capitalize()})")
        self.setGeometry(100, 100, 600, 400)

        self.setStyleSheet("""
    QWidget {
        background: qlineargradient(
            spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
            stop: 0 #a0c4ff,  /* Soft blue */
            stop: 1 #f8f9fa   /* Very light grey, almost white */
        );
    }
""")

        self.showMaximized()
        self.reactor_type = reactor_type
        self.reactor_name = reactor_name
        self.username = username
        self.db_name = ""
        
        # Initialize variables
        self.selected_channels = []
        self.selected_button = None
        self.select_all_state = False

        # Main layout
        main_layout = QHBoxLayout()

        # Left Part - Selected Channels and Footer (10%)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # "Selected Channels" label and list
        title_label = QLabel("Selected Channels")
        left_layout.addWidget(title_label)
        self.selected_channel_listbox = QListWidget()
        self.selected_channel_listbox.setMinimumHeight(850)
        left_layout.addWidget(self.selected_channel_listbox)

        # Spacer to push footer to the bottom
        left_layout.addStretch()

        # Footer label
        footer_label = QLabel("Developed by SVR Infotech")
        footer_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        left_layout.addWidget(footer_label)

        # Add the left part to the main layout
        main_layout.addWidget(left_widget, stretch=1)


        # Middle Part - Checkboxes (70%)
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)

        # Create a scroll area for the checkbox layout
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
        main_layout.addWidget(middle_widget, stretch=7)

        # Right Part - Properties Buttons (20%)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
      #  right_layout.addWidget(QLabel("Database Type"), alignment=Qt.AlignTop)

        # Database buttons
        databases = ["Manufacturing Data", "ISI data", "PTF", "PIE Data"]
        db_lable=QLabel("database Type")
        right_layout.addWidget(db_lable)
        right_layout.setSpacing(40)
        
        
        self.database_buttons = {}
        for database in databases:
            btn = QPushButton(database)
            btn.clicked.connect(lambda checked, db=database: self.select_database_button(db))
            right_layout.addWidget(btn)
            self.database_buttons[database] = btn

        # Action buttons
        action_layout = QHBoxLayout()
        self.edit_btn = QPushButton('Edit')
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_database)
        self.view_btn = QPushButton('View')
        self.view_btn.setEnabled(False)
        self.view_btn.clicked.connect(self.view_database)
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.clicked.connect(self.clear_selection)
        action_layout.addWidget(self.edit_btn)
        action_layout.addWidget(self.view_btn)
        action_layout.addWidget(self.clear_btn)
        right_layout.addLayout(action_layout)

        # Add Query Button
        self.query_btn = QPushButton("Query Data")
        self.query_btn.clicked.connect(self.open_query_window)
        right_layout.addWidget(self.query_btn)

        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        right_layout.addWidget(self.select_all_btn)

        # Back button
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.back_to_main)
        right_layout.addWidget(self.back_btn)

        # Add the right widget to the main layout
        main_layout.addWidget(right_widget, stretch=2)        

        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def update_selected_channels(self, state, row, col):
        channel = f"{row}{col:02}"
        if state == Qt.Checked:
            if channel not in self.selected_channels:
                self.selected_channels.append(channel)
                self.selected_channel_listbox.addItem(channel)
        else:
            if channel in self.selected_channels:
                self.selected_channels.remove(channel)
                items = self.selected_channel_listbox.findItems(channel, Qt.MatchExactly)
                if items:
                    row_index = self.selected_channel_listbox.row(items[0])
                    self.selected_channel_listbox.takeItem(row_index)

        # Check if no checkboxes are selected
        if not self.selected_channels:
            self.edit_btn.setEnabled(False)
            self.view_btn.setEnabled(False)
            for db, btn in self.database_buttons.items():
                btn.setStyleSheet("") 

    def select_database_button(self, db_name):
        if len(self.selected_channels) == 0:
            print("No Channel Selected")
            self.edit_btn.setEnabled(False)
            self.view_btn.setEnabled(False)
        else:
            self.db_name = db_name
            self.edit_btn.setEnabled(True)
            self.view_btn.setEnabled(True)

            for db, btn in self.database_buttons.items():
                if db == db_name:
                    btn.setStyleSheet("background-color: grey;")
                else:
                    btn.setStyleSheet("") 

    def open_query_window(self):
        """Open the query data window."""
        self.query_window = QueryDataWindow(self.selected_channels, self.db_name, self.reactor_type, self.reactor_name)
        self.query_window.show()

    def edit_database(self):
<<<<<<< HEAD
        if not self.selected_channels:
            QMessageBox.warning(self, "Warning", "No channels selected for editing.")
            return

        selected_channels_str = ', '.join(self.selected_channels)
        selected_reactor_type = self.reactor_type
        selected_reactor_name = self.reactor_name

        # Check the selected database and open the appropriate window
        if self.db_name == "Thermal & Electrical Property":
            QMessageBox.information(self, "Edit Database", f"User {self.username} Thermal & Electrical Property for channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            self.editPropertyWindow = EditThermalElectricalPropertyWindow(
                self.username, 
                selected_reactor_type, 
                selected_reactor_name, 
                self.selected_channels,
                self.db_name  # Pass the db_name
            )
            self.editPropertyWindow.show()

        elif self.db_name == "Chemical Properties":
            QMessageBox.information(self, "Edit Database", f"User {self.username} Chemical Property for channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            self.editPropertyWindow = EditChemPropertyWindow(
                self.username, 
                selected_reactor_type, 
                selected_reactor_name, 
                self.selected_channels,
                self.db_name  # Pass the db_name
            )
            self.editPropertyWindow.show()

        elif self.db_name == "Physical Data":  # Add a check for Physical Data
            QMessageBox.information(self, "Edit Database", f"User {self.username} Physical Data: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            self.editPropertyWindow = PhysicalDataWindow(
                self.username, 
                selected_reactor_type, 
                selected_reactor_name, 
                self.selected_channels,
                self.db_name  # Pass the db_name
            )
            self.editPropertyWindow.show()
            
        elif self.db_name == "Reactor Flux":  # Add a check for Physical Data
            QMessageBox.information(self, "Edit Database", f"User {self.username} Reactor Flux: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            self.editPropertyWindow = ReactorFluxViewwindow(
                self.username, 
                selected_reactor_type, 
                selected_reactor_name, 
                self.selected_channels,
                self.db_name  # Pass the db_name
            )
            self.editPropertyWindow.show()


        elif self.db_name=="Manufacturing Data":
            QMessageBox.information(self, "Edit Database", f"{self.db_name}User {self.username} Editing database for channels: {selected_channels_str} of Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            self.editPropertyWindow= MechanicalPropertyViewer(
                self.username, 
                selected_reactor_type, 
                selected_reactor_name, 
                self.selected_channels,
                self.db_name  # Pass the db_name
            )
            self.editPropertyWindow.show()
        elif self.db_name=="ISI data":
            QMessageBox.information(self, "Edit Database", f"{self.db_name}User {self.username} Editing database for channels: {selected_channels_str} of Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            self.editPropertyWindow= ISIDataViewer(
                self.username, 
                selected_reactor_type, 
                selected_reactor_name, 
                self.selected_channels,
                self.db_name  # Pass the db_name
            )
            self.editPropertyWindow.show()
        else:
            QMessageBox.information(self, "Edit Database", f"{self.db_name}User {self.username} Editing database for channels: {selected_channels_str} of Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            self.editPropertyWindow = EditPropertyWindow(
                self.username, 
                selected_reactor_type, 
                selected_reactor_name, 
                self.selected_channels, 
                self.db_name
            )
            self.editPropertyWindow.show()




    def view_database(self):
        if not self.selected_channels:
            QMessageBox.warning(self, "Warning", "No channels selected for viewing.")
            return

        selected_channels_str = ', '.join(self.selected_channels)
        selected_reactor_type = self.reactor_type
        selected_reactor_name = self.reactor_name

        # Check the selected database and open the appropriate window
        if self.db_name == "Chemical Properties":
            QMessageBox.information(self, "View Database", f"User {self.username} Viewing Chemical Properties for channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            
            # Open the ViewChemPropertyWindow for viewing chemical properties
            self.viewPropertyWindow = ChemViewPropertyWindow(
                selected_channels_str.split(', '),  # Split string back into a list
                self.db_name, 
                selected_reactor_type,  # Pass the reactor type
                selected_reactor_name   # Pass the reactor name
            )
            self.viewPropertyWindow.show()
            
        elif self.db_name == "Thermal & Electrical Property":
            QMessageBox.information(self, "View Database", f"User {self.username} Thermal & Electrical Property for channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            
            # Open the ViewChemPropertyWindow for viewing chemical properties
            self.viewPropertyWindow = ThermalPropertyViewWindow(
                selected_channels_str.split(', '),  # Split string back into a list
                self.db_name, 
                selected_reactor_type,  # Pass the reactor type
                selected_reactor_name   # Pass the reactor name
            )
            self.viewPropertyWindow.show()
            
        elif self.db_name == "Physical Data":
            QMessageBox.information(self, "View Database", f"User {self.username} Viewing Physical Data for channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            
            # Open the ViewChemPropertyWindow for viewing chemical properties
            self.viewPropertyWindow = PhysicalDataViewwindow(
                selected_channels_str.split(', '),  # Split string back into a list
                self.db_name, 
                selected_reactor_type,  # Pass the reactor type
                selected_reactor_name   # Pass the reactor name
            )
            self.viewPropertyWindow.show()
            
        elif self.db_name == "Reactor Flux":
            QMessageBox.information(self, "View Database", f"User {self.username} Viewing Reactor Flux for channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            
            # Open the ViewChemPropertyWindow for viewing chemical properties
            self.viewPropertyWindow = PhysicalDataViewwindow(
                selected_channels_str.split(', '),  # Split string back into a list
                self.db_name, 
                selected_reactor_type,  # Pass the reactor type
                selected_reactor_name   # Pass the reactor name
            )
            self.viewPropertyWindow.show()

        else:
            # Handle other database types (as already implemented)
            QMessageBox.information(self, "View Database", f"User {self.username} Viewing database Mnuafacturing Data  Window channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
            
            # Open the ViewPropertyWindow for other property types
            self.viewPropertyWindow = ViewPropertyWindow(
                selected_channels_str.split(', '), 
                self.db_name, 
                selected_reactor_type, 
                selected_reactor_name
            )
            self.viewPropertyWindow.show()

=======
        selected_channels_str = ','.join(self.selected_channels)
        selected_channels_str=selected_channels_str
        selected_reactor_type=self.reactor_type
        selected_reactor_name=self.reactor_name
        QMessageBox.information(self, "Edit Database", f"User {self.username} Editing database for channels: {selected_channels_str.split(",")} of Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
        self.editPropertyWindow=EditPropertyWindow(self.username, selected_reactor_type, selected_reactor_name, selected_channels_str.split(","), self.db_name)
        self.editPropertyWindow.show()

    def view_database(self):
        selected_channels_str = ','.join(self.selected_channels)
        selected_reactor_type=self.reactor_type
        selected_reactor_name=self.reactor_name
        QMessageBox.information(self, "View Database", f"User {self.username} Viewing database for channels: {selected_channels_str} Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
        self.viewPropertyWindow=ViewPropertyWindow(self.username,self.reactor_type,self.reactor_name, selected_channels_str.split(","), self.db_name)
        self.viewPropertyWindow.show()
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a

    def clear_selection(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
        self.selected_channel_listbox.clear()
        self.selected_channels.clear()

    def toggle_select_all(self):
        self.select_all_state = not self.select_all_state
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(self.select_all_state)

    def back_to_main(self):
        self.close()
