import sys
import sqlite3
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox

def Show_Graph(self, cursor, selected_channel, selected_property):
    # Ensure a channel is selected
    print("In Show_Graph: ",selected_channel,selected_property)
    if not selected_channel:
        QMessageBox.critical(self, "Error", "Please select a channel.")
        return
    if selected_property=="":
        QMessageBox.critical(self, "Error", "Please select a property.")
        return
    
    conn = sqlite3.connect('iphwr_analysis.db')
    cursor = conn.cursor()
    
    if selected_channel and selected_property:
        try:
            # Query to retrieve data from the database
            query = """
            SELECT  'Cell1', 'Cell2', 'Cell3', 'Cell4', 'Cell5', 'Cell6', 'Cell7', 'Cell8', 'Cell9', 'Cell10',
            'Cell11', 'Cell12', 'Cell13', 'Cell14', 'Cell15', 'Cell16', 'Cell17', 'Cell18', 'Cell19',
            'Cell20', 'Cell21', 'Cell22', 'Cell23', 'Cell24' FROM properties
            WHERE channel_id = ? AND property_name = ?
            """

            cursor.execute(query, (selected_channel, selected_property))
            rows = cursor.fetchall()
            conn.close()
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

            # Display the plot in a new window
            plot_window = QDialog(self)
            plot_window.setWindowTitle("Graph")
            layout = QVBoxLayout()

            # Matplotlib canvas
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
            plot_window.setLayout(layout)
            plot_window.resize(800, 600)
            plot_window.exec_()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot graph: {e}")
