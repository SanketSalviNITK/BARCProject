from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

def add_company_footer(main_layout):
    """
    Adds the 'Developed by SVR Infotech' footer to the provided main layout.
    The footer will be fixed at the bottom-left side of the window.
    
    Parameters:
        main_layout (QVBoxLayout): The main layout of the window where the footer should be added.
    """
    # Create the company label
    company_label = QLabel("Developed by SVR Infotech")
    company_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
    company_label.setAlignment(Qt.AlignLeft)

    # Create a footer layout for the company label
    footer_layout = QHBoxLayout()
    footer_layout.addWidget(company_label)
    footer_layout.addStretch(1)  # Push any other content to the right (if present)

    # Add a spacer to push the footer to the bottom of the window
    spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    main_layout.addSpacerItem(spacer_item)  # This ensures that the footer is pushed to the bottom

    # Add the footer layout to the main layout
    main_layout.addLayout(footer_layout)
