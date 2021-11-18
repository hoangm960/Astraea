import os
import pickle
from datetime import datetime

import pandas
from utils.connect_db import get_connection
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from models.assignment import Info, Test
from path import OPENED_ASSIGNMENT_PATH, OPENED_ROOM_PATH

ROOM_UI = "./UI_Files/Room.ui"


class RoomWindow(QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self, role, id):
        self.role = role
        self.id = id
        super(RoomWindow, self).__init__()
        uic.loadUi(ROOM_UI, self)
        self.initUI()
        self.define_role()

    def initUI(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()
        self.ID_Room.setText("ID phòng: {}".format(self.id))

    def define_role(self):
        if self.role == 1:
            TeacherUIFunctions(self)
        if self.role == 0:
            StudentUIFunctions(self)


class UIFunctions(RoomWindow):
    def __init__(self, ui):
        self.add_lesson_list(ui)
        self.rank_student(ui)
        self.connect_btn(ui)

    def connect_btn(self, ui):
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_quit.clicked.connect(lambda: self.return_main(ui))
        ui.download_btn.clicked.connect(lambda: self.download_lesson(ui))

    @staticmethod
    def get_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        return QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, filter)[0]

    @staticmethod
    def get_lesson(filename):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
                return data[0], data[1]

    def download_lesson(self, ui):
        item = ui.lesson_list.currentItem()
        if item:
            text = item.text()
            lesson_id = text.replace("ID: ", "").replace("Tên: ", "").split(", ")[0]
            if lesson_id:
                self.download(ui, lesson_id)

    def download(self, ui, lesson_id):
        from edit_main import Assignment

        connection = get_connection()
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
                assignment_id, name, details, mark = iter(assignment)
                cursor.execute(
                    "SELECT TestId FROM test WHERE AssignmentId = %s", (assignment_id,)
                )
                test_ids = [row[0] for row in cursor]
                tests = []
                for test_id in test_ids:
                    cursor.execute(
                        "SELECT InputContent FROM input WHERE TestId = %s", (test_id,)
                    )
                    inputs = [row[0] for row in cursor]
                    cursor.execute(
                        "SELECT OutputContent FROM output WHERE TestId = %s", (test_id,)
                    )
                    outputs = [row[0] for row in cursor]
                    tests.append(Test(inputs, outputs))

                cursor.execute(
                    "SELECT KeyWord, Message, Quantity FROM info WHERE AssignmentId = %s",
                    (assignment_id,),
                )
                infos_data = [row for row in cursor]
                infos = [Info(info[0], info[1], info[2]) for info in infos_data]
                file_assignments.append(Assignment(name, details, mark, tests, infos))
            connection.close()

            filename = self.show_file_dialog(OPENED_ASSIGNMENT_PATH)
            if filename:
                with open(filename, "wb") as f:
                    pickle.dump([title, file_assignments], f, -1)
                open(OPENED_ASSIGNMENT_PATH, "w", encoding="utf8").write(
                    f"{filename}\n{lesson_id}"
                )
                self.return_main(ui)

    @staticmethod
    def show_file_dialog(filename):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        path = QFileDialog.getSaveFileName(None, "Open file", HOME_PATH, "*.list")[0]
        with open(filename, "w", encoding="utf8") as f:
            f.write(path)
        return path

    def add_lesson_list(self, ui):
        ui.lesson_list.clear()
        connection = get_connection()
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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT {filter} FROM user WHERE RoomId = {ui.id} AND Type = 0")
        student_list = [row for row in cursor]
        connection.close()
        return student_list

    @staticmethod
    def save_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        return QFileDialog.getSaveFileName(ui, "Open file", HOME_PATH, filter)[0]

    def rank_student(self, ui):
        students = self.get_student_list(ui, "Username")
        names = self.get_student_list(ui, "ShowName")
        student_scores = tmp_scores = {i[0]: 0 for i in students}
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Username, Mark FROM submission")

        mark_list = [list(row) for row in cursor]
        connection.close()

        for student in list(tmp_scores):
            for mark in mark_list:
                if student == mark[0]:
                    student_scores[student] += mark[1]

        check = []
        rank = []
        for _ in range(len(students)):
            check.append(True)
            rank.append(0)
        stt = 1
        while stt <= len(student_scores):
            max = 0
            record = 0
            for x, i in enumerate(student_scores.keys()):
                if student_scores[i] >= max and check[x]:
                    max = student_scores[i]
                    record = x
            rank[record] = stt
            check[record] = False
            stt += 1
        stt = 0
        for _ in student_scores.keys():
            ui.Achievements_list.addItem(f"{rank[stt]}. {names[stt][0]}")
            stt += 1

    def return_main(self, ui):
        ui.switch_window.emit()


class TeacherUIFunctions(UIFunctions):
    def __init__(self, ui):
        super().__init__(ui)
        self.add_student_list(ui)

    def connect_btn(self, ui):
        super().connect_btn(ui)
        ui.del_lesson_btn.clicked.connect(lambda: self.del_lesson(ui))
        ui.add_btn.clicked.connect(lambda: self.upload(ui))
        ui.reload_btn.clicked.connect(lambda: self.add_student_list(ui))
        ui.download_info_btn.clicked.connect(lambda: self.get_students_submission(ui))
        ui.kick_btn.clicked.connect(lambda: self.kick_student(ui))

    def del_lesson(self, ui):
        items = ui.lesson_list.selectedItems()
        connection = get_connection()
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

    def upload(self, ui):
        filename = self.get_file_dialog(ui, "*.list")
        if ui.id and filename:
            connection = get_connection()
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
                    for input in test.inputs:
                        cursor.execute(
                            "INSERT INTO input(TestId, InputContent) VALUES(%s, %s)",
                            (test_id, input),
                        )
                    for output in test.outputs:
                        cursor.execute(
                            "INSERT INTO output(TestId, OutputContent) VALUES(%s, %s)",
                            (test_id, output),
                        )
                if assignment.infos:
                    for info in assignment.infos:
                        key, message, num = info.keyword, info.message, info.min_num
                        cursor.execute(
                            "INSERT INTO info(AssignmentId, KeyWord, Message, Quantity) VALUES(%s, %s, %s, %s)",
                            (assignment_id, key, message, num),
                        )

            if lesson_id:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO lesson_in_room(RoomId, LessonId) VALUES(%s, %s)",
                    (ui.id, lesson_id),
                )

            connection.commit()
            connection.close()
            self.add_lesson_list(ui)

    def add_student_list(self, ui):
        ui.student_list.clear()
        students = self.get_student_list(ui, "Username, ShowName")

        for student in students:
            username, name = student
            ui.student_list.addItem(f"Tên người dùng: {username}, Tên: {name}")

    @staticmethod
    def checkLessonName(lesson_name):
        invalid_char = ':*?/\[]'
        for i in invalid_char:
            if i in lesson_name:
                lesson_name = lesson_name.replace(i, '-')
        return lesson_name

    def addToSubmissionFile(self, writer, submission, lesson_name):
        lesson_name = self.checkLessonName(lesson_name)
        submission.to_excel(writer, sheet_name=lesson_name, index=False)
        wb = writer.book
        ws = writer.sheets[lesson_name]
        format = wb.add_format({"text_wrap": True})
        for idx, col in enumerate(submission):
            series = submission[col]
            max_len = (
                max((series.astype(str).map(len).max(), len(str(series.name)))) + 1
            )
            ws.set_column(idx, idx, max_len, format)

    def get_students_submission(self, ui):
        connection = get_connection()
        cursor = connection.cursor()
        room_id = int(open(OPENED_ROOM_PATH, mode="r", encoding="utf8").read())
        cursor.execute(f"SELECT LessonId FROM lesson_in_room WHERE RoomId = {room_id}")
        lesson_ids = [row[0] for row in cursor]
        filename = self.save_file_dialog(ui, "*.xlsx")

        temp_names = []
        for id in lesson_ids:
            cursor.execute(f"SELECT Name FROM lesson WHERE LessonId = {id}")
            temp_names.append(cursor.fetchone()[0])

        lesson_names = [
            f"{ele} {idx}" if (ele in temp_names[:idx]) else ele
            for idx, ele in enumerate(temp_names)
        ]

        lessons = {id: name for id, name in zip(lesson_ids, lesson_names)}
        if filename:
            writer = pandas.ExcelWriter(filename, engine="xlsxwriter")
            for id in lesson_ids:
                lesson_name = lessons[id]
                submission = pandas.read_sql(
                    f"SELECT UserName, SubmissionDate, Mark, Comment FROM submission WHERE LessonId = {id}",
                    connection,
                )
                self.addToSubmissionFile(writer, submission, lesson_name)
            writer.save()
            os.startfile(filename)
        connection.close()

    def kick_student(self, ui):
        item = ui.student_list.currentItem()
        if item:
            text = item.text()
            username = (
                text.replace("Tên người dùng: ", "").replace("Tên: ", "").split(", ")[0]
            )
            if username:
                ui.student_list.takeItem(ui.student_list.row(item))
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE user SET RoomId = Null WHERE Username = %s", (username,)
                )
                connection.commit()
                connection.close()


class StudentUIFunctions(UIFunctions):
    def __init__(self, ui):
        super().__init__(ui)
        ui.student_list_frame.close()
        ui.del_lesson_btn.close()
        ui.add_btn.close()
        ui.ButtonFrame.close()
