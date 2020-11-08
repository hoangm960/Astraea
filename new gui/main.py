import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui_functions import *
from ui_main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        UIFunctions.uiDefinitions(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.move(1070, 0)
    window.show()
    sys.exit(app.exec_())

