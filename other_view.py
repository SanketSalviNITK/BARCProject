import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore


class EditPropertyWindow(QtWidgets.QWidget):
    def __init__(self, username, reactor_type, reactor_name, selected_channels, database_type):
        super().__init__()
        self.setWindowTitle("View Properties")
        self.setGeometry(100, 100, 1200, 600)
        self.username = username
        self.selected_channels = selected_channels
        self.database_type = database_type
        self.selected_channel = ""
        self.selected_property = ""

        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Create horizontal layout for channel frame and table
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
        self.channel_frame.setFixedWidth(120)
        self.horizontal_layout.addWidget(self.channel_frame)

        # Frame for table to display data
        self.table_frame = QtWidgets.QFrame(self)
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

        self.horizontal_layout.addWidget(self.table_frame)
        self.main_layout.addLayout(self.horizontal_layout)

        # Create footer frame for Back button
        self.footer_frame = QtWidgets.QFrame(self)
        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_frame)

        # Back button
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setFixedSize(80, 30)  # Set size for Back button
        self.back_button.clicked.connect(self.go_back)
        self.footer_layout.addWidget(self.back_button)

        self.main_layout.addWidget(self.footer_frame)

    def go_back(self):
        """Close the current window and go back to the previous window."""
        self.close()

    def populate_table(self, channel):
        """Fetch data from the database and populate the TableView for the selected channel."""
        # Check if a channel is selected
        if not channel or not self.database_type:
            return

        conn = sqlite3.connect('iphwr_analysis.db')
        cursor = conn.cursor()

        # Define the columns for the table
        headers = [
            'Channel ID', 'Property Name', 'Year', 'HOY', 'Length', 'Entry By', 'Entry Date', 'Remark',
            'Cell1', 'Cell2', 'Cell3', 'Cell4', 'Cell5', 'Cell6', 'Cell7', 'Cell8', 'Cell9', 'Cell10',
            'Cell11', 'Cell12', 'Cell13', 'Cell14', 'Cell15', 'Cell16', 'Cell17', 'Cell18', 'Cell19',
            'Cell20', 'Cell21', 'Cell22', 'Cell23', 'Cell24'
        ]

        # Set column count and headers
        self.tree.setColumnCount(len(headers))
        self.tree.setHorizontalHeaderLabels(headers)

        # Clear the current table
        self.tree.setRowCount(0)  # Clear existing data in the table

        # Fetch data for the selected channel
        query = "SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10, Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties WHERE channel_id=?"
        cursor.execute(query, (channel,))
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
        self.selected_channel = selected_channel
        self.populate_table(selected_channel)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditPropertyWindow(["Example_Channel", "Channel_2"], "Type A")
    window.show()
    sys.exit(app.exec_())
