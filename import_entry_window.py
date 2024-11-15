import sqlite3
from PyQt5.QtWidgets import (QMessageBox, QFileDialog, QPushButton, QDialog, QVBoxLayout, 
                             QLabel, QLineEdit, QFormLayout, QHBoxLayout)
from PyQt5.QtCore import QDateTime
from datetime import datetime
import pandas as pd  # Assuming pandas is installed for Excel handling

class ImportEntryWindow(QDialog):
    """A custom dialog for importing data."""

    def __init__(self, reactor_name, reactor_type, username, selected_channel, selected_property, database_type, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"Import Entry for Channel {selected_channel} for {selected_property}")
        #self.import_button = QPushButton("", self)
        self.setGeometry(100, 100, 400, 300)

        # Initialize input fields
        self.year_input = QLineEdit()
        self.hoy_input = QLineEdit()
        self.length_input = QLineEdit()
        self.entry_by_input = QLineEdit(username)  # Automatically fill with the username
        self.entry_date_input = QLineEdit(datetime.now().strftime("%d-%m-%Y"))  # Current date as default
        self.remark_input = QLineEdit()
        self.reactor_type_input = QLineEdit(reactor_type)
        self.reactor_name_input = QLineEdit(reactor_name)

        # Initialize database_type
        self.database_type = database_type  # Make sure database_type is passed during initialization

        # Store selected_channel and selected_property for later use
        self.selected_channel = selected_channel
        self.selected_property = selected_property

        # Create form layout for user inputs
        form_layout = QFormLayout()
        form_layout.addRow("Year:", self.year_input)
        form_layout.addRow("HOY:", self.hoy_input)
        form_layout.addRow("Length:", self.length_input)
        form_layout.addRow("Entry by:", self.entry_by_input)
        form_layout.addRow("Entry date:", self.entry_date_input)
        form_layout.addRow("Remark:", self.remark_input)
        form_layout.addRow("Reactor type:", self.reactor_type_input)
        form_layout.addRow("Reactor name:", self.reactor_name_input)

        # Create buttons for dialog
        button_layout = QHBoxLayout()
        self.select_file_button = QPushButton("Select File")
        self.select_file_button.clicked.connect(self.select_file)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.import_data)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.select_file_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        # Add form and button layout to main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.selected_file = None

    def select_file(self):
        """Handle file selection."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.selected_file = file_path
            QMessageBox.information(self, "File Selected", f"File selected: {file_path}")

    def import_data(self):
        """Import data from the selected Excel file into the database."""
        # Collect the form data
        form_data = self.get_form_data()

        # Ensure we have selected a file and filled required fields
        if not self.selected_file:
            QMessageBox.warning(self, "Warning", "Please select an Excel file to import!")
            return
        
        if not form_data["year"] or not form_data["hoy"]:
            QMessageBox.warning(self, "Warning", "Year and HOY are required fields!")
            return

        try:
            # Read the Excel file
            df = pd.read_excel(self.selected_file)

            # Process the data and save to database
            self.save_to_database(form_data, df)
            QMessageBox.information(self, "Success", "Data imported successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import data: {str(e)}")

    def save_to_database(self, form_data, df):
        """Save the data from the Excel file to the database."""
        conn = sqlite3.connect('iphwr_analysis.db')
        cursor = conn.cursor()

        for index, row in df.iterrows():
            # Ensure data types are correct before inserting
            channel_id = str(form_data["selected_channel"])  # Ensure it's a string
            property_name = str(form_data["selected_property"])  # Ensure it's a string
            database_type = str(form_data["database_type"])  # Ensure it's a string
            year = str(form_data["year"])  # Ensure it's a string
            hoy = str(form_data["hoy"])  # Ensure it's a string
            length = str(form_data["length"])  # Ensure it's a string
            entry_by = str(form_data["entry_by"])  # Ensure it's a string
            entry_date = str(form_data["entry_date"])  # Ensure it's a string
            remark = str(form_data["remark"])  # Ensure it's a string
            reactor_type = str(form_data["reactor_type"])  # Ensure it's a string
            reactor_name = str(form_data["reactor_name"])  # Ensure it's a string

            # Prepare your insert statement here
            cursor.execute('''INSERT INTO properties (channel_id, property_name, database_type, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                            Reactor_Type, Reactor_Name)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (channel_id, property_name, database_type, year, hoy, length, 
                        entry_by, entry_date, remark, reactor_type, reactor_name))

        conn.commit()
        conn.close()

    def get_form_data(self):
        """Return the data entered by the user and the selected file path."""
        return {
            "year": self.year_input.text(),
            "hoy": self.hoy_input.text(),
            "length": self.length_input.text(),
            "entry_by": self.entry_by_input.text(),
            "entry_date": self.entry_date_input.text(),
            "remark": self.remark_input.text(),
            "reactor_type": self.reactor_type_input.text(),
            "reactor_name": self.reactor_name_input.text(),
            "selected_channel": self.selected_channel,
            "selected_property": self.selected_property,
            "database_type": self.database_type,  # This now exists and will be passed
            "file": self.selected_file
        }  
