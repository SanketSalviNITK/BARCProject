# load_220_iphwr.py

from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from load_core_layout import CoreLayoutWindow  # Ensure correct import

def load_220_iphwr(self, sub_layout_2, reactor_type, username):
    # Clear the existing layout content
    while sub_layout_2.count():
        item = sub_layout_2.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

    # Create a label for the 220 IPHWR title
    title_label = QLabel(reactor_type)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setStyleSheet("font-size: 26px; color: #34495e; font-weight: bold; margin-bottom: 20px;")  # Style the title
    sub_layout_2.addWidget(title_label)

    # Create a grid layout for reactor buttons
    grid_layout = QGridLayout()
    grid_layout.setSpacing(15)  # Add spacing between buttons
    grid_layout.setContentsMargins(20, 20, 20, 20)  # Set margins for the grid layout

    # Reactor buttons
    reactor_buttons = [
        "RAPS-1", "RAPS-2", "RAPS-3", "RAPS-4",
        "RAPS-5", "RAPS-6", "MAPS-1", "MAPS-2",
        "KAPS-1", "KAPS-2", "KGS-1", "KGS-2",
        "KGS-3", "KGS-4", "NAPS-1", "NAPS-2"
    ]

    # Add buttons to the grid layout
    for index, button_name in enumerate(reactor_buttons):
        button = QPushButton(button_name)
        button.setFixedSize(120, 50)  # Set a larger fixed size for buttons
        button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;  /* Primary color */
                color: white;
                border-radius: 12px;  /* Rounded corners */
                font-size: 16px;
                font-weight: bold;
                padding: 10px;  /* Inner padding for button text */
            }
            QPushButton:hover {
                background-color: #2980b9;  /* Darker shade on hover */
            }
            QPushButton:pressed {
                background-color: #1c6f94;  /* Even darker when pressed */
            }
        """)
        button.clicked.connect(lambda checked, reactor_name=button_name: button_clicked(username, reactor_name, reactor_type))  
        grid_layout.addWidget(button, index // 4, index % 4)  # 4x4 layout

    # Update the layout
    sub_layout_2.addLayout(grid_layout)

def button_clicked(username, reactor_name, reactor_type):
    print(f"User {username} has {reactor_type} {reactor_name} clicked.")
    core_layout_window = CoreLayoutWindow(None, username, reactor_type, reactor_name, mode="edit")  # Pass `self` as the parent
    core_layout_window.show()
