from PyQt6 import QtWidgets
from controller import Controller

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec())
