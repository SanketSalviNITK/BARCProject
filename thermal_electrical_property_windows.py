import sys
import sqlite3
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
from footer_util import add_company_footer
from manual_entry_window import ManualEntryWindow
from PyQt5.QtWidgets import QPushButton,QFileDialog

class EditThermalElectricalPropertyWindow(QtWidgets.QWidget):
    def __init__(self, username, reactor_type, reactor_name, selected_channels, database_type):
        super().__init__()
        # Your initialization code here
        self.setWindowTitle("Edit Thermal & Electrical Properties")
        self.setGeometry(100, 100, 1200, 600)

        self.username = username
        self.reactor_type = reactor_type
        self.reactor_name = reactor_name
        self.selected_channels = selected_channels
        self.database_type = database_type
        self.selected_channel=""
        self.selected_property=""

        # Database connection
        self.conn = sqlite3.connect("iphwr_analysis.db")
        self.cursor = self.conn.cursor()

        self.properties =[
            "Specific heat","Thermal Conductivity"," Electrical conductivity"


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
        self.channel_frame.setFixedHeight(800)
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

        # Horizontal layout for Add New, Manual, Import, and Refresh buttons
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
        self.manual_button.clicked.connect(lambda: self.open_manual_entry(self.username, reactor_type, reactor_name,
                                                                          self.selected_channel, database_type, self.selected_property))
        self.manual_button.hide()  # Hide initially
        self.button_layout.addWidget(self.manual_button)

        # Import button (initially hidden)
        self.import_button = QtWidgets.QPushButton("Import")
        self.import_button.setFixedSize(100, 30)  # Set the size (width=100, height=30)
        self.import_button.clicked.connect(self.import_data)
        self.import_button.hide()  # Hide initially
        self.button_layout.addWidget(self.import_button)

        # Add the Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFixedSize(100, 30)  # Set the size (width=100, height=30)
        self.refresh_button.clicked.connect(self.refresh_table)  # Connect to refresh function
        self.button_layout.addWidget(self.refresh_button)

        # Add button layout to the property layout
        self.property_layout.addLayout(self.button_layout)

        # Table to display existing data from the database
        self.table_frame = QtWidgets.QFrame(self.property_frame)
        self.table_layout = QtWidgets.QVBoxLayout(self.table_frame)

        # Define columns for TableView
        self.tree = QtWidgets.QTableWidget()
        self.tree.setColumnCount(24)  # Set the number of columns
        self.tree.setHorizontalHeaderLabels([
            "Channel", "Property", "Year", "HOY", "Length", "Entry_by", "Entry_Date", "Remark",
            "Cell1", "Cell2", "Cell3", "Cell4", "Cell5", "Cell6", "Cell7", "Cell8", "Cell9", "Cell10",
            "Cell11", "Cell12", "Cell13", "Cell14", "Cell15", "Cell16", "Cell17", "Cell18", "Cell19",
            "Cell20", "Cell21", "Cell22", "Cell23", "Cell24"
        ])
        self.table_layout.addWidget(self.tree)

        self.property_layout.addWidget(self.table_frame)

        self.horizontal_layout.addWidget(self.property_frame)
        self.main_layout.addLayout(self.horizontal_layout)
        #add_company_footer(self.main_layout)

        # Create footer frame for Back button
        self.footer_frame = QtWidgets.QFrame(self)
        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_frame)

        # Back button
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setFixedSize(80, 30)  # Set smaller size for Back button
        self.back_button.clicked.connect(self.go_back)
        self.footer_layout.addWidget(self.back_button)
        self.main_layout.addWidget(self.footer_frame)

        # Add company footer to the main layout
        add_company_footer(self.main_layout)

    def refresh_table(self):
        """Refresh the table by re-populating it with the current channel and property."""
        self.populate_table(self.selected_channel)  # Repopulate with the same selected channel and property 


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
        if len(selected_channel) == 0:
            QMessageBox.information(self, "Info", "Please select the channel to be edited")
        else:
            print("Selected channel is " + selected_channel)
            self.manualEntryWindow = ManualEntryWindow(self, username, reactor_type, reactor_name, selected_channel,
                                                       database_type, selected_property)
            self.manualEntryWindow.show()
        pass

    def import_data(self):
        """Handle import of data from an Excel file."""
        try:
            # Open file dialog to select an Excel file
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")

            # If a file is selected
            if file_path:
                # Read the Excel file using pandas
                df = pd.read_excel(file_path, engine='openpyxl')  # 'openpyxl' engine used for .xlsx files

                # You can process the DataFrame (df) here or populate your table/tree
                self.populate_table_from_dataframe(df)

                # Inform the user that the file was successfully imported
                QMessageBox.information(self, "Success", f"Data imported successfully from {file_path}")

        except Exception as e:
            # Handle any errors that occur during the import process
            QMessageBox.critical(self, "Error", f"Failed to import data: {e}")

    def populate_table_from_dataframe(self, df):
        """Populate your table or UI elements using the imported DataFrame."""
        # Example: Populate the QTableWidget from the DataFrame (assuming self.tree is a QTableWidget)
        self.tree.setRowCount(0)  # Clear the table first

        # Set the number of rows and columns based on the DataFrame
        self.tree.setRowCount(len(df.index))
        self.tree.setColumnCount(len(df.columns))

        # Set the headers (optional)
        self.tree.setHorizontalHeaderLabels(df.columns)

        # Populate the table with data from the DataFrame
        for row_idx, row_data in df.iterrows():
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tree.setItem(row_idx, col_idx, item)

    def populate_table(self, channel):
            """Fetch data from the database and populate the TableView for the selected channel."""
            if not channel or not self.database_type or not self.property_combo.currentText():
                return

            conn = sqlite3.connect('iphwr_analysis.db')
            cursor = conn.cursor()

            # Define the columns for the table
            headers = [
                'Channel ID', 'Property Name', 'Year', 'HOY', 'Length', 'Entry By', 'Entry Date', 'Remark',
                'Cell1 (Pos 0-250 m)', 'Cell2 (Pos 251-500 m)', 'Cell3 (Pos 501-750 m)',
                'Cell4 (Pos 751-1000 m)', 'Cell5 (Pos 1001-1250 m)', 'Cell6 (Pos 1251-1500 m)',
                'Cell7 (Pos 1501-1750 m)', 'Cell8 (Pos 1751-2000 m)', 'Cell9 (Pos 2001-2250 m)',
                'Cell10 (Pos 2251-2500 m)', 'Cell11 (Pos 2501-2750 m)', 'Cell12 (Pos 2751-3000 m)',
                'Cell13 (Pos 3001-3250 m)', 'Cell14 (Pos 3251-3500 m)', 'Cell15 (Pos 3501-3750 m)',
                'Cell16 (Pos 3751-4000 m)', 'Cell17 (Pos 4001-4250 m)', 'Cell18 (Pos 4251-4500 m)',
                'Cell19 (Pos 4501-4750 m)', 'Cell20 (Pos 4751-5000 m)', 'Cell21 (Pos 5001-5250 m)',
                'Cell22 (Pos 5251-5500 m)', 'Cell23 (Pos 5501-5750 m)', 'Cell24 (Pos 5751-6000 m)',
                'Actions'
            ]

            self.tree.setColumnCount(len(headers))
            self.tree.setHorizontalHeaderLabels(headers)
            self.tree.setRowCount(0)  # Clear existing data in the table

            # Customize header
            header = self.tree.horizontalHeader()
            header.setStyleSheet("QHeaderView::section { background-color: #2E8BFF; color: white; font-weight: bold; }")  # Blue background, white text
            header.setFont(QtGui.QFont("Arial", 10))  # Change font and size

            cursor.execute(
                """SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10,
                Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19,
                Cell20, Cell21, Cell22, Cell23, Cell24
                FROM properties
                WHERE channel_id = ? AND property_name = ?""", (channel, self.selected_property)
            )

            for row_number, row_data in enumerate(cursor.fetchall()):
                self.tree.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(data))
                    item.setFont(QtGui.QFont("Arial", 10))  # Set font for each item
                    item.setTextAlignment(QtCore.Qt.AlignCenter)  # Center align text
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Set as non-editable initially
                    self.tree.setItem(row_number, column_number, item)

                    # Apply alternating row colors
                    if row_number % 2 == 0:
                        item.setBackground(QtGui.QColor(240, 240, 240))  # Light gray background for even rows
                    else:
                        item.setBackground(QtGui.QColor(255, 255, 255))  # White background for odd rows

                # Create Edit and Delete buttons for each row
                edit_button = QtWidgets.QPushButton("Edit")
                delete_button = QtWidgets.QPushButton("Delete")

                # Set fixed sizes for the buttons
                edit_button.setFixedWidth(50)
                delete_button.setFixedWidth(60)

                # Connect edit and delete buttons
                edit_button.clicked.connect(lambda checked, r=row_number: self.edit_row(r))
                delete_button.clicked.connect(lambda checked, r=row_number: self.delete_row(r))

                # Add the buttons to the table
                button_widget = QtWidgets.QWidget()
                layout = QtWidgets.QHBoxLayout(button_widget)
                layout.addWidget(edit_button)
                layout.addWidget(delete_button)
                layout.setAlignment(QtCore.Qt.AlignCenter)
                self.tree.setCellWidget(row_number, len(row_data), button_widget)

            # Set the height for all rows
            for i in range(self.tree.rowCount()):
                self.tree.setRowHeight(i, 60)  # Adjust the height as per your requirement (e.g., 40 pixels)

            conn.close()

    def property_selected(self, index):
        """Handle selection of a property from the combo box."""
        if index < 0 or index >= len(self.properties):
            return  # Ensure the index is valid
        self.selected_property = self.properties[index]
        self.populate_table(self.selected_channel)

    def populate_table_with_selected_channel(self, index):
        """Handle selection of a channel from the list box."""
        if index < 0:
            return  # No valid selection
        self.selected_channel = self.selected_channel_listbox.item(index).text()
        self.populate_table(self.selected_channel)

    def delete_row(self, row):

        """Delete a selected row from the database."""
        channel_id = self.tree.item(row, 0).text()  # Assuming channel_id is in the first column
        property_name = self.tree.item(row, 1).text()  # Assuming property_name is in the second column

        # Prompt confirmation for deletion
        confirm = QMessageBox.question(self, 'Delete Row',
                                    "Are you sure you want to delete this row?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            try:
                # Connect to the database
                conn = sqlite3.connect('iphwr_analysis.db')
                cursor = conn.cursor()

                # Execute SQL command to delete only the specified row
                cursor.execute("DELETE FROM properties WHERE channel_id = ? AND property_name = ?",
                            (channel_id, property_name))
                conn.commit()
                conn.close()

                # Remove row from the table in the UI
                self.tree.removeRow(row)
                QMessageBox.information(self, "Success", "Row deleted successfully!")

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete row: {e}")

    def edit_row(self, row):
        """Edit the selected row."""
        if row < 0:
            return

        # Get the channel_id or primary identifier for the selected row
        channel_id = self.tree.item(row, 0).text()
        property_name = self.tree.item(row, 1).text()  # Assuming 2nd column is property_name

        # Loop through the columns and make them editable except for Entry_by (column 5) and Entry_Date (column 6)
        for column in range(2, self.tree.columnCount() - 1):  # Skipping channel_id and buttons
            if column not in [5, 6]:  # Skip Entry_by (column 5) and Entry_Date (column 6)
                item = self.tree.item(row, column)
                if item:
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)  # Enable editing for the column

        # Add a "Save" button to save the changes
        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_edited_row(row, channel_id, property_name))  # Connect to save method

        # Replace the current Edit/Delete buttons with a Save button
        self.tree.setCellWidget(row, self.tree.columnCount() - 1, save_button)


    def save_edited_row(self, row, channel_id, property_name):
            """Save the changes made to the selected row back to the database."""
            # Collect the new values from the row
            new_values = []
            for column in range(2, self.tree.columnCount() - 1):  # Skip channel_id and last column (buttons)
                item = self.tree.item(row, column)
                if item:
                    new_values.append(item.text())

            # Prepare the SQL query to update the database
            update_query = """
            UPDATE properties
            SET Year = ?, HOY = ?, Length = ?, Entry_by = ?, Entry_Date = ?, Remark = ?,
                Cell1 = ?, Cell2 = ?, Cell3 = ?, Cell4 = ?, Cell5 = ?, Cell6 = ?, Cell7 = ?, 
                Cell8 = ?, Cell9 = ?, Cell10 = ?, Cell11 = ?, Cell12 = ?, Cell13 = ?, Cell14 = ?, 
                Cell15 = ?, Cell16 = ?, Cell17 = ?, Cell18 = ?, Cell19 = ?, Cell20 = ?, Cell21 = ?, 
                Cell22 = ?, Cell23 = ?, Cell24 = ?
            WHERE channel_id = ? AND property_name = ?"""

            try:
                # Update the database with new values
                conn = sqlite3.connect('iphwr_analysis.db')
                cursor = conn.cursor()
                cursor.execute(update_query, (*new_values, channel_id, property_name))  # Pass new values and identifiers
                conn.commit()
                conn.close()

                # Inform the user that the data has been saved
                QMessageBox.information(self, "Success", "Row updated successfully!")

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Failed to update row: {e}")

            # Reset the Edit/Delete buttons back
            self.reset_buttons(row)


    def reset_buttons(self, row):
        """Reset the buttons for the row after editing."""
        edit_button = QtWidgets.QPushButton("Edit")
        delete_button = QtWidgets.QPushButton("Delete")
        edit_button.clicked.connect(lambda checked, r=row: self.edit_row(r))
        delete_button.clicked.connect(lambda checked, r=row: self.delete_row(r))

        button_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(button_widget)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.tree.setCellWidget(row, self.tree.columnCount() - 1, button_widget)

        # Set items back to non-editable
        for column in range(2, self.tree.columnCount() - 1):  # Skipping channel_id and buttons
            item = self.tree.item(row, column)
            if item:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Reset to non-editable