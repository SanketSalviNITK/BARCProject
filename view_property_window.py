import sys
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QListWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt

class ViewPropertyWindow(QMainWindow):
    def __init__(self, selected_channels, database_type):
        super().__init__()
        self.setWindowTitle("View Properties")
        self.setGeometry(100, 100, 1200, 600)

        self.selected_channels = selected_channels
        self.database_type = database_type

        # Initialize SQLite connection
        self.conn = sqlite3.connect('iphwr_analysis.db')
        self.c = self.conn.cursor()

        # Create a central widget and set it as the central widget of the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout(central_widget)

        # Frame for selected channels
        self.channel_frame = QWidget()
        self.channel_layout = QVBoxLayout()
        self.channel_frame.setLayout(self.channel_layout)
        
        self.channel_label = QLabel("Selected Channels")
        self.channel_layout.addWidget(self.channel_label)
        
        self.selected_channel_listbox = QListWidget()
        self.selected_channel_listbox.addItems(selected_channels)
        self.channel_layout.addWidget(self.selected_channel_listbox)

        main_layout.addWidget(self.channel_frame)

        # Frame for properties
        self.property_frame = QWidget()
        self.property_layout = QVBoxLayout()
        self.property_frame.setLayout(self.property_layout)
        main_layout.addWidget(self.property_frame)

        # List of properties
        self.properties = [
            "UTS axial", "UTS transverse", "YS axial", "YS transverse",
            "Elongation axial", "Elongation transverse", "Hardness", "Ki axial",
            "Ki transverse", "Density (rho)", "Poisson ratio"
        ]

        # Property selection buttons
        self.property_buttons = {}
        for prop in self.properties:
            button = QPushButton(prop)
            button.clicked.connect(lambda checked, p=prop: self.select_property(p))
            self.property_layout.addWidget(button)
            self.property_buttons[prop] = button

        # Table to display existing data from the database
        self.table = QTableWidget()
        self.property_layout.addWidget(self.table)

        # Buttons for Graph and Export
        self.graph_button = QPushButton("Graph")
        self.graph_button.clicked.connect(self.plot_graph)
        self.property_layout.addWidget(self.graph_button)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_to_excel)
        self.property_layout.addWidget(self.export_button)

        # Populate the table with properties initially
        self.selected_property = None
        self.populate_table()

    def select_property(self, property_name):
        """Select a property and update the table based on the selection."""
        self.selected_property = property_name
        self.populate_table()

    def plot_graph(self):
        if not self.selected_channel_listbox.currentItem():
            QMessageBox.critical(self, "Error", "Please select a channel.")
            return
        
        selected_channel = self.selected_channel_listbox.currentItem().text()
        
        if selected_channel and self.selected_property:
            try:
                # Query to retrieve data from the database
                query = """
                SELECT cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8,
                       cell9, cell10, cell11, cell12, cell13, cell14, cell15,
                       cell16, cell17, cell18, cell19, cell20, cell21, cell22
                FROM properties
                WHERE channel_id = ? AND property_name = ?
                """
                self.c.execute(query, (selected_channel, self.selected_property))
                rows = self.c.fetchall()

                if not rows:
                    QMessageBox.critical(self, "Error", "No data available for the selected channel and property.")
                    return

                # Convert the retrieved data to a DataFrame
                df = pd.DataFrame(rows, columns=[f"Cell{i+1}" for i in range(len(rows[0]))])
                df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

                # Create a plot
                fig, ax = plt.subplots(figsize=(10, 6))
                for index, row in df.iterrows():
                    ax.plot(df.columns, row.values, marker='o', label=f"Entry {index + 1}")

                ax.set_title(f"{self.selected_property} - {selected_channel}")
                ax.set_xlabel("Cells")
                ax.set_ylabel("Value")
                ax.legend()

                # Display the plot
                plt.show()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to plot graph: {e}")

    def export_to_excel(self):
        try:
            if not self.selected_channel_listbox.currentItem():
                QMessageBox.critical(self, "Error", "Please select a channel.")
                return
            
            selected_channel = self.selected_channel_listbox.currentItem().text()
            
            if not self.selected_property:
                QMessageBox.critical(self, "Error", "Property must be selected.")
                return

            query = "SELECT * FROM properties WHERE channel_id = ? AND property_name = ?"
            df = pd.read_sql_query(query, self.conn, params=(selected_channel, self.selected_property))

            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
            if file_path:
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", f"Data exported successfully to {file_path}.")
                self.display_exported_data(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")

    def display_exported_data(self, file_path):
        try:
            df = pd.read_excel(file_path)

            # Clear existing data in the table
            self.table.setRowCount(0)
            self.table.setColumnCount(0)

            self.table.setColumnCount(len(df.columns))
            self.table.setRowCount(len(df))

            # Set headers
            self.table.setHorizontalHeaderLabels(df.columns)

            for row_index, row in df.iterrows():
                for col_index, value in enumerate(row):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to display exported data: {str(e)}")

    def populate_table(self):
        """Fetch data from the database and populate the table based on selected channels and property."""
        # Clear the current table
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        # Fetch the data for the selected channels and database type
        for channel in self.selected_channels:
            query = '''SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark,
                              Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10,
                              Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19,
                              Cell20, Cell21, Cell22, Cell23, Cell24
                       FROM properties
                       WHERE channel_id = ? AND database_type = ?'''

            if self.selected_property:
                query += ' AND property_name = ?'
                self.c.execute(query, (channel, self.database_type, self.selected_property))
            else:
                self.c.execute(query, (channel, self.database_type))

            rows = self.c.fetchall()

            # Populate the table with fetched data
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col_index, item in enumerate(row):
                    self.table.setItem(row_position, col_index, QTableWidgetItem(str(item)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    selected_channels = ["Channel 1", "Channel 2", "Channel 3"]  # Example selected channels
    database_type = "example_db"  # Replace with actual database type
    window = ViewPropertyWindow(selected_channels, database_type)
    window.show()
    sys.exit(app.exec_())
