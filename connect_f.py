
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QListWidgetItem, QMainWindow)

import main_ui

CONNECT_UI = "./UI_Files/connect.ui"

class ConnectWindow(QMainWindow):
    def __init__(self, pg):
        self.pg = pg
        QMainWindow.__init__(self)
        uic.loadUi(CONNECT_UI, self)
        
        
        UIFunctions(self)


class UIFunctions(ConnectWindow):

    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
            round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
            round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))

    def close_pg(self, ui):
        ui.close()
        main_ui.main('student', ui.pg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConnectWindow(None)
    window.show()
    sys.exit(app.exec_())
