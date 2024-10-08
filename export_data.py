import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
    QTableWidget,
    QApplication,
    QMainWindow
)

from display_exported__data import disp_exported_data


class ExportData(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize QTableWidget
        self.table_widget = QTableWidget(self)
        self.setCentralWidget(self.table_widget)

    def export_to_excel(self, selected_channel, selected_property):
        try:
            if selected_property == "":
                QMessageBox.critical(self, "Error", "Property must be selected.")
                return
            
            conn = sqlite3.connect('iphwr_analysis.db')
            query = "SELECT * FROM properties WHERE channel_id = ? AND property_name = ?"
            df = pd.read_sql_query(query, conn, params=(selected_channel, selected_property))
            conn.close()

            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
            if file_path:
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", f"Data exported successfully to {file_path}.")
                disp_exported_data(file_path)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")
