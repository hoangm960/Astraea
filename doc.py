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
    def __init__(self, role):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_UI, self)
        self.role = role
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
        ui.Delete.clicked.connect(lambda: cls.Delete(ui, ui.Delete_spin.value()-1))
        ui.Save_btn.clicked.connect(lambda: cls.Change(ui, ui.Name_spin.value()-1, ui.Name_edit.text()))
        ui.deleteBox_frame.hide()
    @classmethod
    def close_pg(cls, ui):
        ui.close()
        main_ui.main(ui.role)
    @classmethod
    def Delete(cls, ui,number):
        ui.titles.takeItem(number)
    @classmethod
    def Change(cls, ui, number, text):
        if number<ui.titles.count():
            ui.titles.item(number).setText(text)
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

        # def change_title(self, ui, edit, text):
        #     pos = ui.titles.currentRow()
        #     ui.titles.takeItem(pos)
        #     if edit:  
        #         title = QLineEdit(ui)
        #         title.setText(text)
        #         title.returnPressed.connect(lambda: self.change_title(ui, False, title.text()))
        #     else:
        #         title = QLabel()
        #         title.setText(text)
        #         print(UIFunctions.docs)
        #         UIFunctions.docs[text] = UIFunctions.docs.pop(text)
        #         title_item = QListWidgetItem()
        #         ui.titles.insertItem(ui.titles.count(), title_item)
        #         ui.titles.setItemWidget(title_item, title)

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
            main_ui.main(ui.role)
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
    window = DocWindow("teacher")
    window.show()
    sys.exit(app.exec_())
