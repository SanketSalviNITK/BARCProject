import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QScrollArea, QWidget, 
                             QMessageBox)

class ManualEntryWindow(QDialog):
    def __init__(self, parent, username, reactor_type, reactor_name, selected_channel, database_type, selected_property):
        super().__init__(parent)
        self.username = username  # Store username if needed
        self.selected_channel = selected_channel
        self.database_type = database_type
        self.selected_property = selected_property
        self.setWindowTitle("Manual Entry for Channel "+self.selected_channel+" for "+self.selected_property)
        self.setGeometry(100, 100, 400, 600)
        print(self.username, reactor_type, reactor_name, self.selected_channel,self.database_type,self.selected_property)

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

        # Check and add missing columns in the database
        self.update_database_schema()

        # Create entry fields with prefilled values
        self.entries = {}
        fields = {
            "Year": "2023",
            "HOY": "100",
            "Length": "10.5",
            "Entry_by": self.username,
            "Entry_Date": "2023-10-04",
            "Remark": "Test entry",
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

        # Add cell entries
        for i in range(1, 25):
            label = QLabel(f"Cell{i}")
            self.scroll_layout.addWidget(label)
            entry = QLineEdit()
            entry.setText(f"Test Value {i}")  # Prefill with test values
            self.scroll_layout.addWidget(entry)
            self.entries[f"Cell{i}"] = entry

        # Create Save and Cancel buttons
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_manual_entry)
        self.scroll_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        self.scroll_layout.addWidget(cancel_button)

        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def update_database_schema(self):
        # This function can be implemented to ensure the schema is as expected,
        # but since we are dropping and creating the table in the previous function,
        # we can leave this empty or use it to add further checks in the future.
        pass

    def save_manual_entry(self):
        # Collect the data from the entries
        data = {field: entry.text() for field, entry in self.entries.items()}

        # Ensure we have valid data before saving
        if not data["Year"] or not data["HOY"]:
            QMessageBox.warning(self, "Warning", "Year and HOY are required fields!")
            return

        conn = sqlite3.connect('iphwr_analysis.db')
        cursor = conn.cursor()

        # Insert manual entries for each selected channel (using placeholder channel for demonstration)
        channel = self.selected_channel  # Placeholder channel
        property_name = self.selected_property  # Placeholder property name

        # Insert into the properties table with all required columns
        cursor.execute('''INSERT INTO properties (channel_id, property_name, database_type, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                        Reactor_Type, Reactor_Name,
                        Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10,
                        Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20,
                        Cell21, Cell22, Cell23, Cell24)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (channel, property_name, self.database_type, data["Year"], data["HOY"], data["Length"], data["Entry_by"], data["Entry_Date"], data["Remark"],
                    data["Reactor_Type"], data["Reactor_Name"],
                    data["Cell1"], data["Cell2"], data["Cell3"], data["Cell4"], data["Cell5"], data["Cell6"], data["Cell7"], data["Cell8"],
                    data["Cell9"], data["Cell10"], data["Cell11"], data["Cell12"], data["Cell13"], data["Cell14"], data["Cell15"],
                    data["Cell16"], data["Cell17"], data["Cell18"], data["Cell19"], data["Cell20"], data["Cell21"], data["Cell22"],
                    data["Cell23"], data["Cell24"]))

        conn.commit()
        conn.close()
        QMessageBox.information(self, "Info", "Manual entries added successfully!")
        self.accept()
