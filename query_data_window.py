import sys
import sqlite3
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from footer_util import add_company_footer

class QueryDataWindow(QWidget):
    def __init__(self, selected_channels, database_type, reactor_type, reactor_name):
        super().__init__()
        self.setWindowTitle("Query Data")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(
                spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                stop: 0 #a0c4ff,  /* Soft blue */
                stop: 1 #f8f9fa   /* Very light grey, almost white */
            );
        }
        """)

        self.selected_channels = selected_channels
        self.database_type = database_type
        self.reactor_type = reactor_type
        self.reactor_name = reactor_name

        # Initialize SQLite connection
        self.conn = sqlite3.connect('iphwr_analysis.db')
        self.c = self.conn.cursor()

        # Layout for the window
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Label for instructions
        instruction_label = QLabel("Select a channel and property to query:")
        layout.addWidget(instruction_label)

        # List for selected channels
        self.channel_listbox = QListWidget()
        self.channel_listbox.addItems(self.selected_channels)
        layout.addWidget(self.channel_listbox)

        # Property selection
        self.property_label = QLabel("Select Property:")
        layout.addWidget(self.property_label)

        self.properties = [
            "UTS axial", "UTS transverse", "YS axial", "YS transverse",
            "Elongation axial", "Elongation transverse", "Hardness", "Ki axial",
            "Ki transverse", "Density (rho)", "Poisson ratio"
        ]

        self.property_combobox = QComboBox()
        self.property_combobox.addItems(self.properties)
        layout.addWidget(self.property_combobox)

        # Query Button
        self.query_button = QPushButton("Fetch Data")
        self.query_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.query_button)

        # Plot Graph Button
        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(self.plot_button)

        # Table to display fetched data
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Path display label
        self.path_label = QLabel("")
        layout.addWidget(self.path_label)

        # Export Button (disabled until data is fetched)
        self.export_button = QPushButton("Export Data")
        self.export_button.setEnabled(False)  # Disable initially
        self.export_button.clicked.connect(self.export_data)
        layout.addWidget(self.export_button)

        # Add company footer at the end of the layout
        add_company_footer(layout)

    def fetch_data(self):
        """Fetch data from the database based on selected channel and property."""
        selected_channel = self.channel_listbox.currentItem()
        selected_property = self.property_combobox.currentText()

        if not selected_channel:
            QMessageBox.critical(self, "Error", "Please select a channel.")
            return

        channel_id = selected_channel.text()

        # Update the path label with the selected details
        path = f"Path: Channel ID = {channel_id}, Reactor Type = {self.reactor_type}, Reactor Name = {self.reactor_name}, Database Type = {self.database_type}, Property = {selected_property}"
        self.path_label.setText(path)

        # Query to retrieve data from the database
        query = """
            SELECT * FROM properties 
            WHERE channel_id = ? AND property_name = ? AND reactor_type = ? AND reactor_name = ?
        """
        self.c.execute(query, (channel_id, selected_property, self.reactor_type, self.reactor_name))
        rows = self.c.fetchall()

        # Populate the table with results
        if rows:
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]))
            for row_index, row in enumerate(rows):
                for col_index, item in enumerate(row):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(item)))
            self.export_button.setEnabled(True)  # Enable the export button after fetching data
        else:
            QMessageBox.information(self, "No Data", "No data found for the selected channel and property.") 
            self.export_button.setEnabled(False)  # Disable the export button if no data

    def plot_graph(self):


        """Plot a graph based on the selected channel and property, using dynamic positions from the database."""
        selected_channel = self.channel_listbox.currentItem()
        selected_property = self.property_combobox.currentText()

        if not selected_channel:
            QMessageBox.critical(self, "Error", "Please select a channel.")
            return

        channel_id = selected_channel.text()

        # Query to retrieve cell values, positions, Year, and HOY for the selected channel and property
        query = f"""
        SELECT {', '.join(['Cell' + str(i) for i in range(1, 101)])}, 
            {', '.join(['Position' + str(i) for i in range(1, 101)])},
            Year, HOY
        FROM properties 
        WHERE channel_id = ? AND property_name = ? AND reactor_type = ? AND reactor_name = ?
        """
        self.c.execute(query, (channel_id, selected_property, self.reactor_type, self.reactor_name))
        rows = self.c.fetchall()

        if not rows:
            QMessageBox.critical(self, "Error", "No data available for the selected channel and property.")
            return

        # Prepare data for plotting
        for row in rows:
            cell_values = row[:100]  # Get the first 100 cells
            positions = row[100:200]  # Get the next 100 positions
            year = row[200]  # Year
            hoy = row[201]  # HOY

            # Convert to Pandas Series for easier handling
            cell_values_series = pd.Series(cell_values)
            positions_series = pd.Series(positions)

            # Ensure there are no NaN values in positions
            valid_positions = positions_series.dropna()
            valid_values = cell_values_series[valid_positions.index]  # Align values with valid positions

            # Plot the data
            plt.plot(valid_positions, valid_values, marker='o', label=f"Channel: {channel_id} - Year: {year}, HOY: {hoy}")

            # Annotate the plot with Year and HOY
            for pos, value in zip(valid_positions, valid_values):
                if pd.notna(pos) and pd.notna(value):
                    plt.text(pos, value, f"{year}\n{hoy}", fontsize=8, ha='center', va='bottom', alpha=0.7)

        # Set the plot title, labels, and legend
        plt.title(f"{selected_property} - {channel_id} ({self.reactor_type} - {self.reactor_name})")
        plt.xlabel("Position")
        plt.ylabel("Cell Value")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

       
    def export_data(self):
        """Export the currently fetched data to a CSV file."""
        # Open file dialog to choose where to save the CSV
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data as CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if file_name:
            try:
                with open(file_name, 'w', newline='') as file:
                    writer = csv.writer(file)

                    # Write the table headers
                    headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                    writer.writerow(headers)

                    # Write the table data
                    for row_index in range(self.table.rowCount()):
                        row_data = []
                        for col_index in range(self.table.columnCount()):
                            item = self.table.item(row_index, col_index)
                            row_data.append(item.text() if item is not None else "")
                        writer.writerow(row_data)

                QMessageBox.information(self, "Success", "Data successfully exported to CSV.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")
