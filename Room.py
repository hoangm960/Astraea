import os
import pickle
import sys
from datetime import datetime
import pandas

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from UI_Files import Resources


class RoomWindow(QMainWindow):
    ROOM_UI = "./UI_Files/Room.ui"
    def __init__(self, role, pg, connection):
        self.role = role
        self.pg = pg 
        self.connection = connection
        super(RoomWindow, self).__init__()
        uic.loadUi(self.ROOM_UI, self)
        UIFunctions(self)

class UIFunctions(RoomWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
    OPENED_ROOM_PATH = "./data/Users/opened_room.or"
    room_id = open(OPENED_ROOM_PATH).readline().rstrip()

    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.showMaximized()
        ui.ID_Room.setText(self.room_id)
        self.add_lesson_list(ui)
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
            ui.download_info_btn.clicked.connect(lambda: self.get_students_submission(ui))

    @staticmethod
    def get_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(
            os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(
            ui, "Open file", HOME_PATH, filter)[0]
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
        filename = self.get_file_dialog(ui, '*.list')
        if self.room_id and filename:
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

            if lesson_id:
                cursor = ui.connection.cursor()
                cursor.execute(f"INSERT INTO lesson_in_room(RoomId, LessonId) VALUES({self.room_id}, {lesson_id})")

            ui.connection.commit()
            self.add_lesson_list(ui)

    @staticmethod
    def del_lesson(ui):
        items = ui.lesson_list.selectedItems()
        if items:
            for item in items:
                ui.lesson_list.takeItem(ui.lesson_list.row(item))
        
                text = item.text()
                lesson_id = text.replace('ID: ', '').replace('Tên: ', '').split(', ')[0]
                if lesson_id:
                    cursor = ui.connection.cursor()
                    cursor.execute(f'DELETE FROM lesson_in_room WHERE LessonId = {lesson_id}')
                    ui.connection.commit()

    def download_lesson(self, ui):
        item = ui.lesson_list.currentItem()
        if item:
            text = item.text()
            lesson_id = text.replace('ID: ', '').replace('Tên: ', '').split(', ')[0]
            if lesson_id:
                self.download(ui, lesson_id)
                self.close_pg(ui)

    def download(self, ui, lesson_id):
        from edit_main import Assignment
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

            filename = self.show_file_dialog(self.OPENED_LESSON_PATH)
            with open(filename, "wb") as f:
                pickle.dump([title, file_assignments], f, -1)
            open(self.OPENED_LESSON_PATH, 'w').write(f'{filename}\n{lesson_id}')

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

    def add_lesson_list(self, ui):
        ui.lesson_list.clear()
        cursor = ui.connection.cursor()
        try:
            cursor.execute(f'SELECT LessonId FROM lesson_in_room WHERE RoomId = {self.room_id}')
        except:
            msg = QMessageBox(ui)
            msg.setWindowTitle("Bắt được lỗi chương trình.")
            msg.move(round((QApplication.primaryScreen().size().width() - msg.width()) / 2),
            round((QApplication.primaryScreen().size().height() - msg.height()) / 2),
            )
            msg.setText(f"1054 (42S22): không tồn tại Column")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        lesson_ids = [row[0] for row in cursor]
        for lesson_id in lesson_ids:
            cursor.execute(f'SELECT Name FROM lesson WHERE LessonId = {lesson_id}')
            lesson_name = [row[0] for row in cursor][0]
            ui.lesson_list.addItem(f'ID: {lesson_id}, Tên: {lesson_name}')

    def add_student_list(self, ui):
        ui.student_list.clear()
        cursor = ui.connection.cursor()
        cursor.execute(f'SELECT Username, ShowName FROM user WHERE RoomId = {self.room_id} AND Type = 0')
        students = [row for row in cursor]
        for student in students:
            username, name = student
            ui.student_list.addItem(f'Tên người dùng: {username}, Tên: {name}')

    @staticmethod
    def save_file_dialog(ui, filter):
        HOME_PATH = os.path.join(os.path.join(
            os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getSaveFileName(
            ui, "Open file", HOME_PATH, filter)[0]
        return file_path

    def get_students_submission(self, ui):
        lesson_id = open(self.OPENED_LESSON_PATH).readlines()[1]
        submission = pandas.read_sql(f"SELECT UserName, SubmissionDate, Mark, Comment FROM submission WHERE LessonId = {lesson_id}", ui.connection)
        filename = self.save_file_dialog(ui, '*.xlsx')
        if filename:
            submission.to_excel(filename)

    @staticmethod
    def close_pg(ui):
        import main_ui
        main_ui.main(ui.role, ui.pg, ui.connection)
        ui.close()

if __name__ == '__main__':
    connection = mysql.connector.connect(
        host="remotemysql.com",
        user="K63yMSwITl",
        password="zRtA9VtyHq",
        database="K63yMSwITl"
    )
    app = QApplication(sys.argv)
    window = RoomWindow(1, None, connection)
    # window = RoomWindow(0, None, connection)
    window.show()
    sys.exit(app.exec_())
