import sys

from PyQt5 import QtCore, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect, QMainWindow
import main_ui
import pyautogui

DOC_PATH = "./UI_Files/Doc.ui"


class DocWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(DOC_PATH, self)
        UIFunctions.uiDefinitions(self)

class UIFunctions(DocWindow):
    STATUS = True
    @classmethod
    def uiDefinitions(cls, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
        round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
        round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        def status_change():
            if cls.STATUS == True:
                ui.showMaximized()
                ui.btn_maximize.setToolTip('Phóng to')
                cls.STATUS = False
            else:
                ui.showNormal()
                ui.btn_minimize.setToolTip('Thu nhỏ')
                cls.STATUS = True
        ui.btn_maximize.clicked.connect(lambda: status_change())
        ui.btn_quit.clicked.connect(lambda: cls.close_pg(ui))
    @classmethod
    def close_pg(cls, ui):
        try:
            cls.pg.close()
        except:
            pass
        ui.close()    
   



