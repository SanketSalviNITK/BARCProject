import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel

class DatabaseViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.database = "reactor_data.db"  # Adjust the database name as needed
    
    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout()

        # Label
        self.label = QLabel("Joined Data:")
        self.layout.addWidget(self.label)

        # Button to load joined data
        self.load_joined_data_btn = QPushButton("Load Joined Data")
        self.load_joined_data_btn.clicked.connect(self.load_joined_data)
        self.layout.addWidget(self.load_joined_data_btn)

        # Table to display joined data
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Set layout
        self.setLayout(self.layout)
        self.setWindowTitle("Database Viewer")
        self.resize(800, 600)

    def load_joined_data(self):
        # Example SQL to perform the join
        join_query = """
            SELECT 
                min_thickness.channel_id,
                min_thickness.property_name,
                min_thickness.database_type,
                min_thickness.Cell1_Position_mm,
                min_thickness.Cell1_Min_Thickness_mm,
                max_thickness.Cell1_Max_Thickness_mm
            FROM 
                reactor_data_min_thickness AS min_thickness
            JOIN 
                reactor_data_max_thickness AS max_thickness 
            ON 
                min_thickness.channel_id = max_thickness.channel_id;
        """
        
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(join_query)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

        # Set up the table widget with the joined data
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.show()
    sys.exit(app.exec_())
