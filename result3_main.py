from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip
import sys
from win32api import GetSystemMetrics
class ResultWindow(QMainWindow):
    UI_Window = 'UI_Files/result_form.ui'
    state_Window = False
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(self.UI_Window, self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(
            round((GetSystemMetrics(0) - self.width()) / 3),
            round((GetSystemMetrics(1) - self.height()) / 2),
            self.width(),
            self.height(),
        )
        def changedstate():
            if self.state_Window is True:
                self.state_Window = False
                self.showNormal()
            else:
                self.state_Window = True
                self.showMaximized()
        
        self.btn_quit.clicked.connect(lambda: self.close())
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_maximize.clicked.connect(lambda: changedstate())
        
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }"
        )
        self.sizegrip.setToolTip("Resize Window")
        
def main():
    app = QApplication(sys.argv)
    window = ResultWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()