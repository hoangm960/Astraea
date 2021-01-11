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



class DocWindow(QMainWindow):
    def __init__(self, role, pg, connection):
        QMainWindow.__init__(self)
        uic.loadUi(DOC_UI, self)
        self.role = role
        self.pg = pg
        self.connection = connection

        UIFunctions(self)


class UIFunctions(DocWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
    docs = {}

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
        self.get_doc(ui)
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
            lambda: self.Change(ui, ui.Name_edit.text()))
        ui.load_btn.clicked.connect(lambda: self.load_doc(ui))

    @staticmethod
    def close_pg(ui):
        ui.close()
        main_ui.main(ui.role, ui.pg, ui.connection)

    @staticmethod
    def options(ui):
        if ui.titles.selectedItems():
            ui.deleteBox_frame.show()
            ui.text_entry.hide()

    def Delete(self, ui):
        selected_items = ui.titles.selectedItems()
        if selected_items:
            item = selected_items[0]
            if item.text() in self.docs:
                del self.docs[item.text()]
            ui.titles.takeItem(ui.titles.row(item))
            ui.text_entry.clear()
            ui.deleteBox_frame.hide()

            lesson_id = open(UIFunctions.OPENED_LESSON_PATH).readlines()[1]
            cursor = ui.connection.cursor()
            cursor.execute(f"DELETE FROM doc WHERE DocName = '{item.text()}' AND LessonId = {lesson_id}")
            ui.connection.commit()

    def Change(self, ui, text):
        selected_items = ui.titles.selectedItems()
        if selected_items and not ui.Name_edit.text() in self.docs:
            item = selected_items[0]

            lesson_id = open(UIFunctions.OPENED_LESSON_PATH).readlines()[1]
            cursor = ui.connection.cursor()
            cursor.execute(f"UPDATE doc SET DocName = '{text}' WHERE DocName = '{item.text()}' AND LessonId = {lesson_id}")
            ui.connection.commit()

            temp = self.docs[item.text()]
            self.docs.pop(item.text())
            item.setText(text)
            self.docs[item.text()] = temp
            ui.Name_edit.clear()

    def get_doc(self, ui):
        self.docs.clear()
        lesson_path, lesson_id = open(self.OPENED_LESSON_PATH).readlines()
        # try:
        if lesson_id:
            cursor = ui.connection.cursor()
            cursor.execute(f"SELECT DocName, DocContent FROM doc WHERE LessonId = {lesson_id}")
            docs = [row for row in cursor]
            for doc in docs:
                title, content = doc
                self.docs[title] = content.replace("''", "'")
            
            filename = f'{os.path.dirname(lesson_path).rstrip()}/doc.sd'
            open(filename, 'w').close()
            with open(filename, "wb") as f:
                pickle.dump(self.docs, f, -1)
            open(OPENED_DOC, 'w').write(filename)
        # except:
        #     pass

    def check_opened_doc(self, ui):
        doc_path = open(OPENED_DOC).read()
        if os.path.exists(doc_path):
            if os.path.getsize(doc_path) > 0:
                with open(doc_path, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    self.docs = unpickler.load()
                    ui.titles.clear()
                    for key in self.docs.keys():
                        ui.titles.addItem(key)

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

        @staticmethod
        def add_titles(ui):
            title = QLabel()
            title_item = QListWidgetItem()
            ui.titles.addItem(title_item)
            ui.titles.setItemWidget(title_item, title)

        def saveDocx(self, ui):
            cursor = ui.connection.cursor()
            lesson_id = open(UIFunctions.OPENED_LESSON_PATH).readlines()[1]
            cursor.execute(f"SELECT DocName FROM doc WHERE LessonId = {lesson_id}")
            doc_names = [row[0] for row in cursor]
            for key in UIFunctions.docs:
                content = UIFunctions.docs[key].replace("'", "''")
                if key in doc_names:
                    cursor.execute(f"UPDATE doc SET DocContent = '{content}' WHERE DocName = '{key}'")
                else:
                    cursor.execute(f"INSERT INTO doc(LessonId, DocName, DocContent) VALUES({lesson_id},'{key}', '{content}')")
                ui.connection.commit()

        def connect_btn(self, ui):
            ui.add_btn.clicked.connect(lambda: self.add_titles(ui))
            ui.titles.itemClicked.connect(lambda: self.open_doc(ui))
            ui.SaveDocx.clicked.connect(
                lambda: self.saveDocx(ui))

    class StudentUiFunctions:
        def __init__(self, ui):
            ui.confirm_frame.close()
            ui.titles.itemClicked.connect(lambda: ui.text_entry.setText(
                UIFunctions.docs[ui.titles.currentItem().text()]))

    def define_role(self, ui):
        if ui.role == 1:
            self.TeacherUiFunctions(ui)
        if ui.role == 0:
            self.StudentUiFunctions(ui)


if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="remotemysql.com",
        user="K63yMSwITl",
        password="zRtA9VtyHq",
        database="K63yMSwITl"
    )
    app = QApplication(sys.argv)
    window = DocWindow(1, None, connection)
    # window = DocWindow(0, None, connection)
    window.show()
    sys.exit(app.exec_())
