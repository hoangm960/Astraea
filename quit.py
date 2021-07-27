from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,

QUIT_FILE = "./UI_Files/QuitFrame.ui"


class QuitFrame(QMainWindow):
    def __init__(self, ui):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(QUIT_FILE, self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        def AcceptQuit():
            if ui.pg:
                ui.pg.close()
            ui.close()
            self.close()
        self.Accept.clicked.connect(lambda: AcceptQuit())
        self.Deny.clicked.connect(lambda: self.close())