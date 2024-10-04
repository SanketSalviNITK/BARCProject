# load_220_iphwr.py

from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from load_core_layout import CoreLayoutWindow  # Ensure correct import

def load_220_iphwr(sub_layout_2,reactor_type):
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
    reactor_buttons = [
        "RAPS-1", "RAPS-2", "RAPS-3", "RAPS-4",
        "RAPS-5", "RAPS-6", "MAPS-1", "MAPS-2",
        "KAPS-1", "KAPS-2", "KGS-1", "KGS-2",
        "KGS-3", "KGS-4", "NAPS-1", "NAPS-2"
    ]

    # Add buttons to the grid layout
    for index, button_name in enumerate(reactor_buttons):
        button = QPushButton(button_name)
        button.clicked.connect(lambda checked, name=button_name: button_clicked(name, reactor_type))  
        grid_layout.addWidget(button, index // 4, index % 4)  # 4x4 layout

    # Update the layout
    sub_layout_2.addLayout(grid_layout)
    
    
    # Function to handle button click
def button_clicked(button_name,reactor_type):
    print(f"{reactor_type} {button_name} is clicked")
    core_layout_window = CoreLayoutWindow(None, reactor_type, button_name, mode="edit")  # Pass `self` as the parent
    core_layout_window.show()