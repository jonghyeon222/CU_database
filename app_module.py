import sys
from PyQt5.QtWidgets import QApplication
from login_module import LoginDialog
from main import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginDialog()
    if login.exec_() == LoginDialog.Accepted:
        w = MainWindow()
        w.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)