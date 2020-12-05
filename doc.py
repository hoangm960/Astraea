import os
import pickle
import sys

import mammoth
import pyautogui
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsDropShadowEffect,
                             QMainWindow)

import main_ui
from win32com import client as wc

DOC_PATH = "./UI_Files/Doc.ui"
HTML_CONVERT_PATH = "./data/html_convert"


class DocWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_PATH, self)
        UIFunctions.uiDefinitions(self)


class UIFunctions(DocWindow):
    assignments = {}

    @classmethod
    def uiDefinitions(cls, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
            round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
            round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )
        ui.showMaximized()
        ui.btn_quit.clicked.connect(lambda: cls.close_pg(ui))
        ui.assignments.itemPressed.connect(lambda: cls.load_doc(
            ui, "D:/Programming/Python/Astraea/bruh.docx"))
        cls.load_assignments(
            ui, open(main_ui.OPENED_LESSON_PATH).read().rstrip())

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
        html_file = f"{os.path.join(os.path.abspath(HTML_CONVERT_PATH), os.path.splitext(os.path.basename(filename))[0])}.html"
        
        word = wc.Dispatch('Word.Application') 
        doc = word.Documents.Open(filename)
        doc.SaveAs(html_file, 8) 
        doc.Close() 
        word.Quit()

        ui.text_entry.setSource(QtCore.QUrl.fromLocalFile(html_file))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocWindow()
    window.show()
    sys.exit(app.exec_())
