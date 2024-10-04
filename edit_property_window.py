import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore


class EditPropertyWindow(QtWidgets.QWidget):
    def __init__(self, selected_channels, database_type):
        super().__init__()
        self.setWindowTitle("Edit Properties")
        self.setGeometry(100, 100, 1200, 600)

        self.selected_channels = selected_channels
        self.database_type = database_type

        # List of properties
        self.properties = [
            "UTS axial", "UTS transverse", "YS axial", "YS transverse",
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
        self.property_layout.addWidget(self.property_combo)

        # Horizontal layout for Add New, Manual, and Import buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        self.add_new_button = QtWidgets.QPushButton("Add New")
        self.add_new_button.setCheckable(True)  # Make it a toggle button
        self.add_new_button.clicked.connect(self.toggle_add_options)
        self.button_layout.addWidget(self.add_new_button)

        # Manual and Import buttons (initially hidden)
        self.manual_button = QtWidgets.QPushButton("Manual")
        self.manual_button.clicked.connect(self.open_manual_entry)
        self.import_button = QtWidgets.QPushButton("Import")
        self.import_button.clicked.connect(self.import_data)

        # Hide the manual and import buttons initially
        self.manual_button.hide()
        self.import_button.hide()

        self.button_layout.addWidget(self.manual_button)
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
            "Channel", "Property", "Value", "Year", "HOY", "Length", "Entryby", "Entry_Date", "Remark",
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

        # Populate the table initially
        self.populate_table()

        # Automatically select the first channel's properties in the table
        if self.selected_channels:
            self.populate_table_with_selected_channel()

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

    def open_manual_entry(self):
        """Handle manual entry of properties."""
        # Logic for manual entry will be implemented here
        pass

    def import_data(self):
        """Handle import of data."""
        # Logic for import will be implemented here
        pass

    def save_new_properties(self):
        """Save new properties to the database."""
        # Logic for saving properties will be implemented here
        pass

    def populate_table(self):
        """Fetch data from the database and populate the TableView."""
        conn = sqlite3.connect('iphwr_analysis.db')
        cursor = conn.cursor()

        # Clear the current table
        self.tree.setRowCount(0)  # Clear existing data in the table

        # Fetch the data for the selected channels and database type
        for channel in self.selected_channels:
            cursor.execute('''SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                                     Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10,
                                     Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19,
                                     Cell20, Cell21, Cell22, Cell23, Cell24
                              FROM properties
                              WHERE channel_id = ? AND database_type = ?''',
                           (channel, self.database_type))
            rows = cursor.fetchall()

            # Populate the table with fetched data
            for row in rows:
                row_position = self.tree.rowCount()
                self.tree.insertRow(row_position)
                for column_index, item in enumerate(row):
                    self.tree.setItem(row_position, column_index, QtWidgets.QTableWidgetItem(str(item)))

        conn.close()

    def populate_table_with_selected_channel(self):
        """Populate the table with properties of the first selected channel."""
        if not self.selected_channels:
            return

        first_channel = self.selected_channels[0]
        self.selected_channel_listbox.setCurrentRow(0)

        # Fetch properties for the first selected channel
        self.populate_table()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditPropertyWindow(["Channel1", "Channel2"], "Type A")
    window.show()
    sys.exit(app.exec_())
