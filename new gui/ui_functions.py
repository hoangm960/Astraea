from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QResizeEvent
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QSizeGrip
from main import *

GLOBAL_STATE = False

class UIFunctions(MainWindow):
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE

        if status == False:
            self.showMaximized()

            GLOBAL_STATE = True
            
            self.ui.drop_shadow_layout.setContentsMargins(0, 0, 0, 0)
            self.ui.drop_shadow_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 0px;")
            self.ui.btn_maximize.setToolTip("Restore")
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
            self.ui.drop_shadow_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.341, x2:1, y2:0.897, stop:0 rgba(97, 152, 255, 255), stop:0.514124 rgba(186, 38, 175, 255), stop:1 rgba(255, 0, 0, 255)); border-radius: 20px;")
            self.ui.btn_maximize.setToolTip("Maximize")

    def uiDefinitions(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)

        self.ui.btn_maximize.clicked.connect(lambda: UIFunctions.maximize_restore(self))
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_quit.clicked.connect(lambda: self.close())

        self.sizegrip = QSizeGrip(self.ui.frame_grip)
        self.sizegrip.setStyleSheet("QSizeGrip { width: 10px; height: 10px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(201, 21, 8) }")
        self.sizegrip.setToolTip("Resize Window")

    def returnStatus():
        return GLOBAL_STATE