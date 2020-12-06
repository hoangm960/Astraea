import os
import pickle
import sys

import mammoth
import pyautogui
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsDropShadowEffect, QFileDialog,
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
    docs = {}

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
            ui))
        cls.load_assignments(
            ui, open(main_ui.OPENED_LESSON_PATH).read().rstrip())

    @classmethod
    def close_pg(cls, ui):
        ui.close()
        main_ui.main("student")

    @classmethod
    def load_assignments(cls, ui, filename):
        ui.assignments.clear()
        cls.docs.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    for i in range(1, len(cls.docs) + 1):
                        ui.assignments.addItem(str(i))

    @classmethod
    def load_doc(cls, ui):
        with open(HTML_CONVERT_PATH, 'w') as f:
            f.write(cls.docs[1])            
        ui.text_entry.setSource(QtCore.QUrl.fromLocalFile(HTML_CONVERT_PATH))

    @classmethod
    def convert_doc_to_html(cls, filename):
        html_file = f"{os.path.splitext(filename)[0]}.html"

        word = wc.Dispatch('Word.Application') 
        doc = word.Documents.Open(filename)
        doc.SaveAs(html_file, 8) 
        doc.Close() 
        word.Quit()

        return html_file

    @classmethod
    def show_file_dialog(cls, ui, filename):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, "*.docx")[0]
        if file_path:
            with open(filename, "w") as f:
                f.write(file_path)
            cls.load_assignments(ui, file_path)
    # class TeacherUiFunctions:
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocWindow()
    window.show()
    sys.exit(app.exec_())
