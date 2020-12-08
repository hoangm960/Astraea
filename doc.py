import os
import pickle
import shutil
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QFileDialog,
                             QMainWindow, QLineEdit, QListWidgetItem, QLabel)

import main_ui
from win32com import client as wc

DOC_UI = "./UI_Files/Doc.ui"
HTML_CONVERT_PATH = "./data/html_convert"


class DocWindow(QMainWindow):
    def __init__(self, role, name):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_UI, self)
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

        def open_doc(self, ui):
            if ui.titles.selectedItems():
                file_path = self.show_file_dialog(ui)
                if file_path:
                    self.load_doc(ui, file_path)
                    self.delete_html_file(file_path)

        @staticmethod
        def show_file_dialog(ui):
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_path = QFileDialog.getOpenFileName(
                ui, "Open file", HOME_PATH, "*.docx")[0]
            return file_path

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

        @staticmethod
        def check_empty(ui):
            return True if ui.titles.currentItem().text() in UIFunctions.docs else False

        def load_doc(self, ui, filename):
            if not self.check_empty(ui):
                html_data = self.get_html(filename)
                UIFunctions.docs[ui.titles.currentItem().text()] = html_data
                ui.text_entry.setText(html_data)
            else:
                ui.text_entry.setText(
                    UIFunctions.docs[ui.titles.currentItem().text()])

        @staticmethod
        def delete_html_file(filename):
            os.remove(f"{os.path.splitext(filename)[0]}.html")
            shutil.rmtree(f"{os.path.splitext(filename)[0]}_files")

        def change_title(self, ui, edit, text):
            pos = ui.titles.currentRow()
            ui.titles.takeItem(pos)
            if edit:
                title = QLineEdit(ui)
                title.setText(text)
                title.returnPressed.connect(lambda: self.change_title(ui, False, title.text()))
            else:
                title = QLabel()
                title.setText(text)
            title_item = QListWidgetItem()
            ui.titles.insertItem(ui.titles.count(), title_item)
            ui.titles.setItemWidget(title_item, title)

        @staticmethod
        def add_titles(ui):
            title = QLabel()
            title_item = QListWidgetItem()
            ui.titles.insertItem(ui.titles.count(), title_item)
            ui.titles.setItemWidget(title_item, title)
            ui.text_entry.setText('')

        # def saveDocx(self, ui):
        #     with open(filename, "wb") as f:
        #         pickle.dump([ui.lesson_title.text(), assignments], f, -1)

        def connect_btn(self, ui):
            ui.add_btn.clicked.connect(lambda: self.add_titles(ui))
            ui.load_btn.clicked.connect(lambda: self.open_doc(ui))
            # ui.titles.itemPressed.connect(lambda: self.load_doc(ui))
            ui.titles.itemDoubleClicked.connect(lambda: self.change_title(ui, True, ui.titles.selectedItems()[0].text()))

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
