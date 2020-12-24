import os
import pickle
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog)
import pyodbc


class DownloadWindow(QMainWindow):
    CONNECT_UI = "./UI_Files/connect.ui"
    OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"

    server = 'ADMIN' 
    database = 'Astraea-v1'
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;')

    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(self.CONNECT_UI, self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(
            round((QApplication.primaryScreen().size().width() - self.width()) / 2),
            round((QApplication.primaryScreen().size().height() - self.height()) / 2),
        )
        self.btn_quit.clicked.connect(self.close)
        self.download_btn.clicked.connect(lambda: self.download(self.id_entry.text()))

    @classmethod
    def download(self, id):
        if id:
            cursor = self.connection.cursor()
            cursor.execute("SELECT Name FROM [Astraea-v1].[dbo].[Lesson] WHERE LessonId = ?", id)
            titles = [row for row in cursor]
            if titles:
                title = titles[0][0]
                cursor.execute("SELECT AssignmentId FROM [Astraea-v1].[dbo].[Assignment] WHERE LessonId = ?", id)
                assignments = [row[0] for row in cursor]
                self.show_file_dialog(self.OPENED_ASSIGNMENT_PATH)
                self.load_assignments(open(self.OPENED_ASSIGNMENT_PATH, encoding='utf-8').read().rstrip(), title, assignments)

    @classmethod
    def show_file_dialog(self, filename):
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
            cursor.execute("SELECT Name, Details, Mark FROM [Astraea-v1].dbo.Assignment WHERE AssignmentId = ?", id)
            titles, details, mark = [row for row in cursor][0]
            cursor.execute("SELECT InputContent FROM [Astraea-v1].dbo.Input WHERE AssignmentId = ?", id)
            inputs = [row[0] for row in cursor]
            cursor.execute("SELECT OutputContent FROM [Astraea-v1].dbo.Output WHERE AssignmentId = ?", id)
            outputs = [row[0] for row in cursor]
            return titles, details, mark, inputs, outputs

    @classmethod
    def load_assignments(self, filename, title, assignment_ids):
        from edit_main import Assignment
        assignments = []
        for assignment_id in assignment_ids:
            titles, details, mark, inputs, outputs = self.get_assignment(assignment_id)
            assignments.append(
                Assignment(titles, details, mark, inputs, outputs)
            )
        with open(filename, "wb") as f:
            pickle.dump([title, assignments], f, -1)

    @staticmethod
    def close_pg(ui):
        import main_ui
        main_ui.main('student', ui.pg)
        ui.close()