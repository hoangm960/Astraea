import os
import pickle
import sys

import mammoth
import pyautogui
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsDropShadowEffect, QFileDialog,
                             QMainWindow, QLineEdit, QListWidgetItem, QVBoxLayout)

import main_ui
from win32com import client as wc

DOC_PATH = "./UI_Files/Doc.ui"
HTML_CONVERT_PATH = "./data/html_convert"


class DocWindow(QMainWindow):
    def __init__(self, role, name):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_PATH, self)
        self.role = role
        self.name = name
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
        cls.load_assignments(
            ui, open(main_ui.OPENED_LESSON_PATH).read().rstrip())
        cls.define_role(ui)

    @classmethod
    def close_pg(cls, ui):
        ui.close()
        main_ui.main(ui.role, ui.name)

    @classmethod
    def load_assignments(cls, ui, filename):
        ui.titles.clear()
        cls.docs.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    for i in range(1, len(cls.docs) + 1):
                        ui.titles.addItem(str(i))
    

    class TeacherUiFunctions:
        def __init__(self, ui):
            self.connect_btn(ui)
        
        
        def show_file_dialog(self, ui):
            HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            file_path = QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, "*.docx")[0]
            if file_path:
                self.load_doc(ui, file_path)    

        def load_doc(self, ui, filename):
            ui.text_entry.setText(self.get_html(filename))

        @staticmethod
        def convert_doc_to_html(filename):
            html_file = f"{os.path.splitext(filename)[0]}.html"

            word = wc.Dispatch('Word.Application') 
            doc = word.Documents.Open(filename)
            doc.SaveAs(html_file, 8) 
            doc.Close() 
            word.Quit()

            return html_file

        def get_html(self, filename):
            with open(self.convert_doc_to_html(filename), 'r') as f:
                return f.read()

        def add_titles(self, ui):
            title = QLineEdit()
            title_item = QListWidgetItem()
            ui.titles.insertItem(ui.titles.count(), title_item)
            ui.titles.setItemWidget(title_item, title)

        def connect_btn(self, ui):
            ui.add_btn.clicked.connect(lambda: self.add_titles(ui))
            ui.load_btn.clicked.connect(lambda: self.show_file_dialog(ui))
            ui.titles.itemPressed.connect(lambda: self.load_doc(ui))

    class StudentUiFunctions:
        def __init__(self, ui):
            ui.confirm_frame.close()

    @classmethod
    def define_role(cls, ui):
        if ui.role.lower() == "teacher":
            cls.TeacherUiFunctions(ui)
        if ui.role.lower() == "student":
            cls.StudentUiFunctions(ui)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocWindow("teacher",'mineshark15@gmail.com')
    window.show()
    sys.exit(app.exec_())
