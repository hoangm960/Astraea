import os
import pickle
import shutil
import sys

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel,
                             QListWidgetItem, QMainWindow)
from win32com import client as wc

import main_ui

DOC_UI = "./UI_Files/Doc.ui"
OPENED_DOC = "./data/Users/opened_doc.od"
OPENED_DOC_CONTENT = "./data/Users/opened_doc_content.html"


class DocWindow(QMainWindow):
    def __init__(self, role, pg):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_UI, self)
        self.role = role
        self.pg = pg

        UIFunctions(self)


class UIFunctions(DocWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"

    docs = []

    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
            round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
            round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )
        ui.showMaximized()
        ui.deleteBox_frame.hide()

        self.connect_btn(ui)
        self.get_doc()
        self.check_opened_doc(ui)
        self.define_role(ui)

    @staticmethod
    def get_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(
            os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(
            ui, "Open file", HOME_PATH, filter)[0]
        return file_path

    def connect_btn(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.del_btn.clicked.connect(lambda: self.options(ui))
        ui.Delete.clicked.connect(lambda: self.Delete(ui))
        ui.Save_btn.clicked.connect(
            lambda: self.change_title(ui, ui.Name_edit.text()))
        ui.load_btn.clicked.connect(lambda: self.load_doc(ui))
        ui.titles.itemClicked.connect(lambda: self.load_doc(ui))

    @staticmethod
    def close_pg(ui):
        ui.close()
        main_ui.main(ui.role, ui.pg)

    @staticmethod
    def options(ui):
        if ui.titles.selectedItems():
            ui.deleteBox_frame.show()
            ui.text_entry.hide()

    @staticmethod
    def get_connection():
        connection = mysql.connector.connect(
            host="sql6.freesqldatabase.com",
            user="sql6425130",
            password="VbV9wKzkms",
            database="sql6425130"
        )

        return connection


    def load_doc(self, ui):
        name = ui.titles.currentItem().text()
        for doc in self.docs:
            if name in doc:
                content = doc[2]
                ui.text_entry.setText(content)
                open(OPENED_DOC_CONTENT,  'w', encoding='utf8').write(content)

    def Delete(self, ui):
        connection = self.get_connection()
        selected_items = ui.titles.selectedItems()
        if selected_items:
            item = selected_items[0]
            lesson_id = open(UIFunctions.OPENED_LESSON_PATH, encoding='utf8').readlines()[1]

            cursor = connection.cursor()
            for doc in self.docs:
                if item.text() in doc:
                    id = doc[0]
                    cursor.execute(
                        "DELETE FROM doc WHERE DocId = %s AND LessonId = %s", (id, lesson_id))
                    del doc
                    break
            connection.commit()
            connection.close()

            ui.titles.takeItem(ui.titles.row(item))
            ui.text_entry.clear()
            ui.deleteBox_frame.hide()

    def change_title(self, ui, text):
        connection = self.get_connection()
        selected_items = ui.titles.selectedItems()
        cursor = connection.cursor()
        lesson_id = open(UIFunctions.OPENED_LESSON_PATH, encoding='utf8').readlines()[1]
        if selected_items and not ui.Name_edit.text() in self.docs:
            item = selected_items[0]

            for doc in self.docs:
                id = doc[0]
                
                if item.text() == doc[1]:
                    cursor.execute(
                        "UPDATE doc SET DocName = %s WHERE DocId = %s AND LessonId = %s", (text, id, lesson_id))
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
        connection = self.get_connection()
        cursor = connection.cursor()

        self.docs.clear()
        lesson_path, lesson_id = open(self.OPENED_LESSON_PATH, encoding='utf8').readlines()
        if lesson_id:
            cursor.execute(
                "SELECT DocId, DocName, DocContent FROM doc WHERE LessonId = %s", (lesson_id, ))
            self.docs = [row for row in cursor]
            connection.close()

            opened = ''
            try:
                opened = open(OPENED_DOC, 'r', encoding='utf8').readlines()[1]
            except IndexError:
                pass
            if opened:
                for doc in self.docs:
                    if doc[0] == int(opened):
                        self.docs[self.docs.index(doc)] = (doc[0], doc[1], open(OPENED_DOC_CONTENT, encoding='utf8').read())

            filename = f'{os.path.dirname(lesson_path).rstrip()}/doc.sd'
            open(filename, 'w', encoding='utf8').close()
            with open(filename, "wb") as f:
                pickle.dump(self.docs, f, -1)
            open(OPENED_DOC, 'w', encoding='utf8').write(filename)

    def check_opened_doc(self, ui):
        doc_path = open(OPENED_DOC, encoding='utf8').readline()
        if os.path.exists(doc_path):
            if os.path.getsize(doc_path) > 0:
                with open(doc_path, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    self.docs = unpickler.load()
                    ui.titles.clear()
                    for doc in self.docs:
                        ui.titles.addItem(doc[1])

    class TeacherUiFunctions:
        def __init__(self, ui, docs):
            self.docs = docs
            self.connect_btn(ui)

        def connect_btn(self, ui):
            ui.add_btn.clicked.connect(lambda: self.add_titles(ui))
            ui.textpad.clicked.connect(lambda: self.open_textpad(ui))

        def open_textpad(self, ui):
            id = 0
            for doc in self.docs:
                if doc[1] == ui.titles.currentItem().text():
                    id = doc[0]
            open(OPENED_DOC, 'a', encoding='utf8').write('\n' + str(id))
            import Pad
            window = Pad.MainPad(ui.pg)
            window.show()

        def open_doc(self, ui):
            connection = UIFunctions.get_connection()
            
            if not ui.titles.currentItem().text():
                file_path = self.get_file_dialog(ui, "*.docx")
                if file_path:
                    name = os.path.splitext(os.path.basename(file_path))[0]
                    ui.titles.currentItem().setText(name)
                    html_data = self.get_html(file_path)
                    ui.text_entry.setText(html_data)

                    lesson_id = open(UIFunctions.OPENED_LESSON_PATH, encoding='utf8').readlines()[1]
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO doc(LessonId, DocName, DocContent) VALUES(%s, %s, %s)", (lesson_id, name, html_data))
                    connection.commit()
                    connection.close()

                    self.delete_html_file(file_path)

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
            if ui.titles.count():
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
            with open(self.convert_doc_to_html(filename), 'r', encoding='utf8') as f:
                return f.read()

        @staticmethod
        def delete_html_file(filename):
            os.remove(f"{os.path.splitext(filename)[0]}.html")
            shutil.rmtree(f"{os.path.splitext(filename)[0]}_files")

        def check_empty_doc(self):
            for doc in self.docs:
                if doc[1] == '':
                    return True
            return False

        def add_titles(self, ui):
            if not self.check_empty_doc():
                title = QLabel()
                title_item = QListWidgetItem()
                ui.titles.addItem(title_item)
                ui.titles.setItemWidget(title_item, title)

                connection = UIFunctions.get_connection()
                cursor = connection.cursor()
                lesson_id = open(UIFunctions.OPENED_LESSON_PATH, encoding='utf8').readlines()[1]
                cursor.execute("INSERT INTO doc(LessonId, DocName, DocContent) VALUES(%s, '', '')", (lesson_id,))
                self.docs.append((cursor.lastrowid, '', ''))
                connection.commit()
                connection.close()

    class StudentUiFunctions:
        def __init__(self, ui, docs):
            self.docs = docs
            ui.confirm_frame.close()


    def define_role(self, ui):
        if ui.role == 1:
            self.TeacherUiFunctions(ui, self.docs)
        if ui.role == 0:
            self.StudentUiFunctions(ui, self.docs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocWindow(1, None)
    # window = DocWindow(0, None)
    window.show()
    sys.exit(app.exec_())