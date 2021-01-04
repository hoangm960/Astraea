from datetime import datetime
import os
import pickle
import sys

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


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
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"

    def __init__(self, ui):
        ui.connection = ui.connection

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
            lambda: self.upload(ui, open(self.OPENED_LESSON_PATH).read()))
        if ui.role == 'student':
            ui.upload_btn.close()

    def download(self, ui, lesson_id):
        from edit_main import Assignment
        if lesson_id:
            cursor = ui.connection.cursor()
            cursor.execute(
                f"SELECT Name FROM lesson WHERE LessonId = '{lesson_id}'")
            title = [row for row in cursor][0][0]
            if title:
                cursor.execute(
                    f"SELECT AssignmentId, Name, Details, Mark FROM assignment WHERE LessonId = '{lesson_id}'")
                assignments = [row for row in cursor]

                file_assignments = []
                for assignment in assignments:
                    assignment_id, name, details, mark = (
                        i for i in assignment)
                    cursor.execute(
                        f"SELECT TestId FROM test WHERE AssignmentId = '{assignment_id}'")
                    tests = [row for row in cursor]

                    file_tests = []
                    for test in tests:
                        test_id = test[0]
                        cursor.execute(
                            f"SELECT InputContent FROM input WHERE TestId = '{test_id}'")
                        inputs = [row[0] for row in cursor]
                        cursor.execute(
                            f"SELECT OutputContent FROM output WHERE TestId = '{test_id}'")
                        outputs = [row[0] for row in cursor]
                        file_tests.append([inputs, outputs])

                    cursor.execute(
                        f"SELECT KeyWord, Message, Quantity FROM info WHERE AssignmentId = '{assignment_id}'")
                    infos = [row for row in cursor]

                    file_assignments.append(Assignment(
                        name, details, mark, file_tests, infos))

                with open(self.show_file_dialog(self.OPENED_LESSON_PATH), "wb") as f:
                    pickle.dump([title, file_assignments], f, -1)

        self.close_pg(ui)

    @staticmethod
    def show_file_dialog(filename):
        HOME_PATH = os.path.join(os.path.join(
            os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getSaveFileName(
            None, "Open file", HOME_PATH, "*.list"
        )[0]
        with open(filename, "w", encoding='utf8') as f:
            f.write(file_path)
        return file_path

    @staticmethod
    def get_assignment(ui, id):
        if id:
            cursor = ui.connection.cursor()
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
    def get_lesson(filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    return data[0], data[1]

    @classmethod
    def upload(self, ui, filename):
        if filename:
            cursor = ui.connection.cursor()
            title, assignments = self.get_lesson(filename)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                f"INSERT INTO lesson(Name, CreatedDate) VALUES('{title}', '{current_time}');")
            lesson_id = cursor.lastrowid
            for assignment in assignments:
                name, details, mark = assignment.name, assignment.details, assignment.mark
                cursor.execute(
                    f"INSERT INTO assignment(LessonId, Name, Details, Mark) VALUES({lesson_id}, '{name}', '{details}', {mark});")
                assignment_id = cursor.lastrowid
                for test in assignment.tests:
                    cursor.execute(
                        f"INSERT INTO test(AssignmentId) VALUES({assignment_id});")
                    test_id = cursor.lastrowid
                    for input in test[0]:
                        cursor.execute(
                            f"INSERT INTO input(TestId, InputContent) VALUES({test_id}, '{input}');")
                    for output in test[1]:
                        cursor.execute(
                            f"INSERT INTO output(TestId, OutputContent) VALUES({test_id}, '{output}');")
                for info in assignment.infos:
                    key, message, num = (i for i in info)
                    cursor.execute(
                        f"INSERT INTO info(AssignmentId, KeyWord, Message, Quantity) VALUES({assignment_id}, '{key}', '{message}', {num});")
            print(lesson_id)
            ui.connection.commit()
            ui.connection.close()

        self.close_pg(ui)

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
