import os
import pickle
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog)
import pyodbc


class DownloadWindow(QMainWindow):
    CONNECT_UI = "./UI_Files/connect.ui"

    def __init__(self, pg, *args, **kwargs):
        self.pg = pg
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(self.CONNECT_UI, self)
        UIFunctions(self)


class UIFunctions(DownloadWindow):
    OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"
    server = 'ADMIN'
    database = 'Astraea-v1'
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;')

    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
            round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
            round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.download_btn.clicked.connect(
            lambda: self.download(ui, ui.id_entry.text()))

    @classmethod
    def download(self, ui, id):
        if id:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT Name FROM [Astraea-v1].[dbo].[Lesson] WHERE LessonId = ?", id)
            titles = [row for row in cursor]
            if titles:
                title = titles[0][0]
                cursor.execute(
                    "SELECT AssignmentId FROM [Astraea-v1].[dbo].[Assignment] WHERE LessonId = ?", id)
                assignments = [row[0] for row in cursor]
                self.show_file_dialog(self.OPENED_ASSIGNMENT_PATH)
                self.load_assignments(ui, open(
                    self.OPENED_ASSIGNMENT_PATH, encoding='utf-8').read().rstrip(), title, assignments)

    @staticmethod
    def show_file_dialog(filename):
        file_path = open(filename, encoding='utf-8').read().rstrip()
        if not file_path:
            HOME_PATH = os.path.join(os.path.join(
                os.environ["USERPROFILE"]), "Desktop")
            file_path = QFileDialog.getSaveFileName(
                None, "Open file", HOME_PATH, "*.list"
            )[0]
            with open(filename, "w", encoding='utf8') as f:
                f.write(file_path)

    @classmethod
    def get_assignment(self, id):
        if id:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT Name, Details, Mark FROM [Astraea-v1].dbo.Assignment WHERE AssignmentId = ?", id)
            titles, details, mark = [row for row in cursor if row[0]][0]
            cursor.execute(
                "SELECT InputContent FROM [Astraea-v1].dbo.Input WHERE AssignmentId = ?", id)
            inputs = [row[0] for row in cursor if row[0]]
            cursor.execute(
                "SELECT OutputContent FROM [Astraea-v1].dbo.Output WHERE AssignmentId = ?", id)
            outputs = [row[0] for row in cursor]
            return titles, details, mark, inputs, outputs

    @classmethod
    def load_assignments(self, ui, filename, title, assignment_ids):
        from edit_main import Assignment
        assignments = []
        for assignment_id in assignment_ids:
            titles, details, mark, inputs, outputs = self.get_assignment(
                assignment_id)
            assignments.append(
                Assignment(titles, details, mark, inputs, outputs)
            )
        with open(filename, "wb") as f:
            pickle.dump([title, assignments], f, -1)

        self.close_pg(ui)

    @staticmethod
    def close_pg(ui):
        import main_ui
        main_ui.main('student', ui.pg)
        ui.close()
