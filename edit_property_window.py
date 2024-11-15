import sys
import sqlite3
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QDialog,QMenu
from footer_util import add_company_footer  # Assuming this is a utility module you have
from manual_entry_window import ManualEntryWindow  # Importing ManualEntryWindow class
from import_entry_window import ImportEntryWindow  # Importing ImportEntryWindow class
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog


class EditPropertyWindow(QtWidgets.QWidget):
    def __init__(self, username, reactor_type, reactor_name, selected_channels, database_type):
        super().__init__() 
        self.setWindowTitle("Edit Properties")
        self.setGeometry(100, 100, 1200, 600)
<<<<<<< HEAD
        self.setStyleSheet(""" 
            QWidget {
                background: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #a0c4ff,  /* Soft blue */
                    stop: 1 #f8f9fa   /* Very light grey, almost white */
                );
            }
        """)

        # Initialize necessary variables
        self.username = username
        self.reactor_type = reactor_type
        self.reactor_name = reactor_name
=======
        self.username=username
        self.reactor_type=reactor_type
        self.reactor_name=reactor_name
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
        self.selected_channels = selected_channels
        self.database_type = database_type
        self.selected_channel = ""
        self.selected_property = ""

        # List of properties
        self.properties = [
<<<<<<< HEAD
            "Ingot and manufacturing rout", "Chemical", "Mechanical", "Dimensional"           
=======
            "", "UTS axial", "UTS transverse", "YS axial", "YS transverse",
            "Elongation axial", "Elongation transverse", "Hardness", "Ki axial",
            "Ki transverse", "Density (rho)", "Poisson ratio"
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
        ]

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Horizontal layout for channel frame and property frame
        self.horizontal_layout = QtWidgets.QHBoxLayout()

        # Channel frame and layout
        self.channel_frame = QtWidgets.QFrame(self)
        self.channel_layout = QtWidgets.QVBoxLayout(self.channel_frame)
        self.channel_layout.addWidget(QtWidgets.QLabel("Selected Channels", font=QtGui.QFont("Helvetica", 12)),
                                      alignment=QtCore.Qt.AlignCenter)

        self.selected_channel_listbox = QtWidgets.QListWidget()
        self.selected_channel_listbox.currentRowChanged.connect(self.populate_table_with_selected_channel)
        self.channel_layout.addWidget(self.selected_channel_listbox)

        for channel in selected_channels:
            self.selected_channel_listbox.addItem(channel)

        # Enable drag and drop
        self.selected_channel_listbox.setDragEnabled(True)
        self.selected_channel_listbox.setAcceptDrops(True)
        self.selected_channel_listbox.setDropIndicatorShown(True)

        # Set the channel frame size
        self.channel_frame.setFixedWidth(120)
        self.channel_frame.setFixedHeight(800)
        self.horizontal_layout.addWidget(self.channel_frame)

        # Property frame and layout
        self.property_frame = QtWidgets.QFrame(self)
        self.property_layout = QtWidgets.QVBoxLayout(self.property_frame)
        self.property_layout.addWidget(QtWidgets.QLabel("Select Property to Edit", font=QtGui.QFont("Helvetica", 12)),
                                       alignment=QtCore.Qt.AlignLeft)

        # Combo box for selecting properties
        self.property_combo = QtWidgets.QComboBox()
        self.property_combo.addItems(self.properties)
        self.property_combo.currentIndexChanged.connect(self.property_selected)
        self.property_layout.addWidget(self.property_combo)

        # Add a submenu for "Ingot and manufacturing rout"
        self.property_combo.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.property_combo.customContextMenuRequested.connect(self.show_context_menu)

        # Buttons layout
        self.button_layout = QtWidgets.QHBoxLayout()

        # Add New button
        self.add_new_button = QPushButton("Add New")
        self.add_new_button.setCheckable(True)
        self.add_new_button.setFixedSize(100, 30)
        self.add_new_button.clicked.connect(self.toggle_add_options)
        self.button_layout.addWidget(self.add_new_button)

        # Manual button (initially hidden)
        self.manual_button = QPushButton("Manual")
        self.manual_button.setFixedSize(100, 30)
        self.manual_button.clicked.connect(lambda: self.open_manual_entry(self.username, self.reactor_type, 
                                                                          self.reactor_name, self.selected_channel, 
                                                                          self.database_type, self.selected_property))
        self.manual_button.hide()
        self.button_layout.addWidget(self.manual_button)

        # Import button (initially hidden)
        self.import_button = QPushButton("Import")
        self.import_button.setFixedSize(100, 30)
        self.import_button.clicked.connect(self.open_import_entry_window)
        self.import_button.hide()
        self.button_layout.addWidget(self.import_button)

        # Add button layout to property layout
        self.property_layout.addLayout(self.button_layout)

        # Table to display data
        self.table_frame = QtWidgets.QFrame(self.property_frame)
        self.table_layout = QVBoxLayout(self.table_frame)
        self.tree = QTableWidget()
        self.tree.setColumnCount(208)  # This should remain the same

        # Set header labels with Cells and Positions interleaved
        header_labels = ["Channel", "Property", "Year", "HOY", "Length", "Entry_by", "Entry_Date", "Remark"]
        for i in range(1, 101):
            header_labels.append(f"Cell{i}")
            header_labels.append(f"Position{i}")

        self.tree.setHorizontalHeaderLabels(header_labels)

        self.tree.horizontalHeader().setStretchLastSection(True)
        self.tree.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.table_layout.addWidget(self.tree)
        self.property_layout.addWidget(self.table_frame)

        # Add property frame to main layout
        self.horizontal_layout.addWidget(self.property_frame)
        self.main_layout.addLayout(self.horizontal_layout)

        # Footer frame for back button
        self.footer_frame = QtWidgets.QFrame(self)
        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_frame)
        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(80, 30)
        self.back_button.clicked.connect(self.go_back)
        self.footer_layout.addWidget(self.back_button)
        self.main_layout.addWidget(self.footer_frame)

    def show_context_menu(self, position):

        """Display context menu for property selection."""
        context_menu = QMenu(self)
        

        
        # Create submenu for Ingot and Manufacturing Rout
        if self.property_combo.currentText() == "Ingot and manufacturing rout":
            ingot_menu = context_menu.addMenu("Ingot and Manufacturing Rout")
            ingot_menu.addAction("Ingot No", self.select_property)
            ingot_menu.addAction("Source", self.select_property)
            ingot_menu.addAction("DM/QM", self.select_property)
            ingot_menu.addAction("Man. Rout", self.select_property)
            ingot_menu.addAction("Ingot Chemical", self.select_property)

        elif self.property_combo.currentText() == "Chemical":
            chemical_menu = context_menu.addMenu("Chemical")
            chemical_menu.addAction("Niobium", self.select_property)  
            chemical_menu.addAction("Oxygen", self.select_property)
            chemical_menu.addAction("Iron", self.select_property)
            chemical_menu.addAction("Carbon", self.select_property)
            chemical_menu.addAction("Nitrogen", self.select_property)
            chemical_menu.addAction("Hydrogen", self.select_property)

        elif self.property_combo.currentText() == "Mechanical":
            mechanical_menu = context_menu.addMenu("Mechanical")
            mechanical_menu.addAction("UTS RT", self.select_property)
            mechanical_menu.addAction("YS RT", self.select_property)
            mechanical_menu.addAction("% Elongation RT", self.select_property)
            mechanical_menu.addAction("UTS 300", self.select_property)
            mechanical_menu.addAction("YS 300", self.select_property)
            mechanical_menu.addAction("% Elongation 300", self.select_property)
            mechanical_menu.addAction("Hardness", self.select_property)

        elif self.property_combo.currentText() == "Dimensional":
            dimensional_menu = context_menu.addMenu("Dimensional")
            dimensional_menu.addAction("Average Inner Diameter vs position", self.select_property)
            dimensional_menu.addAction("Minimum Thickness vs position", self.select_property)
            dimensional_menu.addAction("Maximum Thickness vs position", self.select_property)
            dimensional_menu.addAction("Total Length", self.select_property)
            dimensional_menu.addAction("UT inspection report", self.select_property)
            dimensional_menu.addAction("Garter Spring positions", self.select_property)       

        context_menu.exec_(self.mapToGlobal(position))


        #context_menu.exec_(self.property_combo.mapToGlobal(position))

    def select_property(self):
        """Handle property selection from the submenu."""
        action = self.sender()
        if action:
            selected_property = action.text()
            self.property_combo.setCurrentText(selected_property)
            

    def go_back(self):
        """Go back to the previous window."""
        self.close()
        
    def toggle_add_options(self):
        """Toggle visibility of Manual and Import buttons."""
        if self.add_new_button.isChecked():
            self.manual_button.show()
            self.import_button.show()
            self.add_new_button.setText("Undo")
        else:
            self.manual_button.hide()
            self.import_button.hide()
            self.add_new_button.setText("Add New")

    def open_manual_entry(self, username, reactor_type, reactor_name, selected_channel, database_type, selected_property):
        """Handle manual entry of properties."""
<<<<<<< HEAD
        if not selected_channel:
            QMessageBox.information(self, "Info", "Please select the channel to be edited")
            return
        print("Selected channel is " + selected_channel)
        self.manualEntryWindow = ManualEntryWindow(self, username, reactor_type, reactor_name, selected_channel,
                                                   database_type, selected_property)
        self.manualEntryWindow.show()

        # Connect the manual entry window close event to the table refresh method
        self.manualEntryWindow.finished.connect(self.refresh_table)

    def open_import_entry_window(self):
        """Open the import entry window."""
        import_window = ImportEntryWindow(self.reactor_name, self.reactor_type, self.username, 
                                          self.selected_channel, self.selected_property, self)
        if import_window.exec_() == QDialog.Accepted:
            self.display_imported_data(import_window.selected_file)

    def display_imported_data(self, file_path):
        """Display the imported data in the table."""
        try:
            df = pd.read_excel(file_path)
            self.tree.setRowCount(len(df.index))
            self.tree.setColumnCount(len(df.columns))
            self.tree.setHorizontalHeaderLabels(df.columns.tolist())  # Convert to list for setHorizontalHeaderLabels

            for row in range(len(df.index)):
                for col in range(len(df.columns)):
                    self.tree.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to display imported data: {e}")

    def populate_table(self, channel):
        """Populate the table with data from the database for the selected channel."""
        if not channel or not self.database_type or not self.selected_property:
=======
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
        # Open a file dialog to select a CSV file
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("CSV Files (*.csv);;All Files (*)")
        file_dialog.setViewMode(QtWidgets.QFileDialog.List)

        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                # Assuming the first selected file is the one we want to import
                selected_file = file_paths[0]
                try:
                    # Open the selected CSV file and read its content
                    with open(selected_file, 'r') as file:
                        # Read the CSV file line by line
                        lines = file.readlines()

                    # Process the content of the CSV file
                    for line in lines:
                        # Assuming CSV format: channel_id, property_name, year, HOY, length, entry_by, entry_date, remark, ...
                        data = line.strip().split(',')
                        if len(data) < 8:  # Ensure there are enough fields
                            continue

                        channel_id, property_name, year, hoy, length, entry_by, entry_date, remark, *cells = data

                        # Insert or update the data into the database
                        conn = sqlite3.connect('iphwr_analysis.db')
                        cursor = conn.cursor()

                        # Here, you might want to use an INSERT or UPDATE query based on your requirements
                        query = """
                        INSERT INTO properties (channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                                                Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9,
                                                Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17,
                                                Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        cursor.execute(query, (channel_id, property_name, year, hoy, length, entry_by, entry_date, remark,
                                            *cells))

                        conn.commit()
                        conn.close()

                    QMessageBox.information(self, "Success", "Data imported successfully!")
                    # Optionally, you might want to refresh the table view after import
                    self.populate_table(self.selected_channel, self.selected_property)

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while importing data: {str(e)}")


    def populate_table(self, channel, property):
        """Fetch data from the database and populate the TableView for the selected channel."""
        if property=="":
            print("No property selected")
        # Check if a channel is selected
        if not channel or not self.database_type:
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
            return

        try:
            with sqlite3.connect('iphwr_analysis.db') as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                    {', '.join([f'Cell{i}, Position{i}' for i in range(1, 101)])} 
                    FROM properties 
                    WHERE channel_id = ? AND property_name = ?''', 
                    (channel, self.selected_property)
                )

                rows = cursor.fetchall()
                self.tree.setRowCount(len(rows))  # Set number of rows in the table
                for row_idx, row_data in enumerate(rows):
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value))
                        self.tree.setItem(row_idx, col_idx, item)

               # if not rows:
                   # QMessageBox.information(self, "No Data", f"No data available for {channel} - {self.selected_property}")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while accessing the database: {e}")

    def populate_table_with_selected_channel(self, current_row):
        """Populate the table when a channel is selected."""
        if current_row >= 0:
            self.selected_channel = self.selected_channel_listbox.item(current_row).text()
            self.populate_table(self.selected_channel)

<<<<<<< HEAD
    def property_selected(self):
        """Handle the property selection from the combo box."""  
        self.selected_property = self.property_combo.currentText()
        self.populate_table(self.selected_channel)

    def refresh_table(self):
        """Refresh the table after manual entry or import."""
        self.populate_table(self.selected_channel)
=======
        # Build the SQL query based on whether a property is selected or not
        if property == "":
            print("No specific property selected, showing all properties")
            query = "SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties WHERE channel_id=? AND reactor_type=? AND reactor_name=?"
            cursor.execute(query, (channel, self.reactor_type, self.reactor_name))
        else:
            query = "SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties WHERE channel_id=? AND property_name=? AND reactor_type=? AND reactor_name=?"
            cursor.execute(query, (channel, property, self.reactor_type, self.reactor_name))
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
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
