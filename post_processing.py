import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout, QLineEdit, QGroupBox, QFrame
from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QFrame

class RxRunningOutputPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a group box to group the panel
        group_box = QGroupBox("Rx Running Output Panel")

        # Create grid layout inside the group box
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)  # Minimize the spacing between elements
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margin

        # Add labels and values for the Rx Running Output Panel
        labels = [
            "N Moment PT (kNm)", "F Moment PT (kNm)", "N Moment CT (kNm)", "F Moment CT (kNm)",
            "N Reaction PT (kN)", "F Reaction PT (kN)", "N Reaction CT (kN)", "F Reaction CT (kN)"
        ]
        values = [
            "-0.47", "0", "-0.35", "0",
            "0.67", "0.5", "0.22", "0.37"
        ]

        # Adding the rows with minimized spacing and group formatting
        for i in range(4):  # First row
            grid_layout.addWidget(QLabel(labels[i]), 0, i)
            value_box = QLineEdit(values[i])
            value_box.setReadOnly(True)  # Make it read-only
            value_box.setStyleSheet("color: orange; font-weight: bold; padding: 2px;")  # Reduced padding
            value_box.setFixedWidth(80)  # Set fixed width for the text box
            grid_layout.addWidget(value_box, 1, i)

        for i in range(4, 8):  # Second row
            grid_layout.addWidget(QLabel(labels[i]), 2, i-4)
            value_box = QLineEdit(values[i])
            value_box.setReadOnly(True)
            value_box.setStyleSheet("color: orange; font-weight: bold; padding: 2px;")  # Reduced padding
            value_box.setFixedWidth(80)  # Set fixed width for the text box
            grid_layout.addWidget(value_box, 3, i-4)

        # Create Max Deflection section frame without border
        max_deflection_frame = QFrame()
        max_deflection_layout = QGridLayout(max_deflection_frame)

        max_deflection_label = QLabel("Max Deflection (mm)")
        max_deflection_layout.addWidget(max_deflection_label, 0, 0, 1, 2)  # Span across two columns
        
        pt_rr_label = QLabel("PT RR Value:")
        pt_rr_value = QLineEdit("-8.88")
        pt_rr_value.setReadOnly(True)
        pt_rr_value.setStyleSheet("color: orange; font-weight: bold; padding: 2px;")  # Reduced padding
        pt_rr_value.setFixedWidth(80)  # Set fixed width for the text box
        
        ct_rr_label = QLabel("CT RR Value:")
        ct_rr_value = QLineEdit("-6.77")
        ct_rr_value.setReadOnly(True)
        ct_rr_value.setStyleSheet("color: orange; font-weight: bold; padding: 2px;")  # Reduced padding
        ct_rr_value.setFixedWidth(80)  # Set fixed width for the text box

        # Add Max Deflection labels and values to the Max Deflection frame layout
        max_deflection_layout.addWidget(pt_rr_label, 1, 0)
        max_deflection_layout.addWidget(pt_rr_value, 1, 1)

        max_deflection_layout.addWidget(ct_rr_label, 2, 0)
        max_deflection_layout.addWidget(ct_rr_value, 2, 1)

        # Adding alignment to right side
        max_deflection_layout.addWidget(QLabel(" "), 1, 2)  # Empty space for padding
        max_deflection_layout.addWidget(QLabel(" "), 2, 2)  # Empty space for padding

        # Adding Max Deflection frame to the main grid layout
        grid_layout.addWidget(max_deflection_frame, 4, 0, 1, 4)  # Span across the full width

        group_box.setLayout(grid_layout)
        self.layout = QVBoxLayout()
        self.layout.addWidget(group_box)
        self.setLayout(self.layout)


class ISIOutputPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a group box to group the panel
        group_box = QGroupBox("ISI Output Panel")
        
        # Create grid layout inside the group box
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)  # Minimize the spacing between elements
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margin
        
        # Add labels and values for the ISI Output Panel
        labels = [
            "N Moment PT (kNm)", "F Moment PT (kNm)", "N Moment CT (kNm)", "F Moment CT (kNm)",
            "N Reaction PT (kN)", "F Reaction PT (kN)", "N Reaction CT (kN)", "F Reaction CT (kN)",
        ]
        values = [
            "-0.17", "0", "-0.03", "0",
            "0.27", "-0.06", "-0.11", "0.11"
        ]

        # Adding the rows with minimized spacing and group formatting
        for i in range(4):  # First row
            grid_layout.addWidget(QLabel(labels[i]), 0, i)
            value_box = QLineEdit(values[i])
            value_box.setReadOnly(True)  # Make it read-only
            value_box.setStyleSheet("color: orange; font-weight: bold; padding: 5px;")
            value_box.setFixedSize(80, 30)  # Set fixed size (width, height)
            grid_layout.addWidget(value_box, 1, i)

        for i in range(4, 8):  # Second row
            grid_layout.addWidget(QLabel(labels[i]), 2, i-4)
            value_box = QLineEdit(values[i])
            value_box.setReadOnly(True)
            value_box.setStyleSheet("color: orange; font-weight: bold; padding: 5px;")
            value_box.setFixedSize(80, 30)  # Set fixed size (width, height)
            grid_layout.addWidget(value_box, 3, i-4)

        # Adding the Max Deflection common heading
        max_deflection_label = QLabel("Max Deflection (mm)")
        max_deflection_label.setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        grid_layout.addWidget(max_deflection_label, 4, 0, 1, 2)  # Span across two columns

        # Adding PT and CT labels for Max Deflection
        grid_layout.addWidget(QLabel("PT"), 5, 0)  # Label for PT
        grid_layout.addWidget(QLabel("CT"), 5, 1)  # Label for CT

        # Adding Max Deflection values
        pt_deflection_value = QLineEdit("-5.11")
        pt_deflection_value.setReadOnly(True)
        pt_deflection_value.setStyleSheet("color: orange; font-weight: bold; padding: 5px;")
        pt_deflection_value.setFixedSize(80, 30)
        grid_layout.addWidget(pt_deflection_value, 6, 0)  # Value for PT

        ct_deflection_value = QLineEdit("-2.58")
        ct_deflection_value.setReadOnly(True)
        ct_deflection_value.setStyleSheet("color: orange; font-weight: bold; padding: 5px;")
        ct_deflection_value.setFixedSize(80, 30)
        grid_layout.addWidget(ct_deflection_value, 6, 1)  # Value for CT

        group_box.setLayout(grid_layout)
        self.layout = QVBoxLayout()
        self.layout.addWidget(group_box)
        self.setLayout(self.layout)



class GSOutputPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a group box for the GS Output Panel
        group_box = QGroupBox("GS Output Panel")
       
        # Create grid layout inside the group box
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        # Labels and values for the output, structured like the image
        gs_labels = ["GS Position (mm)", "GS Reaction (kN)", "GS Reaction ISI (kN)"]
        gs_positions = ["1250.0", "2150.0", "3050.0", "3950.0"]
        gs_reactions = ["0.01", "0.37", "0.39", "0.2"]
        gs_reaction_isi = ["-0.3", "0.49", "0.0", "0.19"]
        gs_names = ["GS1", "GS2", "GS3", "GS4"]

        # Add header labels
        for i, label in enumerate(gs_labels):
            grid_layout.addWidget(QLabel(label), i + 1, 0, 1, 1)

        # Add GS column values
        for j, gs_name in enumerate(gs_names):
            grid_layout.addWidget(QLabel(gs_name), 0, j + 1)  # GS1, GS2...
            value_box_pos = QLineEdit(gs_positions[j])
            value_box_pos.setReadOnly(True)
            value_box_pos.setStyleSheet("color: orange; font-weight: bold; border: 2px solid gray; padding: 5px;")
            grid_layout.addWidget(value_box_pos, 1, j + 1)

            value_box_react = QLineEdit(gs_reactions[j])
            value_box_react.setReadOnly(True)
            value_box_react.setStyleSheet("color: orange; font-weight: bold; border: 2px solid gray; padding: 5px;")
            grid_layout.addWidget(value_box_react, 2, j + 1)

            value_box_isi = QLineEdit(gs_reaction_isi[j])
            value_box_isi.setReadOnly(True)
            value_box_isi.setStyleSheet("color: orange; font-weight: bold; border: 2px solid gray; padding: 5px;")
            grid_layout.addWidget(value_box_isi, 3, j + 1)

        group_box.setLayout(grid_layout)
        self.layout = QVBoxLayout()
        self.layout.addWidget(group_box)
        self.setLayout(self.layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        # Create Post Processing button
        self.post_processing_btn = QPushButton("Post Processing")
        self.post_processing_btn.clicked.connect(self.open_all_panels)
        self.main_layout.addWidget(self.post_processing_btn)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Post Processing Window")
        self.setGeometry(100, 100, 800, 600)

    def open_all_panels(self):
        # Remove existing widgets, keep the button
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget and widget is not self.post_processing_btn:
                widget.setParent(None)

        # Create instances of the panels
        rx_panel = RxRunningOutputPanel()
        isi_panel = ISIOutputPanel()
        gs_panel = GSOutputPanel()

        # Add all panels to the main layout
        self.main_layout.addWidget(rx_panel)
        self.main_layout.addWidget(isi_panel)
        self.main_layout.addWidget(gs_panel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
