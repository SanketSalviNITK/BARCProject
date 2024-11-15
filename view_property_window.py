import sys
import sqlite3
<<<<<<< HEAD
import pandas as pd
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QListWidget, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
#from footer_util import add_company_footer

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib import cm
from scipy.ndimage import gaussian_filter  


class ViewPropertyWindow(QWidget):
    def __init__(self, selected_channels, database_type, reactor_type, reactor_name):
        super().__init__()
        self.setWindowTitle("View Properties")
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

        self.showMaximized()

        self.selected_channels = selected_channels
        self.database_type = database_type
        self.reactor_type = reactor_type
        self.reactor_name = reactor_name

        # Initialize SQLite connection
        self.conn = sqlite3.connect('iphwr_analysis.db')
        self.c = self.conn.cursor()

        # Create main layout (Horizontal Layout)
        main_layout = QHBoxLayout(self)

        # Frame for selected channels, property label, and property buttons (Left Side)
        self.channel_frame = QWidget()
        self.channel_layout = QVBoxLayout()
        self.channel_frame.setLayout(self.channel_layout)
        
        # Label to display selected channels
        self.channel_label = QLabel(f"Selected Channels for {reactor_type} - {reactor_name}")
        self.channel_layout.addWidget(self.channel_label)
        
        # Listbox to display the selected channels
        self.selected_channel_listbox = QListWidget()
        self.selected_channel_listbox.addItems(selected_channels)
        self.selected_channel_listbox.setFixedWidth(300)  # Set a fixed width for the listbox
        
        self.channel_layout.addWidget(self.selected_channel_listbox)

        # Property label for selected property
        self.property_label = QLabel("Selected Property: None")
        self.channel_layout.addWidget(self.property_label)

        # Property buttons for selecting properties
=======
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

from export_data import ExportData
from manual_entry_window import ManualEntryWindow
from show_graph import Show_Graph


class ViewPropertyWindow(QtWidgets.QWidget):
    def __init__(self, username, reactor_type, reactor_name, selected_channels, database_type):
        super().__init__()
        self.setWindowTitle("View Properties")
        self.setGeometry(100, 100, 1200, 600)
        self.username=username
        self.reactor_type=reactor_type
        self.reactor_name=reactor_name
        self.selected_channels = selected_channels
        self.database_type = database_type
        self.selected_channel=""
        self.selected_property=""
        # List of properties
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
        self.properties = [
            "", "UTS axial", "UTS transverse", "YS axial", "YS transverse",
            "Elongation axial", "Elongation transverse", "Hardness", "Ki axial",
            "Ki transverse", "Density (rho)", "Poisson ratio"
        ]

<<<<<<< HEAD
        self.property_buttons = {}
        for prop in self.properties:
            button = QPushButton(prop)
            button.clicked.connect(lambda checked, p=prop: self.select_property(p))
            button.setFixedWidth(300)  # Set the width of the button to match the listbox
            self.channel_layout.addWidget(button)
            self.property_buttons[prop] = button

        # Add the left layout (channel_frame) to the main layout
        main_layout.addWidget(self.channel_frame)
        #add_company_footer(self.main_layout)

        # Right side for the table
        right_side_layout = QVBoxLayout()

        # Bottom half section: Table to display existing data from the database
        self.table = QTableWidget()
        # Make the table expand to fill more of the window
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        
        # Allow the table to take more width compared to the listbox
        main_layout.addLayout(right_side_layout, stretch=2)  # This increases right side width

        right_side_layout.addWidget(self.table)

        # Buttons for Graph and Export
        button_layout = QHBoxLayout()
        self.graph_button = QPushButton("Graph")
        self.graph_button.clicked.connect(self.plot_graph)
        button_layout.addWidget(self.graph_button)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_to_excel)
        button_layout.addWidget(self.export_button)

        # Add buttons for graph and export under the table
        right_side_layout.addLayout(button_layout)
=======
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

        self.property_layout.addWidget(QtWidgets.QLabel("Select Property to View", font=QtGui.QFont("Helvetica", 12)),
                                       alignment=QtCore.Qt.AlignLeft)

        # Combo box to select properties
        self.property_combo = QtWidgets.QComboBox()
        self.property_combo.setFixedWidth(120)
        self.property_combo.addItems(self.properties)
        self.property_combo.currentIndexChanged.connect(self.property_selected)  # Connect the signal to a method
        self.property_layout.addWidget(self.property_combo)


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
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a

        self.horizontal_layout.addWidget(self.property_frame)
        self.main_layout.addLayout(self.horizontal_layout)

<<<<<<< HEAD
    def select_property(self, property_name):
        """Select a property and update the table based on the selection."""
        self.selected_property = property_name
        self.property_label.setText(f"Selected Property: {self.selected_property}")  # Update label
        self.populate_table()


    def plot_graph(self):

        """Plot a graph based on selected property and channels with enhanced visuals."""
        if not self.selected_channel_listbox.currentItem():
            QMessageBox.critical(self, "Error", "Please select a channel.")
            return

        selected_channel = self.selected_channel_listbox.currentItem().text()

        if selected_channel and self.selected_property:
            try:
                # Query to retrieve data from the database
                query = """
                SELECT HOY, Year, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8,
                    Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15,
                    Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24
                FROM properties
                WHERE channel_id = ? AND property_name = ? AND reactor_type = ? AND reactor_name = ?
                """
                self.c.execute(query, (selected_channel, self.selected_property, self.reactor_type, self.reactor_name))
                rows = self.c.fetchall()
=======
        # Create footer frame for buttons
        self.footer_frame = QtWidgets.QFrame(self)
        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_frame)
        self.footer_layout.setSpacing(10)  # Add spacing between buttons
        self.footer_frame.setFixedHeight(50)  # Adjust height of footer frame if necessary

        # Back button
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setFixedSize(80, 30)  # Set smaller size for Back button
        self.back_button.clicked.connect(self.go_back)
        self.footer_layout.addWidget(self.back_button)

        # Graph button
        self.graph_button = QtWidgets.QPushButton("Graph")
        self.graph_button.setFixedSize(80, 30)  # Set smaller size for Graph button
        self.graph_button.clicked.connect(self.show_graph)
        self.footer_layout.addWidget(self.graph_button)

        # Export Button
        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.setFixedSize(80, 30)  # Set smaller size for Export button
        self.export_button.clicked.connect(self.export_data)
        self.footer_layout.addWidget(self.export_button)

        # Add footer frame to the main layout
        self.main_layout.addWidget(self.footer_frame)

    def go_back(self):
        """Close the current window and go back to the previous window."""
        self.close()
        
    def show_graph(self):
        Show_Graph(self,self.cursor, self.selected_channel,self.selected_property)
    
    def export_data(self):
        ExportData.export_to_excel(self, self.selected_channel,self.selected_property)
    
    def populate_table(self, channel, property):
        """Fetch data from the database and populate the TableView for the selected channel."""
        # Check if a channel is selected
        if not channel or not self.database_type:
            return
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a

        conn = sqlite3.connect('iphwr_analysis.db')
        cursor = conn.cursor()
    
        # Define the columns for the table
        headers = [
            'Channel ID', 'Property Name', 'Year', 'HOY', 'Length', 'Entry By', 'Entry Date', 'Remark',
            'Cell1', 'Cell2', 'Cell3', 'Cell4', 'Cell5', 'Cell6', 'Cell7', 'Cell8', 'Cell9', 'Cell10',
            'Cell11', 'Cell12', 'Cell13', 'Cell14', 'Cell15', 'Cell16', 'Cell17', 'Cell18', 'Cell19',
            'Cell20', 'Cell21', 'Cell22', 'Cell23', 'Cell24'
        ]

<<<<<<< HEAD
                # Create a plot
                fig, ax = plt.subplots(figsize=(10, 6))

                # Generate background blur
                bg_values = np.random.random((25, 100))  # Random background data to simulate blur
                blurred_bg = gaussian_filter(bg_values, sigma=7)  # Apply Gaussian blur
                cmap = ListedColormap(cm.get_cmap('Blues')(np.linspace(0, 0.5, 256)))  # Adjust color map for background

                # Plot blurred background as an image
                ax.imshow(blurred_bg, cmap=cmap, extent=[0, 6000, 0, 1], aspect='auto', alpha=0.4)

                # Plot data for each entry
                for row in rows:
                    hoy, year = row[0], row[1]  # HOY and Year
                    values = row[2:]  # Cell1 to Cell24 values

                    # Convert values to numeric and handle missing values
                    values = pd.Series(pd.to_numeric(values, errors='coerce')).fillna(0)

                    # Define x_positions based on the number of cells available
                    num_cells = len(values)
                    x_positions = [(i * (6000 / 24)) for i in range(num_cells)]  # [0, 250, 500, ..., 6000]

                    # Plot the line for this entry with markers and a thicker line
                    ax.plot(x_positions, values, marker='o', markersize=6, linewidth=2, label=f"HOY: {hoy}, Year: {year}")

                # Set the plot title, labels, and legend
                ax.set_title(f"{self.selected_property} - {selected_channel} ({self.reactor_type} - {self.reactor_name})", fontsize=14, fontweight='bold')
                ax.set_xlabel("Position (mm)", fontsize=12)
                ax.set_ylabel("Value", fontsize=12)
                ax.legend(fontsize=10)

                # Customize x-axis ticks
                ax.set_xticks([i * (6000 / 24) for i in range(25)])  # Set ticks at 0, 250, 500, ..., 6000
                ax.set_xticklabels([str(i * (6000 // 24)) for i in range(25)], fontsize=10)  # Label ticks with the corresponding positions

                # Add gridlines for better readability
                ax.grid(True, linestyle='--', alpha=0.6)

                # Display the plot
                plt.tight_layout()
                plt.show()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to plot graph: {e}")


    def export_to_excel(self):
        """Export data to an Excel file."""
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (.xlsx);;All Files ()", options=options)
            if file_path:
                df = pd.DataFrame()

                for channel in self.selected_channels:
                    query = '''SELECT * FROM properties WHERE channel_id = ? AND database_type = ? AND reactor_type = ? AND reactor_name = ?'''
                    if self.selected_property:
                        query += ' AND property_name = ?'
                        self.c.execute(query, (channel, self.database_type, self.reactor_type, self.reactor_name, self.selected_property))
                    else:
                        self.c.execute(query, (channel, self.database_type, self.reactor_type, self.reactor_name))
                    
                    rows = self.c.fetchall()
                    df = pd.concat([df, pd.DataFrame(rows, columns=[desc[0] for desc in self.c.description])], ignore_index=True)

                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", "Data exported successfully.")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export data: {e}")

    def populate_table(self):
        """Fetch data from the database and populate the table based on selected channels and property."""
=======
        # Set column count and headers
        self.tree.setColumnCount(len(headers))
        self.tree.setHorizontalHeaderLabels(headers)

>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
        # Clear the current table
        self.tree.setRowCount(0)  # Clear existing data in the table

<<<<<<< HEAD
            # Fetch the data for the selected channels and database type
        all_rows = []
        for channel in self.selected_channels:
                query = '''SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                                    Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10,
                                    Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19,
                                    Cell20, Cell21, Cell22
                            FROM properties WHERE channel_id = ? AND database_type = ? AND reactor_type = ? AND reactor_name = ?'''
                if self.selected_property:
                        query += ' AND property_name = ?'
                        self.c.execute(query, (channel, self.database_type, self.reactor_type, self.reactor_name, self.selected_property))
                else:
                        self.c.execute(query, (channel, self.database_type, self.reactor_type, self.reactor_name))
                    
                rows = self.c.fetchall()
                all_rows.extend(rows)

        if all_rows:
            # Set table dimensions and headers
            headers = ['Channel ID', 'Property Name', 'Year', 'HOY', 'Length', 'Entry By', 'Entry Date', 'Remark'] + \
                    [f'Cell{i}' for i in range(1, 23)]
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)

            # Add rows to the table
            for row_idx, row_data in enumerate(all_rows):
                self.table.insertRow(row_idx)
                for col_idx, item in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        else:
            self.table.setColumnCount(0)
=======
        # Build the SQL query based on whether a property is selected or not
        if property == "":
            print("No specific property selected, showing all properties")
<<<<<<< HEAD
            query = "SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties WHERE channel_id=? AND reactor_type=? AND reactor_name=?"
            cursor.execute(query, (channel, self.reactor_type, self.reactor_name))
=======
            query = "SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties WHERE channel_id=?"
            cursor.execute(query, (channel,))
>>>>>>> 02144d384de7f1bfe526796172c4cd9cf3e0bd26
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ViewPropertyWindow("Admin","220_IPHWR", "RAPS-1", ["A08","A09"], "Mechanical")
    window.show()
    sys.exit(app.exec_())
>>>>>>> 98c0f3ee07d7a92d19059f36a8a84909fa2fd36a
