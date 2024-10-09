import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                             QPushButton, QTextEdit, QComboBox, QVBoxLayout, 
                             QWidget, QMessageBox, QHBoxLayout, QGroupBox)
from PyQt5.QtCore import Qt

class FetchWindow(QWidget):
    def __init__(self, parent=None):
        super(FetchWindow, self).__init__(parent)
        self.setWindowTitle("Database Entry Application")
        self.setGeometry(100, 100, 600, 500)

        layout = QHBoxLayout()  # Use a horizontal layout for left and right sections

        # Left Layout for Parameter Selection
        left_layout = QVBoxLayout()
        left_group = QGroupBox("Parameter Selection", self)
        left_group.setLayout(left_layout)

        # Reactor Type Dropdown
        self.reactor_category_var = QComboBox(self)
        self.reactor_category_var.addItems(["Select Reactor Category", "220 IPHWR", "540 IPHWR", "700 IPHWR"])
        self.reactor_category_var.currentIndexChanged.connect(self.update_reactor_names)
        left_layout.addWidget(QLabel("Select Reactor Type:"))
        left_layout.addWidget(self.reactor_category_var)

        # Reactor Name Dropdown (Dependent on Reactor Category)
        left_layout.addWidget(QLabel("Select Reactor Name:"))
        self.reactor_name_var = QComboBox(self)
        left_layout.addWidget(self.reactor_name_var)
        self.reactor_name_var.currentIndexChanged.connect(self.print_selected_reactor_name)


        # Channel ID Entry
        self.channel_var = QLineEdit(self)
        self.channel_var.setPlaceholderText("Enter Channel ID")
        left_layout.addWidget(QLabel("Enter Channel ID:"))
        left_layout.addWidget(self.channel_var)

        # Database Type Dropdown
        self.db_type_var = QComboBox(self)
        self.db_type_var.addItems(self.get_database_types())
        self.db_type_var.currentIndexChanged.connect(self.update_path)
        left_layout.addWidget(QLabel("Select Database Type:"))
        left_layout.addWidget(self.db_type_var)

        # Property Name Dropdown
        self.property_var = QComboBox(self)
        self.property_var.addItems(self.get_property_names())
        self.property_var.currentIndexChanged.connect(self.update_path)
        left_layout.addWidget(QLabel("Select Property Name:"))
        left_layout.addWidget(self.property_var)

        # Cell Number Dropdown
        self.cell_var = QComboBox(self)
        self.cell_var.addItems([str(i) for i in range(1, 25)])
        left_layout.addWidget(QLabel("Select Cell Number:"))
        left_layout.addWidget(self.cell_var)

        # Fetch Button
        self.fetch_button = QPushButton("Fetch Data", self)
        self.fetch_button.clicked.connect(self.fetch_and_display_data)
        left_layout.addWidget(self.fetch_button)

        layout.addWidget(left_group)  # Add the left group to the main layout

        # Right Layout for Result Display
        right_layout = QVBoxLayout()
        right_group = QGroupBox("Result", self)
        right_group.setLayout(right_layout)

        # Path Label
        self.path_label = QLabel("Path: ", self)
        right_layout.addWidget(self.path_label)

        # Data Display TextEdit
        self.data_display = QTextEdit(self)
        right_layout.addWidget(self.data_display)

        layout.addWidget(right_group)  # Add the right group to the main layout

        self.setLayout(layout)

    def update_path(self):
        db_type = self.db_type_var.currentText()
        property_name = self.property_var.currentText()
        channel_id = self.channel_var.text()
        reactor_type = self.reactor_category_var.currentText()
        reactor_name = self.reactor_name_var.currentText()
        
        # Construct path message
        path_message = f"Path: Channel ID = {channel_id}, Database Type = {db_type}, Property = {property_name}, Reactor Type = {reactor_type}, Reactor Name = {reactor_name}"
        self.path_label.setText(path_message)

    def update_reactor_names(self):
        reactor_category = self.reactor_category_var.currentText()
        self.reactor_name_var.clear()  # Clear the reactor names dropdown before adding new options
        self.reactor_type = reactor_category
        
        # Update based on selected reactor category
        if reactor_category == "220 IPHWR":
            reactor_names = ["RAPS-1", "RAPS-2", "RAPS-3", "RAPS-4",
                             "RAPS-5", "RAPS-6", "MAPS-1", "MAPS-2",
                             "KAPS-1", "KAPS-2", "KGS-1", "KGS-2",
                             "KGS-3", "KGS-4", "NAPS-1", "NAPS-2"]
        elif reactor_category == "540 IPHWR":
            reactor_names = ["TAPS-1", "TAPS-2"]
        elif reactor_category == "700 IPHWR":
            reactor_names = ["KAPS-3", "KAPS-4", "RAPS-7", "RAPS-8", "KGS-5", "KGS-6"]
        else:
            reactor_names = ["Select Reactor Name"]
        
        self.reactor_name_var.addItems(reactor_names)
    def print_selected_reactor_name(self):
        # Get the selected reactor name
        self.reactor_name = self.reactor_name_var.currentText()

    def fetch_data(self, channel_id, database_type, property_name, reactor_type, reactor_name, cell_number):
        try:
            with sqlite3.connect('iphwr_analysis.db') as conn:
                cursor = conn.cursor()
                query = f"""SELECT channel_id, property_name, database_type, reactor_type, reactor_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell{cell_number} 
                            FROM properties WHERE channel_id = ? AND property_name = ? AND reactor_type = ? AND reactor_name = ?"""
                params = [channel_id, property_name, reactor_type, reactor_name]
                cursor.execute(query, params)
                rows = cursor.fetchall()

                if rows:
                    return rows
                else:
                    return []

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred while fetching data: {str(e)}")
            return []

    def fetch_and_display_data(self):
        channel_id = self.channel_var.text()
        database_type = self.db_type_var.currentText()
        property_name = self.property_var.currentText()
        cell_number = int(self.cell_var.currentText())

        if channel_id == "" or database_type == "Select Database Type" or property_name == "Select Property Name":
            QMessageBox.warning(self, "Warning", "Please select valid options.")
            return

        rows = self.fetch_data(channel_id, database_type, property_name, self.reactor_type, self.reactor_name, cell_number)
        self.data_display.clear()

        if not rows:
            self.data_display.setPlainText("No data found for the selected options.")
            return

        for row in rows:
            formatted_row = ', '.join(map(str, row))
            self.data_display.append(formatted_row)

    def get_database_types(self):
        return ["Select Database Type", "Mechanical Properties", "Chemical", "Thermal & Electrical", "Reactor Flux"]

    def get_property_names(self):
        return [
            "UTS axial", 
            "UTS transverse",
            "Yield Strength axial",
            "Yield Strength transverse",
            "Elongation axial",
            "Elongation transverse",
            "Hardness",
            "Ki axial",
            "Ki transverse",
            "Density (rho)",
            "Poisson ratio"
        ]

# Main Application Window with "Fetch" button
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application Window")
        self.setGeometry(100, 100, 800, 600)

        # Fetch Button in Main Window
        fetch_button = QPushButton("Fetch", self)
        fetch_button.setGeometry(50, 50, 200, 50)
        fetch_button.clicked.connect(self.open_fetch_window)

    def open_fetch_window(self):
        self.fetch_window = FetchWindow(self)
        self.fetch_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
