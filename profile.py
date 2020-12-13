import os
import pickle
import time
from encryption import decrypt, encrypt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys

UI_PATH = './UI_Files/profile_form.ui'
USER_PATH = './data/Users/opened_user.ou'
class ProfileWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_PATH, self)
        UIFunctions.uiDefinitions(self)
class UIFunctions(ProfileWindow):
    @classmethod
    def uiDefinitions(cls, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        cls.Update(ui)
        ui.Save_btn.setDisabled(True)

    @classmethod 
    def Update(cls, ui):
        with open(USER_PATH, 'r', encoding = 'utf-8') as f:
            name = f.readline().rstrip()
            ui.NameBox.setText(name)
            id = f.readline().rstrip()
            ui.IDBox.setText(id)
            password = f.readline().rstrip()
            ui.PassBox.setText(password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileWindow()
    window.show()
    sys.exit(app.exec_())

