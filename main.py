import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and display the login window
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())

