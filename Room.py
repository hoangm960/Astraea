import os
import pickle
import sys
from datetime import datetime

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


class RoomWindow(QMainWindow):
    ROOM_UI = "./UI_Files/Room.ui"
    def __init__(self, id, role, pg, connection):
        self.id = id
        self.role = role
        self.pg = pg 
        self.connection = connection
        super(RoomWindow, self).__init__()
        uic.loadUi(self.ROOM_UI, self)
        UIFunctions(self)
class UIFunctions(RoomWindow):
    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.showMaximized()
        ui.ID_Room.setText(ui.id)
    @staticmethod
    def close_pg(ui):
        import main_ui
        main_ui.main(ui.role, ui.pg, ui.connection)
        ui.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RoomWindow('123ABCD63NG')
    window.show()
    sys.exit(app.exec_())
