import sys
import sqlite3
<<<<<<< HEAD
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QScrollArea, QWidget)
from datetime import datetime
=======
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QScrollArea, QWidget, 
                             QMessageBox)
import datetime  # Import the datetime module

>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a

class ManualEntryWindow(QDialog):

    def __init__(self, parent, username, reactor_type, reactor_name, selected_channel, database_type, selected_property):
        super().__init__(parent)
        self.username = username
        self.selected_channel = selected_channel
        self.database_type = database_type
        self.selected_property = selected_property
        self.setWindowTitle(f"Manual Entry for Channel {self.selected_channel} for {self.selected_property}")
        self.setGeometry(100, 100, 400, 600)

        # Create layout
        layout = QVBoxLayout()

        # Create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a widget for the scroll area
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        # Create layout for scrollable widget
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

<<<<<<< HEAD
=======
        # Check and add missing columns in the database
        self.update_database_schema()
        # Get the current date in the format YYYY-MM-DD
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
        # Create entry fields with prefilled values
        self.entries = {}
        fields = {
            "Year": "",
            "HOY": "",
            "Length": "",
            "Entry_by": self.username,
<<<<<<< HEAD
            "Entry_Date": datetime.now().strftime("%d-%m-%y"),  # Set default to current date
            "Remark": "",
=======
            "Entry_Date": current_date,
            "Remark": "Test entry",
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
            "Reactor_Type": reactor_type,
            "Reactor_Name": reactor_name,
        }

        for field, default_value in fields.items():
            label = QLabel(field)
            self.scroll_layout.addWidget(label)
            entry = QLineEdit()
            entry.setText(default_value)  # Set prefilled value
            self.scroll_layout.addWidget(entry)
            self.entries[field] = entry

        # Add cell entries with position names (for 100 cells and positions)
        for i in range(1, 101):
            label = QLabel(f"Cell{i}")
            self.scroll_layout.addWidget(label)
            entry = QLineEdit()  # Input for the Cell value
            self.scroll_layout.addWidget(entry)
            self.entries[f"Cell{i}"] = entry
            
            position_label = QLabel(f"Position{i}")
            self.scroll_layout.addWidget(position_label)
            position_entry = QLineEdit()  # Input for the Position value
            self.scroll_layout.addWidget(position_entry)
            self.entries[f"Position{i}"] = position_entry  # Store position input fields

        # Add the Save button
        save_button = QPushButton("Save")
        self.scroll_layout.addWidget(save_button)
        save_button.clicked.connect(self.save_manual_entry)  # Connect the button to the save method

        # Add the scroll area to the main layout
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def save_manual_entry(self):
        # Collect the data from the entries
        data = {field: entry.text() for field, entry in self.entries.items()}

        # Ensure we have valid data before saving
        if not data["Year"] or not data["HOY"]:
            QMessageBox.warning(self, "Warning", "Year and HOY are required fields!")
            return

        conn = sqlite3.connect('iphwr_analysis.db')
        cursor = conn.cursor()

        # Check for duplicate entries for the same channel, Year, HOY, and property
        cursor.execute('''SELECT COUNT(*) FROM properties 
                          WHERE channel_id = ? AND Year = ? AND HOY = ? AND property_name = ?''', 
                       (self.selected_channel, data["Year"], data["HOY"], self.selected_property))
        result = cursor.fetchone()

        if result[0] > 0:
            # Entry already exists, show a warning message
            QMessageBox.warning(self, "Warning", "An entry already exists for this Channel, Year, HOY, and Property!")
            conn.close()
            return

        # Insert into the properties table with all required columns, including positions for 100 cells
        cursor.execute(f'''INSERT INTO properties (channel_id, property_name, database_type, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                            Reactor_Type, Reactor_Name, {", ".join([f"Cell{i}" for i in range(1, 101)])}, {", ".join([f"Position{i}" for i in range(1, 101)])})
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                {", ".join(["?" for _ in range(1, 201)])})''',
                    (self.selected_channel, self.selected_property, self.database_type, data["Year"], data["HOY"], data["Length"], data["Entry_by"], data["Entry_Date"], data["Remark"],
                        data["Reactor_Type"], data["Reactor_Name"], 
                        *(data[f"Cell{i}"] for i in range(1, 101)), *(data[f"Position{i}"] for i in range(1, 101)) ))

        conn.commit()
        conn.close()
        QMessageBox.information(self, "Info", "Manual entries added successfully!")
        self.accept()
