import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

from manual_entry_window import ManualEntryWindow


class EditPropertyWindow(QtWidgets.QWidget):
    def __init__(self, username, reactor_type, reactor_name, selected_channels, database_type):
        super().__init__()
        self.setWindowTitle("Edit Properties")
        self.setGeometry(100, 100, 1200, 600)
        self.username=username
        self.selected_channels = selected_channels
        self.database_type = database_type
        self.selected_channel=""
        self.selected_property=""
        # List of properties
        self.properties = [
            "", "UTS axial", "UTS transverse", "YS axial", "YS transverse",
            "Elongation axial", "Elongation transverse", "Hardness", "Ki axial",
            "Ki transverse", "Density (rho)", "Poisson ratio"
        ]

        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Create horizontal layout for channel frame and property frame
        self.horizontal_layout = QtWidgets.QHBoxLayout()

        # Frame for selected channels
        self.channel_frame = QtWidgets.QFrame(self)
        self.channel_layout = QtWidgets.QVBoxLayout(self.channel_frame)

        self.channel_layout.addWidget(QtWidgets.QLabel("Selected Channels", font=QtGui.QFont("Helvetica", 12)),
                                      alignment=QtCore.Qt.AlignCenter)

        self.selected_channel_listbox = QtWidgets.QListWidget()
        self.selected_channel_listbox.currentRowChanged.connect(self.populate_table_with_selected_channel)
        self.channel_layout.addWidget(self.selected_channel_listbox)

        for channel in selected_channels:
            self.selected_channel_listbox.addItem(channel)

        # Set the channel frame to occupy 10% width
        self.channel_frame.setFixedWidth(120)  # Adjust width as needed
        self.horizontal_layout.addWidget(self.channel_frame)

        # Frame for properties and table
        self.property_frame = QtWidgets.QFrame(self)
        self.property_layout = QtWidgets.QVBoxLayout(self.property_frame)

        self.property_layout.addWidget(QtWidgets.QLabel("Select Property to Edit", font=QtGui.QFont("Helvetica", 12)),
                                       alignment=QtCore.Qt.AlignLeft)

        # Combo box to select properties
        self.property_combo = QtWidgets.QComboBox()
        self.property_combo.addItems(self.properties)
        self.property_combo.currentIndexChanged.connect(self.property_selected)  # Connect the signal to a method
        self.property_layout.addWidget(self.property_combo)

        # Horizontal layout for Add New, Manual, and Import buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        # Add New button
        self.add_new_button = QtWidgets.QPushButton("Add New")
        self.add_new_button.setCheckable(True)  # Make it a toggle button
        self.add_new_button.setFixedSize(100, 30)  # Set the size (width=100, height=30)
        self.add_new_button.clicked.connect(self.toggle_add_options)
        self.button_layout.addWidget(self.add_new_button)

        # Manual button (initially hidden)
        self.manual_button = QtWidgets.QPushButton("Manual")
        self.manual_button.setFixedSize(100, 30)  # Set the size (width=100, height=30)
        self.manual_button.clicked.connect(lambda: self.open_manual_entry(self.username, reactor_type,reactor_name,self.selected_channel, database_type, self.selected_property))
        self.manual_button.hide()  # Hide initially
        self.button_layout.addWidget(self.manual_button)

        # Import button (initially hidden)
        self.import_button = QtWidgets.QPushButton("Import")
        self.import_button.setFixedSize(100, 30)  # Set the size (width=100, height=30)
        self.import_button.clicked.connect(self.import_data)
        self.import_button.hide()  # Hide initially
        self.button_layout.addWidget(self.import_button)

        # Add button layout to the property layout
        self.property_layout.addLayout(self.button_layout)

        # Table to display existing data from the database
        self.table_frame = QtWidgets.QFrame(self.property_frame)
        self.table_layout = QtWidgets.QVBoxLayout(self.table_frame)

        # Define columns for TableView
        self.tree = QtWidgets.QTableWidget()
        self.tree.setColumnCount(24)  # Set the number of columns
        self.tree.setHorizontalHeaderLabels([
            "Channel", "Property", "Value", "Year", "HOY", "Length", "Entry_by", "Entry_Date", "Remark",
            "Cell1", "Cell2", "Cell3", "Cell4", "Cell5", "Cell6", "Cell7", "Cell8", "Cell9", "Cell10",
            "Cell11", "Cell12", "Cell13", "Cell14", "Cell15", "Cell16", "Cell17", "Cell18", "Cell19",
            "Cell20", "Cell21", "Cell22", "Cell23", "Cell24"
        ])
        self.table_layout.addWidget(self.tree)

        self.property_layout.addWidget(self.table_frame)

        self.horizontal_layout.addWidget(self.property_frame)
        self.main_layout.addLayout(self.horizontal_layout)

        # Create footer frame for Back button
        self.footer_frame = QtWidgets.QFrame(self)
        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_frame)

        # Back button
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setFixedSize(80, 30)  # Set smaller size for Back button
        self.back_button.clicked.connect(self.go_back)
        self.footer_layout.addWidget(self.back_button)

        self.main_layout.addWidget(self.footer_frame)

    def go_back(self):
        """Close the current window and go back to the previous window."""
        self.close()

    def toggle_add_options(self):
        """Toggle the visibility of 'Manual' and 'Import' buttons when 'Add New' is clicked."""
        if self.add_new_button.isChecked():
            self.manual_button.show()
            self.import_button.show()
            self.add_new_button.setText("Undo")  # Change button text to Undo
        else:
            self.manual_button.hide()
            self.import_button.hide()
            self.add_new_button.setText("Add New")  # Change button text back to Add New

    def open_manual_entry(self, username, reactor_type, reactor_name, selected_channel, database_type, selected_property):
        """Handle manual entry of properties."""
        if self.selected_property=="":
            QMessageBox.information(self,"Error","Please select the property to be loaded")
        else:
            print("Selected channel is "+selected_channel)
            self.manualEntryWindow=ManualEntryWindow(self, username, reactor_type, reactor_name, selected_channel, database_type, selected_property)
            self.manualEntryWindow.show()
        # Logic for manual entry will be implemented here
        pass

    def import_data(self):
        """Handle import of data."""
        # Logic for import will be implemented here
        pass

    def populate_table(self, channel, property):
        """Fetch data from the database and populate the TableView for the selected channel."""
        if property=="":
            print("No property selected")
        # Check if a channel is selected
        if not channel or not self.database_type:
            return

        conn = sqlite3.connect('iphwr_analysis.db')
        cursor = conn.cursor()

        # Define the columns for the table
        headers = [
            'Channel ID', 'Property Name', 'Year', 'HOY', 'Length', 'Entry By', 'Entry Date', 'Remark',
            'Cell1', 'Cell2', 'Cell3', 'Cell4', 'Cell5', 'Cell6', 'Cell7', 'Cell8', 'Cell9', 'Cell10',
            'Cell11', 'Cell12', 'Cell13', 'Cell14', 'Cell15', 'Cell16', 'Cell17', 'Cell18', 'Cell19',
            'Cell20', 'Cell21', 'Cell22', 'Cell23', 'Cell24'
        ]

        # Set column count and headers
        self.tree.setColumnCount(len(headers))
        self.tree.setHorizontalHeaderLabels(headers)

        # Clear the current table
        self.tree.setRowCount(0)  # Clear existing data in the table

        # Build the SQL query based on whether a property is selected or not
        if property == "":
            print("No specific property selected, showing all properties")
            query = "SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties WHERE channel_id=?"
            cursor.execute(query, (channel,))
        else:
            query = "SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties WHERE channel_id=? AND property_name=?"
            cursor.execute(query, (channel, property))
        rows = cursor.fetchall()

        # Populate the table with fetched data
        for row in rows:
            row_position = self.tree.rowCount()
            self.tree.insertRow(row_position)
            for column_index, item in enumerate(row):
                self.tree.setItem(row_position, column_index, QtWidgets.QTableWidgetItem(str(item)))

        conn.close()
    

    def populate_table_with_selected_channel(self, row):
        """Populate the table with properties of the selected channel."""
        if row < 0:  # If no valid channel is selected
            return
        selected_channel = self.selected_channels[row]
        self.selected_channel=selected_channel
        if self.selected_channel=="":
            QMessageBox.information("Please select a channel to edit")
        else:
            print("Before table is populated ",self.selected_property)
            self.populate_table(selected_channel, self.selected_property)
            
    def property_selected(self):
        self.selected_property = self.property_combo.currentText()  # Get the currently selected property
        print(f"Selected Property: {self.selected_property}")  # Print the selected property
        self.populate_table(self.selected_channel,self.selected_property)


#if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    window = EditPropertyWindow("Admin","220_IPHWR", "RAPS-1", ["A08","A09"], "Mechanical")
#    window.show()
#    sys.exit(app.exec_())