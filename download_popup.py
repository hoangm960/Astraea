import datetime
import os
import pickle
import sys
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog)
import mysql.connector


class DownloadWindow(QMainWindow):
    CONNECT_UI = "./UI_Files/connect.ui"

    def __init__(self, pg, role, connection, *args, **kwargs):
        self.pg = pg
        self.role = role
        self.connection = connection
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(self.CONNECT_UI, self)
        UIFunctions(self)


class UIFunctions(DownloadWindow):
    OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"

    def __init__(self, ui):
        self.connection = ui.connection

        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
            round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
            round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.download_btn.clicked.connect(
            lambda: self.download(ui, ui.id_entry.text()))
        ui.upload_btn.clicked.connect(
            lambda: self.upload(open(self.OPENED_LESSON_PATH).read()))
        if ui.role == 'student':
            ui.upload_btn.close()

    def download(self, ui, id):
        if id:
            cursor = self.connection.cursor()
            cursor.execute(
                f"SELECT Name FROM lesson WHERE LessonId = '{id}'")
            titles = [row for row in cursor]
            if titles:
                title = titles[0][0]
                cursor.execute(
                    f"SELECT AssignmentId FROM assignment WHERE LessonId = '{id}'")
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
                f"SELECT Name, Details, Mark FROM assignment WHERE AssignmentId = '{id}'")
            titles, details, mark = [row for row in cursor if row[0]][0]
            cursor.execute(
                f"SELECT InputContent FROM input WHERE AssignmentId = '{id}'")
            inputs = [row[0] for row in cursor if row[0]]
            cursor.execute(
                f"SELECT OutputContent FROM output WHERE AssignmentId = '{id}'")
            outputs = [row[0] for row in cursor]
            return titles, details, mark, inputs, outputs

    @classmethod
    def load_assignments(self, ui, filename, title, assignment_ids):
        from edit_main import assignment
        assignments = []
        for assignment_id in assignment_ids:
            titles, details, mark, inputs, outputs = self.get_assignment(
                assignment_id)
            assignments.append(
                assignment(titles, details, mark, inputs, outputs)
            )
        with open(filename, "wb") as f:
            pickle.dump([title, assignments], f, -1)

        self.close_pg(ui)

    @classmethod
    def upload(self, filename):
        if filename:
            cursor = self.connection.cursor()
            data = self.parent.get_assignments(filename)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f"INSERT INTO lesson VALUES {data[0]}, {current_time}, {str(data[1])};", 
            )
            self.connection.commit()
            self.connection.close()

    @staticmethod
    def close_pg(ui):
        import main_ui
        main_ui.main(ui.role, ui.pg)
        ui.close()

if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="remotemysql.com",
        user="K63yMSwITl",
        password="zRtA9VtyHq",
        database="K63yMSwITl"
    )
    app = QApplication(sys.argv)
    window = DownloadWindow(None, "teacher", connection)
    window.show()
    sys.exit(app.exec_())
