from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QVBoxLayout, QGridLayout,
    QCheckBox, QPushButton, QListWidget, QFrame, QScrollArea,
    QWidget, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

from edit_property_window import EditPropertyWindow


class CoreLayoutWindow(QMainWindow):
    def __init__(self, parent, reactor_type, reactor_name, mode="edit"):
        super().__init__(parent)  # Call the superclass's __init__
        self.setWindowTitle(f"Core Layout - {reactor_type} {reactor_name} ({mode.capitalize()})")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowState(Qt.WindowMaximized)  # Maximize window
        self.setFixedSize(1200, 500)  # Set a fixed size
        self.reactor_type=reactor_type
        self.reactor_name=reactor_name
        # Initialize variables
        self.selected_channels = []
        self.selected_button = None
        self.select_all_state = False

        # Main layout - Horizontal layout for 3 parts
        main_layout = QHBoxLayout()

        # Left Part - Selected Channels (10%)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        title_label = QLabel("Selected Channels")
        left_layout.addWidget(title_label)
        self.selected_channel_listbox = QListWidget()
        self.selected_channel_listbox.setMinimumHeight(150)
        left_layout.addWidget(self.selected_channel_listbox)
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
        if reactor_type!="540 IPHWR":
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
            
        else:
            # Checkbox positions and skip locations for the 396 checkbox layout
            self.checkbox_positions = {chr(row): list(range(1, 21)) for row in range(65, 85) if chr(row) != 'I'}
            self.checkbox_positions['T'] = list(range(1, 15))  # T (14 checkboxes)

            self.skip_locations = {
                'A': list(range(1, 8)) + list(range(16, 23)),
                'B': list(range(1, 6)) + list(range(18, 23)),
                'C': list(range(1, 4)) + list(range(19, 23)),
                'D': list(range(1, 3)) + list(range(20, 23)),
                'E': [1, 22],
                'F': [1, 22],
                'G': [1, 22],
                'N': [1, 22],
                'O': [1, 22],
                'P': [1, 22],
                'Q': [1, 22],
                'R': list(range(1, 3)) + list(range(20, 23)),
                'S': list(range(1, 5)) + list(range(18, 23)),
                'T': list(range(1, 6)) + list(range(17, 23)),  # Adjusting for 14 total
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
                checkbox.stateChanged.connect(lambda state, r=row, c=col: self.update_selected_channels(state, r, c))
                grid_layout.addWidget(checkbox, ord(row) - 64, col)
                self.checkboxes[f"{row}{col:02}"] = checkbox

        middle_layout.addWidget(self.scroll_area)
        main_layout.addWidget(middle_widget, stretch=7)

        # Right Part - Properties Buttons (20%)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(QLabel("Database Type"), alignment=Qt.AlignTop)

        # Database buttons
        databases = ["Mechanical Properties", "Chemical Properties", "Thermal & Electrical Property", "Physical Data", "Reactor Flux", "Inspection Data"]
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
                self.selected_channel_listbox.takeItem(self.selected_channel_listbox.row(channel))

    def select_database_button(self, db_name):
        if self.selected_button:
            self.selected_button.setStyleSheet("background-color: lightblue;")
        self.selected_button = self.database_buttons[db_name]
        self.selected_button.setStyleSheet("background-color: lightgray;")
        self.edit_btn.setEnabled(True)
        self.view_btn.setEnabled(True)

    def edit_database(self):
        selected_channels_str = ', '.join(self.selected_channels)
        selected_reactor_type=self.reactor_type
        selected_reactor_name=self.reactor_name
        QMessageBox.information(self, "Edit Database", f"Editing database for channels: {selected_channels_str} of Reactor Type: {selected_reactor_type} and Reactor Name: {selected_reactor_name}")
        EditPropertyWindow(selected_channels_str,selected_reactor_type,selected_reactor_name)

    def view_database(self):
        selected_channels_str = ', '.join(self.selected_channels)
        QMessageBox.information(self, "View Database", f"Viewing database for channels: {selected_channels_str}")

    def clear_selection(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
        self.selected_channel_listbox.clear()
        self.selected_channels.clear()

    def toggle_select_all(self):
        self.select_all_state = not self.select_all_state
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(self.select_all_state)
        self.selected_channel_listbox.clear()
        self.selected_channels.clear()
        if self.select_all_state:
            self.selected_channels = list(self.checkboxes.keys())
            for channel in self.selected_channels:
                self.selected_channel_listbox.addItem(channel)

    def back_to_main(self):
        self.close()  # Close this window