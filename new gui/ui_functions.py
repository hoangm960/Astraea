from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QResizeEvent
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QSizeGrip
from main import *

GLOBAL_STATE = False

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
        self.ui.btn_quit.clicked.connect(lambda: self.close())

    def returnStatus():
        return GLOBAL_STATE