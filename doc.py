import os
import pickle
import sys

import docx
import mammoth
import pyautogui
from docx import Document
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsDropShadowEffect,
                             QMainWindow)

import main_ui

DOC_PATH = "./UI_Files/Doc.ui"


class DocWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(DOC_PATH, self)
        UIFunctions.uiDefinitions(self)


class UIFunctions(DocWindow):
    STATUS = True
    assignments = {}

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
        ui.assignments.itemPressed.connect(lambda: cls.load_doc(ui, "test.docx"))
        cls.load_assignments(ui, open(main_ui.OPENED_LESSON_PATH).read().rstrip())


    @classmethod
    def close_pg(cls, ui):
        ui.close()
        main_ui.main("student")

    @classmethod
    def load_assignments(cls, ui, filename):
        ui.assignments.clear()
        cls.assignments.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    title = data[0]
                    assignments = data[1]
                    for assignment in assignments:
                        cls.assignments[assignment.name] = assignment.details
                        ui.assignments.addItem(assignment.name)

    @classmethod
    def load_doc(cls, ui, filename):
        f = open(filename, 'rb')
        html_filename = os.path.splitext(filename)[0] + '.html'
        b = open(html_filename, 'wb')
        document = mammoth.convert_to_html(f)
        b.write(document.value.encode('utf8'))
        f.close()
        b.close()
        
        ui.text_entry.setSource(QtCore.QUrl.fromLocalFile(html_filename))
