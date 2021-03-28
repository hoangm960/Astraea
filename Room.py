import os
import pickle
import sys
from datetime import datetime

import mysql.connector
import pandas
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from encryption import decrypt, encrypt


class RoomWindow(QMainWindow):
    ROOM_UI = "./UI_Files/Room.ui"

    def __init__(self, role, pg, id):
        self.role = role
        self.pg = pg
        self.id = id
        super(RoomWindow, self).__init__()
        uic.loadUi(self.ROOM_UI, self)
        UIFunctions(self)


class UIFunctions(RoomWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
    OPENED_ROOM_PATH = "./data/Users/opened_room.or"

    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.showMaximized()
        ui.ID_Room.setText(ui.id)
        self.add_lesson_list(ui)
        self.rank_student(ui)
        
        if ui.role == 0:
            ui.student_list_frame.close()
        else:
            self.add_student_list(ui)
        self.connect_btn(ui)

    def connect_btn(self, ui):
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.download_btn.clicked.connect(lambda: self.download_lesson(ui))
        if ui.role == 0:
            ui.del_lesson_btn.close()
            ui.add_btn.close()
            ui.ButtonFrame.close()
        else:
            ui.del_lesson_btn.clicked.connect(lambda: self.del_lesson(ui))
            ui.add_btn.clicked.connect(lambda: self.upload(ui))
            ui.reload_btn.clicked.connect(lambda: self.add_student_list(ui))
            ui.download_info_btn.clicked.connect(
                lambda: self.get_students_submission(ui)
            )
            ui.kick_btn.clicked.connect(lambda: self.kick_student(ui))

    @staticmethod
    def get_connection():
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="K63yMSwITl",
            password="zRtA9VtyHq",
            database="K63yMSwITl"
        )

        return connection

    @staticmethod
    def get_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, filter)[0]
        return file_path

    @staticmethod
    def get_lesson(filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    return data[0], data[1]

    def upload(self, ui):
        filename = self.get_file_dialog(ui, "*.list")
        if ui.id and filename:
            connection = self.get_connection()
            cursor = connection.cursor()
            title, assignments = self.get_lesson(filename)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO lesson(Name, CreatedDate) VALUES(%s, %s)",
                (title, current_time),
            )
            lesson_id = cursor.lastrowid
            for assignment in assignments:
                name, details, mark = (
                    assignment.name,
                    assignment.details,
                    assignment.mark,
                )
                cursor.execute(
                    "INSERT INTO assignment(LessonId, Name, Details, Mark) VALUES(%s, %s, %s, %s)",
                    (lesson_id, name, details, mark),
                )
                assignment_id = cursor.lastrowid
                for test in assignment.tests:
                    cursor.execute(
                        "INSERT INTO test(AssignmentId) VALUES(%s)", (assignment_id,)
                    )
                    test_id = cursor.lastrowid
                    for input in test[0]:
                        cursor.execute(
                            "INSERT INTO input(TestId, InputContent) VALUES(%s, %s)",
                            (test_id, input),
                        )
                    for output in test[1]:
                        cursor.execute(
                            "INSERT INTO output(TestId, OutputContent) VALUES(%s, %s)",
                            (test_id, output),
                        )
                for info in assignment.infos:
                    key, message, num = (i for i in info)
                    cursor.execute(
                        "INSERT INTO info(AssignmentId, KeyWord, Message, Quantity) VALUES(%s, %s, %s, %s)",
                        (assignment_id, key, message, num),
                    )

            if lesson_id:
                cursor = ui.connection.cursor()
                cursor.execute(
                    "INSERT INTO lesson_in_room(RoomId, LessonId) VALUES(%s, %s)",
                    (ui.id, lesson_id),
                )

            connection.commit()
            connection.close()
            self.add_lesson_list(ui)

    def del_lesson(self, ui):
        items = ui.lesson_list.selectedItems()
        connection = self.get_connection()
        cursor = connection.cursor()
        if items:
            for item in items:
                ui.lesson_list.takeItem(ui.lesson_list.row(item))

                text = item.text()
                lesson_id = text.replace("ID: ", "").replace("Tên: ", "").split(", ")[0]
                if lesson_id:
                    cursor.execute(
                        "DELETE FROM lesson_in_room WHERE LessonId = %s", (lesson_id,)
                    )
                    connection.commit()
                    connection.close()
                    break

    def download_lesson(self, ui):
        item = ui.lesson_list.currentItem()
        if item:
            text = item.text()
            lesson_id = text.replace("ID: ", "").replace("Tên: ", "").split(", ")[0]
            if lesson_id:
                self.download(ui, lesson_id)

    def download(self, ui, lesson_id):
        from edit_main import Assignment

        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT Name FROM lesson WHERE LessonId = '{lesson_id}'")
        title = [row for row in cursor][0][0]
        if title:
            cursor.execute(
                f"SELECT AssignmentId, Name, Details, Mark FROM assignment WHERE LessonId = '{lesson_id}'"
            )
            assignments = [row for row in cursor]

            file_assignments = []
            for assignment in assignments:
                assignment_id, name, details, mark = (i for i in assignment)
                cursor.execute(
                    "SELECT TestId FROM test WHERE AssignmentId = %s", (assignment_id,)
                )
                tests = [row for row in cursor]

                file_tests = []
                for test in tests:
                    test_id = test[0]
                    cursor.execute(
                        "SELECT InputContent FROM input WHERE TestId = %s", (test_id,)
                    )
                    inputs = [row[0] for row in cursor]
                    cursor.execute(
                        "SELECT OutputContent FROM output WHERE TestId = %s", (test_id,)
                    )
                    outputs = [row[0] for row in cursor]
                    file_tests.append([inputs, outputs])

                cursor.execute(
                    "SELECT KeyWord, Message, Quantity FROM info WHERE AssignmentId = %s",
                    (assignment_id,),
                )
                infos = [row for row in cursor]

                file_assignments.append(
                    Assignment(name, details, mark, file_tests, infos)
                )
            connection.close()

            filename = self.show_file_dialog(self.OPENED_LESSON_PATH)
            if filename:
                with open(filename, "wb") as f:
                    pickle.dump([title, file_assignments], f, -1)
                open(self.OPENED_LESSON_PATH, "w").write(f"{filename}\n{lesson_id}")
                self.close_pg(ui)

    @staticmethod
    def show_file_dialog(filename):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        path = QFileDialog.getSaveFileName(None, "Open file", HOME_PATH, "*.list")[0]
        with open(filename, "w", encoding="utf8") as f:
            f.write(path)
        return path

    def add_lesson_list(self, ui):
        ui.lesson_list.clear()
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT LessonId FROM lesson_in_room WHERE RoomId = %s", (ui.id,)
        )
        lesson_ids = [row[0] for row in cursor]
        for lesson_id in lesson_ids:
            cursor.execute("SELECT Name FROM lesson WHERE LessonId = %s", (lesson_id,))
            lesson_name = [row[0] for row in cursor][0]
            ui.lesson_list.addItem(f"ID: {lesson_id}, Tên: {lesson_name}")
        connection.close()

    def get_student_list(self, ui, filter):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT {filter} FROM user WHERE RoomId = {ui.id} AND Type = 0"
        )
        student_list = [row for row in cursor]
        connection.close()
        return student_list

    def add_student_list(self, ui):
        ui.student_list.clear()
        students = self.get_student_list(ui, "Username, ShowName")

        for student in students:
            username, name = student
            ui.student_list.addItem(f"Tên người dùng: {username}, Tên: {name}")

    @staticmethod
    def save_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getSaveFileName(ui, "Open file", HOME_PATH, filter)[0]
        return file_path

    def get_students_submission(self, ui):
        try:
            connection = self.get_connection()
            lesson_id = open(self.OPENED_LESSON_PATH).readlines()[1]
            submission = pandas.read_sql(
                f"SELECT UserName, SubmissionDate, Mark, Comment FROM submission WHERE LessonId = {lesson_id}",
                connection,
            )
            filename = self.save_file_dialog(ui, "*.xlsx")
            if filename:
                submission.to_excel(filename)
            connection.close()
        except:
            ui.download_info_btn.setText("Chưa có dữ liệu")
            ui.download_info_btn.setDisabled(True)
            timer = QtCore.QTimer()
            timer.singleShot(1000, lambda: ui.download_info_btn.setDisabled(False))
            timer.singleShot(
                1000,
                lambda: ui.download_info_btn.setText(
                    "Tải xuống dữ liệu bài làm học sinh"
                ),
            )

    def kick_student(self, ui):
        item = ui.student_list.currentItem()
        if item:
            text = item.text()
            username = (
                text.replace("Tên người dùng: ", "").replace("Tên: ", "").split(", ")[0]
            )
            if username:
                ui.student_list.takeItem(ui.student_list.row(item))
                connection = self.get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE user SET RoomId = Null WHERE Username = %s", (username,)
                )
                connection.commit()
                connection.close()

    def rank_student(self, ui):
        students = self.get_student_list(ui, "Username")
        names = self.get_student_list(ui, 'ShowName')
        student_scores = tmp_scores = {i[0]:0 for i in students}
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT Username, Mark FROM submission"
        )

        mark_list = [list(row) for row in cursor]
        connection.close()

        for student in list(tmp_scores):
            for mark in mark_list:
                if student == mark[0]:
                    student_scores[student] += mark[1]
        
        check = list()
        rank = list()
        for _ in range(0, len(students)):
            check.append(True)
            rank.append(0)
        stt = 1
        while stt <= len(student_scores):
            max = 0
            x = 0
            record = 0
            for i in student_scores.keys():
                if student_scores[i]>=max and check[x]:
                    max = student_scores[i]
                    record = x
                x+=1
            rank[record] = stt
            check[record] = False
            stt+=1
        stt = 0
        for _ in student_scores.keys():
            ui.Achievements_list.addItem(f"{rank[stt]}. {names[stt][0]}")
            stt+=1

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
        database="K63yMSwITl",
    )
    app = QApplication(sys.argv)
    window = RoomWindow(1, None, "11")
    # window = RoomWindow(0, None, '1')
    window.show()
    sys.exit(app.exec_())
