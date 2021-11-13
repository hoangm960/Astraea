import os
import pickle
import shutil

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QFileDialog, QLabel, QListWidgetItem, QMainWindow
from win32com import client as wc

from utils.connect_db import get_connection
from path import OPENED_ASSIGNMENT_PATH, OPENED_DOC, OPENED_DOC_CONTENT

DOC_UI = "./UI_Files/Doc.ui"

class DocWindow(QMainWindow):
    switch_window_main = QtCore.pyqtSignal()
    switch_window_pad = QtCore.pyqtSignal()

    def __init__(self, role):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_UI, self)
        self.initUI()

        self.role = role
        self.define_role()

    def define_role(self):
        if self.role == 1:
            TeacherUIFunctions(self)
        if self.role == 0:
            StudentUIFunctions(self)

    def initUI(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()
        self.deleteBox_frame.hide()


class UIFunctions(DocWindow):
    docs = []

    def __init__(self, ui):
        self.get_doc()
        self.check_opened_doc(ui)
        self.connect_btn(ui)

    def connect_btn(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.return_main(ui))
        ui.del_btn.clicked.connect(lambda: self.options(ui))
        ui.Delete.clicked.connect(lambda: self.Delete(ui))
        ui.Save_btn.clicked.connect(lambda: self.change_title(ui, ui.Name_edit.text()))
        ui.load_btn.clicked.connect(lambda: self.load_doc(ui))
        ui.titles.itemClicked.connect(lambda: self.load_doc(ui))

    @staticmethod
    def get_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        return QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, filter)[0]

    def return_main(self, ui):
        ui.switch_window_main.emit()

    @staticmethod
    def options(ui):
        if ui.titles.selectedItems():
            ui.deleteBox_frame.show()
            ui.text_entry.hide()

    def load_doc(self, ui):
        name = ui.titles.currentItem().text()
        for doc in self.docs:
            if name in doc:
                content = doc[2]
                ui.text_entry.setText(content)
                open(OPENED_DOC_CONTENT, "w", encoding="utf8").write(content)

    def Delete(self, ui):
        connection = get_connection()
        selected_items = ui.titles.selectedItems()
        if selected_items:
            item = selected_items[0]
            lesson_id = open(
                OPENED_ASSIGNMENT_PATH, encoding="utf8"
            ).readlines()[1]

            cursor = connection.cursor()
            for doc in self.docs:
                if item.text() in doc:
                    id = doc[0]
                    cursor.execute(
                        "DELETE FROM doc WHERE DocId = %s AND LessonId = %s",
                        (id, lesson_id),
                    )
                    del doc
                    break
            connection.commit()
            connection.close()

            ui.titles.takeItem(ui.titles.row(item))
            ui.text_entry.clear()
            ui.deleteBox_frame.hide()

    def change_title(self, ui, text):
        connection = get_connection()
        selected_items = ui.titles.selectedItems()
        cursor = connection.cursor()
        lesson_id = open(OPENED_ASSIGNMENT_PATH, encoding="utf8").readlines()[1]
        if selected_items and ui.Name_edit.text() not in self.docs:
            item = selected_items[0]

            for doc in self.docs:
                id = doc[0]

                if item.text() == doc[1]:
                    cursor.execute(
                        "UPDATE doc SET DocName = %s WHERE DocId = %s AND LessonId = %s",
                        (text, id, lesson_id),
                    )
                    list_doc = list(doc)
                    list_doc[1] = text
                    self.docs[self.docs.index(doc)] = tuple(list_doc)
                    ui.Name_edit.clear()
                    break

        connection.commit()
        connection.close()

        ui.titles.clear()
        for doc in self.docs:
            ui.titles.addItem(doc[1])
        ui.text_entry.clear()

    def get_doc(self):
        connection = get_connection()
        cursor = connection.cursor()

        self.docs.clear()
        lesson_path, lesson_id = open(
            OPENED_ASSIGNMENT_PATH, encoding="utf8"
        ).readlines()
        if lesson_id:
            cursor.execute(
                "SELECT DocId, DocName, DocContent FROM doc WHERE LessonId = %s",
                (lesson_id,),
            )
            self.docs = [row for row in cursor]
            connection.close()

            opened = ""
            try:
                opened = open(OPENED_DOC, "r", encoding="utf8").readlines()[1]
            except IndexError:
                pass
            if opened:
                for doc in self.docs:
                    if doc[0] == int(opened):
                        self.docs[self.docs.index(doc)] = (
                            doc[0],
                            doc[1],
                            open(OPENED_DOC_CONTENT, encoding="utf8").read(),
                        )

            filename = f"{os.path.dirname(lesson_path).rstrip()}/doc.sd"
            open(filename, "w", encoding="utf8").close()
            with open(filename, "wb") as f:
                pickle.dump(self.docs, f, -1)
            open(OPENED_DOC, "w", encoding="utf8").write(filename)

    def check_opened_doc(self, ui):
        doc_path = open(OPENED_DOC, encoding="utf8").readline()
        if os.path.exists(doc_path) and os.path.getsize(doc_path) > 0:
            with open(doc_path, "rb") as f:
                unpickler = pickle.Unpickler(f)
                self.docs = unpickler.load()
                ui.titles.clear()
                for doc in self.docs:
                    ui.titles.addItem(doc[1])


class TeacherUIFunctions(UIFunctions):
    def __init__(self, ui):
        super().__init__(ui)

    def connect_btn(self, ui):
        super().connect_btn(ui)
        ui.add_btn.clicked.connect(lambda: self.add_titles(ui))
        ui.textpad.clicked.connect(lambda: self.open_textpad(ui))

    def open_textpad(self, ui):
        id = 0
        for doc in self.docs:
            if doc[1] == ui.titles.currentItem().text():
                id = doc[0]
        open(OPENED_DOC, "a", encoding="utf8").write("\n" + str(id))

        ui.switch_window_pad.emit()

    def open_doc(self, ui):
        connection = get_connection()

        if not ui.titles.currentItem().text():
            file_path = self.get_file_dialog(ui, "*.docx")
            if file_path:
                name = os.path.splitext(os.path.basename(file_path))[0]
                ui.titles.currentItem().setText(name)
                html_data = self.get_html(file_path)
                ui.text_entry.setText(html_data)

                lesson_id = open(
                    OPENED_ASSIGNMENT_PATH, encoding="utf8"
                ).readlines()[1]
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO doc(LessonId, DocName, DocContent) VALUES(%s, %s, %s)",
                    (lesson_id, name, html_data),
                )
                connection.commit()
                connection.close()

                self.delete_html_file(file_path)

        self.load_doc(ui)

    @staticmethod
    def get_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        return QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, filter)[0]

    @staticmethod
    def save_file_dialog(ui, filter):
        if ui.titles.count():
            HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            return QFileDialog.getSaveFileName(ui, "Open file", HOME_PATH, filter)[0]

    @staticmethod
    def convert_doc_to_html(filename):
        html_file = f"{os.path.splitext(filename)[0]}.html"

        word = wc.Dispatch("Word.Application")
        doc = word.Documents.Open(filename)
        doc.SaveAs(html_file, 8)
        doc.Close()
        word.Quit()

        return html_file

    def get_html(self, filename):
        with open(self.convert_doc_to_html(filename), "r", encoding="utf8") as f:
            return f.read()

    @staticmethod
    def delete_html_file(filename):
        os.remove(f"{os.path.splitext(filename)[0]}.html")
        shutil.rmtree(f"{os.path.splitext(filename)[0]}_files")

    def check_empty_doc(self):
        return any(doc[1] == "" for doc in self.docs)

    def add_titles(self, ui):
        if not self.check_empty_doc():
            title = QLabel()
            title_item = QListWidgetItem()
            ui.titles.addItem(title_item)
            ui.titles.setItemWidget(title_item, title)

            connection = get_connection()
            cursor = connection.cursor()
            lesson_id = open(
                OPENED_ASSIGNMENT_PATH, encoding="utf8"
            ).readlines()[1]
            cursor.execute(
                "INSERT INTO doc(LessonId, DocName, DocContent) VALUES(%s, '', '')",
                (lesson_id,),
            )
            self.docs.append((cursor.lastrowid, "", ""))
            connection.commit()
            connection.close()


class StudentUIFunctions(UIFunctions):
    def __init__(self, ui):
        super().__init__(ui)
        ui.confirm_frame.close()
