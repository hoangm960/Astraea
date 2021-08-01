from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow

QUIT_FILE = "./UI_Files/QuitFrame.ui"


class QuitFrame(QMainWindow):
    close_window = QtCore.pyqtSignal()
    reset_state = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(QUIT_FILE, self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.Accept.clicked.connect(self.AcceptQuit)
        self.Deny.clicked.connect(self.DenyQuit)

    def AcceptQuit(self):
        self.close_window.emit()

    def DenyQuit(self):
        self.close()
        self.reset_state.emit()
