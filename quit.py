from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow

QUIT_FILE = "./UI_Files/QuitFrame.ui"


class QuitFrame(QMainWindow):
    def __init__(self, ui):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(QUIT_FILE, self)
        ui.setDisabled(True)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.Accept.clicked.connect(lambda: self.AcceptQuit(ui))
        self.Deny.clicked.connect(lambda: self.deny(ui))

    def AcceptQuit(self, ui):
            if ui.pg:
                ui.pg.close()
            ui.close()
            self.close()

    def deny(self, ui):
        self.close()
        ui.setDisabled(False)