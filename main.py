import os
import subprocess
import sys

import win32con
import win32gui
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsDropShadowEffect,
                             QMainWindow, QSizeGrip)

from main import *
from ui_main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        UIFunctions.uiDefinitions(self)


class UIFunctions(MainWindow):
    def uiDefinitions(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.ui.bg_frame.setGraphicsEffect(self.shadow)

        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_quit.clicked.connect(lambda: UIFunctions.close_pg(self))

        UIFunctions.open_vscode()
        #fix here
        UIFunctions.load_assignments(self, "Text.txt")
        with open("text2.txt") as f:
            self.ui.assignment_details.setDocument(f.read())
        

    @classmethod
    def open_vscode(cls):
        file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
        subprocess.call(file)
        cls.pg = win32gui.FindWindow(None, 'Visual Studio Code')
        x0, y0, x1, y1 = win32gui.GetWindowRect(cls.pg)
        w = x1 - x0
        h = y1 - y0
        win32gui.MoveWindow(cls.pg, 0, 0, w + 50, h, True)

    @classmethod
    def close_pg(cls, self):
        win32gui.PostMessage(cls.pg, win32con.WM_CLOSE,0,0)
        self.close()

    @classmethod
    def load_assignments(cls, self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.ui.list_assignments.addItem(line)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.move(1070, 0)
    window.show()
    sys.exit(app.exec_())

