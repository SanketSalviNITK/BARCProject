import pandas as pd
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMessageBox

class DataDisplay:
    def __init__(self, tree_widget):
        # Pass the QTreeWidget from the main window
        self.tree_widget = tree_widget

    def display_exported_data(self, file_path):
        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file_path)

            # Clear the existing data in the tree widget
            self.tree_widget.clear()

            # Set the headers for the QTreeWidget based on the dataframe columns
            self.tree_widget.setHeaderLabels(df.columns)

            # Insert rows into the tree widget
            for _, row in df.iterrows():
                item = QTreeWidgetItem([str(value) for value in row.tolist()])
                self.tree_widget.addTopLevelItem(item)

        except Exception as e:
            # Display error message in case of failure
            QMessageBox.critical(None, "Error", f"Failed to display exported data: {str(e)}")

