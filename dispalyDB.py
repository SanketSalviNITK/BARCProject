import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QLabel

class DatabaseViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reactor Data Viewer")
        self.setGeometry(100, 100, 1200, 600)

        # Layout and widgets
        self.layout = QVBoxLayout()
        self.table_selector = QComboBox()
        self.table_selector.addItems([
            "reactor_data_min_thickness",
            "reactor_data_max_thickness",
            "reactor_data_min_inner_diameter",
            "reactor_data_max_inner_diameter",
            "reactor_data_avg_outside_diameter"
        ])
        self.table_selector.currentIndexChanged.connect(self.load_table_data)

        self.table_widget = QTableWidget()
        self.layout.addWidget(QLabel("Select Table:"))
        self.layout.addWidget(self.table_selector)
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)

        # Load initial data
        self.load_table_data()

    def load_table_data(self):
        table_name = self.table_selector.currentText()
        connection = sqlite3.connect('reactor_data.db')
        cursor = connection.cursor()

        # Fetch data from the selected table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        # Set table widget dimensions
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

        # Close the database connection
        connection.close()

# Initialize and run the application
app = QApplication(sys.argv)
viewer = DatabaseViewer()
viewer.show()
sys.exit(app.exec_())
