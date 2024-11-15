import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QLabel, QMessageBox
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel,  QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
import sqlite3

class MechanicalPropertyViewer(QWidget):
    def __init__(self, username, reactor_type, reactor_name, selected_channels, database_type):
        super().__init__()
        self.setWindowTitle("Edit Properties")
        self.setGeometry(100, 100, 1200, 600)
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
        self.selected_channels = selected_channels
        self.database_type = database_type
        self.selected_channel = ""
        self.selected_property = ""
        self.table_name = "reactor_data_min_thickness"
        
        # Define properties and associated tables
        self.properties = {
            "Manufacturing_Tube_Dimensions": [
                "reactor_data_min_thickness",
                "reactor_data_max_thickness",
                "reactor_data_min_inner_diameter",
                "reactor_data_max_inner_diameter",
                "reactor_data_avg_outside_diameter"
            ],
            "Manufacturing_Tube_Mechanical_Properties": ["Tube_Mechanical_Properties"],
            "Manufacturing_Tube_Chemical_Composition": ["Tube_Chemical_Composition"],
            "Manufacturing_Ingot_Details": ["Tube_Ingot_Details"],
            "Manufacturing_Installation": ["Tube_Installation"]
        }

        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        
        # Channel list frame (20% width)
        self.channel_frame = QtWidgets.QFrame(self)
        self.channel_frame.setFixedWidth(240)  # Set to 20% of 1200px (window width)
        self.channel_layout = QVBoxLayout(self.channel_frame)
        
        self.channel_label = QLabel("Selected Channels", font=QtGui.QFont("Helvetica", 12))
        self.channel_layout.addWidget(self.channel_label, alignment=QtCore.Qt.AlignCenter)

        self.selected_channel_listbox = QListWidget()
        self.selected_channel_listbox.addItems(selected_channels)
        self.selected_channel_listbox.currentRowChanged.connect(self.populate_table_with_selected_channel)
        self.channel_layout.addWidget(self.selected_channel_listbox)

        main_layout.addWidget(self.channel_frame)

        # Main content frame (remaining 80%)
        content_frame = QtWidgets.QFrame(self)
        content_layout = QVBoxLayout(content_frame)
        
        # Dropdowns and table
        self.property_label = QLabel("Select Property to Edit", font=QtGui.QFont("Helvetica", 12))
        content_layout.addWidget(self.property_label, alignment=QtCore.Qt.AlignLeft)

        self.property_dropdown = QComboBox()
        self.property_dropdown.addItems(self.properties.keys())
        self.property_dropdown.currentTextChanged.connect(self.update_table_dropdown)
        content_layout.addWidget(self.property_dropdown)

        self.table_label = QLabel("Select Table:")
        content_layout.addWidget(self.table_label)

        self.table_dropdown = QComboBox()
        self.table_dropdown.currentTextChanged.connect(self.load_table_data)
        content_layout.addWidget(self.table_dropdown)

        self.table_widget = QTableWidget()
        content_layout.addWidget(self.table_widget)

        main_layout.addWidget(content_frame)

        # Initialize the table dropdown with the first property selection
        self.update_table_dropdown(self.property_dropdown.currentText())
        
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
        main_layout.addLayout(self.button_layout)
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
        if not selected_channel:
            QMessageBox.information(self, "Info", "Please select the channel to be edited")
            return
        print("Selected channel is " + selected_channel)
        # self.manualEntryWindow = ManualEntryWindow(self, username, reactor_type, reactor_name, selected_channel,
                                                #    database_type, selected_property)
        self.manualEntryWindow.show()

        # Connect the manual entry window close event to the table refresh method
        self.manualEntryWindow.finished.connect(self.refresh_table)

    def open_import_entry_window(self):
        """Open the import entry window."""
        # import_window = ImportEntryWindow(self.reactor_name, self.reactor_type, self.username, 
        #                                   self.selected_channel, self.selected_property, self)
        # if import_window.exec_() == QDialog.Accepted:
        #     self.display_imported_data(import_window.selected_file)
    
    def populate_table_with_selected_channel(self, current_row):
        if current_row >= 0:
            self.selected_channel = self.selected_channel_listbox.item(current_row).text()
            self.populate_table(self.selected_channel) 

    def populate_table(self, channel):
        if not channel or not self.database_type or not self.selected_property:
            return

        try:
            with sqlite3.connect('reactor_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {self.table_name}")
                rows = cursor.fetchall()
                self.table_widget.setRowCount(len(rows))
                for row_idx, row_data in enumerate(rows):
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value))
                        self.table_widget.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while accessing the database: {e}")
    
    def update_table_dropdown(self, property_name):
        self.table_dropdown.clear()
        tables = self.properties.get(property_name, [])
        self.table_dropdown.addItems(tables)

    def load_table_data(self):
        self.table_name = self.table_dropdown.currentText()
        if not self.table_name:
            return

        connection = sqlite3.connect('reactor_data.db')
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(column_names))
            self.table_widget.setHorizontalHeaderLabels(column_names)

            for row_index, row_data in enumerate(rows):
                for column_index, cell_data in enumerate(row_data):
                    cell_item = QTableWidgetItem(str(cell_data))
                    self.table_widget.setItem(row_index, column_index, cell_item)

            self.table_widget.resizeColumnsToContents()
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
        finally:
            connection.close()

            
            
class ISIDataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ISI Data Viewer")
        self.setGeometry(100, 100, 1200, 600)

        # Define ISI properties and associated tables
        self.properties = {
            "ISI Data Viewer": [
                "ISI_PSI_Avg_Diameter",
                "ISI_PT_Centerline_SAG",
                "ISI_Thickness",
                "ISI_Channel_Length",
                "ISI_Inspection_Log",
                "ISI_GS_Position"
            ]
        }

        # Layout and widgets
        self.layout = QVBoxLayout()

        # Dropdown for selecting ISI Property
        self.property_label = QLabel("Select ISI Property:")
        self.property_dropdown = QComboBox()
        self.property_dropdown.addItems(self.properties.keys())
        self.property_dropdown.currentTextChanged.connect(self.update_table_dropdown)

        # Dropdown for selecting specific table within the selected property
        self.table_label = QLabel("Select Table:")
        self.table_dropdown = QComboBox()
        self.table_dropdown.currentTextChanged.connect(self.load_table_data)

        # Table widget to display data
        self.table_widget = QTableWidget()

        # Add widgets to layout
        self.layout.addWidget(self.property_label)
        self.layout.addWidget(self.property_dropdown)
        self.layout.addWidget(self.table_label)
        self.layout.addWidget(self.table_dropdown)
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)

        # Initialize the table dropdown with the first property selection
        self.update_table_dropdown(self.property_dropdown.currentText())

    def update_table_dropdown(self, property_name):
        """Updates the table dropdown based on the selected property."""
        # Clear and populate the table dropdown
        self.table_dropdown.clear()
        tables = self.properties.get(property_name, [])
        self.table_dropdown.addItems(tables)

    def load_table_data(self):
        """Loads data from the selected table into the table widget."""
        table_name = self.table_dropdown.currentText()
        if not table_name:
            return

        # Connect to the database and fetch data
        connection = sqlite3.connect('reactor_data.db')
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            # Set up the table widget
            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(column_names))
            self.table_widget.setHorizontalHeaderLabels(column_names)

            # Populate the table widget with data
            for row_index, row_data in enumerate(rows):
                for column_index, cell_data in enumerate(row_data):
                    cell_item = QTableWidgetItem(str(cell_data))
                    self.table_widget.setItem(row_index, column_index, cell_item)

            # Resize columns to fit content
            self.table_widget.resizeColumnsToContents()
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
        finally:
            # Close the database connection
            connection.close()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #viewer = MechanicalPropertyViewer()
    viewer = ISIDataViewer()
    viewer.show()
    sys.exit(app.exec_())
