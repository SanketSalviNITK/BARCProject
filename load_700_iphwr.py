# load_700_iphwr.py

from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from load_core_layout import CoreLayoutWindow  # Ensure correct import

def load_700_iphwr(self,sub_layout_2,reactor_type, username):
    # Clear the existing layout content
    while sub_layout_2.count():
        item = sub_layout_2.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

    # Create a label for the 220 IPHWR title
    title_label = QLabel(reactor_type)
    title_label.setAlignment(Qt.AlignCenter)
    sub_layout_2.addWidget(title_label)

    # Create a grid layout for reactor buttons
    grid_layout = QGridLayout()

    # Reactor buttons
    reactor_buttons = ["KAPS-3", "KAPS-4", "RAPS-7", "RAPS-8", "KGS-5", "KGS-6"]

    # Add buttons to the grid layout
    for index, button_name in enumerate(reactor_buttons):
        button = QPushButton(button_name)
        button.clicked.connect(lambda checked,  reactor_name=button_name: button_clicked(username, reactor_name, reactor_type))
        grid_layout.addWidget(button, index // 4, index % 4)  # 4x4 layout

    # Update the layout
    sub_layout_2.addLayout(grid_layout)
    
    
# Function to handle button click
def button_clicked(username, reactor_name,reactor_type):
    print(f"User {username} has {reactor_type} {reactor_name} is clicked")
    core_layout_window = CoreLayoutWindow(None, username, reactor_type, reactor_name, mode="edit")  # Pass `self` as the parent
    core_layout_window.show()