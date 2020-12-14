import os
import pickle
import shutil
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QLineEdit,
                             QListWidgetItem, QMainWindow)
from win32com import client as wc

import main_ui

DOC_UI = "./UI_Files/Doc.ui"
HTML_CONVERT_PATH = "./data/html_convert"


class DocWindow(QMainWindow):
    def __init__(self, role, pg):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_UI, self)
        self.role = role
        self.pg = pg
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
        ui.del_btn.clicked.connect(lambda: cls.options(ui))
        ui.Delete.clicked.connect(lambda: cls.Delete(ui))
        ui.Save_btn.clicked.connect(lambda: cls.Change(ui, ui.Name_edit.text()))
        ui.deleteBox_frame.hide()

    @staticmethod
    def close_pg(ui):
        ui.close()
        main_ui.main(ui.role, None)

    @staticmethod
    def options(ui):
        if ui.titles.selectedItems():
            ui.deleteBox_frame.show()
            ui.text_entry.hide()

    @classmethod
    def Delete(cls, ui):
        selected_items = ui.titles.selectedItems()
        if selected_items:
            item = selected_items[0]
            if item.text() in cls.docs:
                del cls.docs[item.text()]
            ui.titles.takeItem(ui.titles.row(item))
            ui.text_entry.clear()
            ui.deleteBox_frame.hide()
        
    @classmethod
    def Change(cls, ui, text):
        selected_items = ui.titles.selectedItems()
        if selected_items and not ui.Name_edit.text() in cls.docs:
            item = selected_items[0]
            temp = cls.docs[item.text()]
            cls.docs.pop(item.text())
            item.setText(text)
            cls.docs[item.text()] = temp
            ui.Name_edit.clear()

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
            if not ui.titles.currentItem().text():
                file_path = self.get_file_dialog(ui, "*.docx")
                if file_path:
                    ui.titles.currentItem().setText(
                        os.path.splitext(os.path.basename(file_path))[0])
                    self.load_doc(ui, file_path)
                    self.delete_html_file(file_path)
            else:
                self.load_doc(ui)

        @staticmethod
        def get_file_dialog(ui, filter):
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_path = QFileDialog.getOpenFileName(
                ui, "Open file", HOME_PATH, filter)[0]
            return file_path

        @staticmethod
        def save_file_dialog(ui, filter):
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_path = QFileDialog.getSaveFileName(
                ui, "Open file", HOME_PATH, filter)[0]
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

        def load_doc(self, ui, filename=''):
            if filename:
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

        def add_titles(self, ui):
            title = QLabel()
            title_item = QListWidgetItem()
            ui.titles.addItem(title_item)
            ui.titles.setItemWidget(title_item, title)

        def saveDocx(self, ui, filename):
            with open(filename, "wb") as f:
                pickle.dump(UIFunctions.docs, f, -1)
            self.reopen_main(ui)

        @staticmethod
        def reopen_main(ui):
            import main_ui
            main_ui.main(ui.role, None)
            ui.close()

        def connect_btn(self, ui):
            ui.add_btn.clicked.connect(lambda: self.add_titles(ui))
            # ui.load_btn.clicked.connect(lambda: self.get_doc(ui))
            ui.titles.itemClicked.connect(lambda: self.open_doc(ui))
            # ui.titles.itemDoubleClicked.connect(lambda: self.change_title(ui, True, ui.titles.selectedItems()[0].text()))
            ui.SaveDocx.clicked.connect(lambda: self.saveDocx(
                ui, self.save_file_dialog(ui, "*.sd")))

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
    window = DocWindow("teacher", None)
    window.show()
    sys.exit(app.exec_())
