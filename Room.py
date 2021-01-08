import os
import pickle
import sys
from datetime import datetime

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


class RoomWindow(QMainWindow):
    ROOM_UI = "./UI_Files/Room.ui"
    def __init__(self, id, role, pg, connection):
        self.id = id
        self.role = role
        self.pg = pg 
        self.connection = connection
        super(RoomWindow, self).__init__()
        uic.loadUi(self.ROOM_UI, self)
        UIFunctions(self)

class UIFunctions(RoomWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"

    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.showMaximized()
        ui.ID_Room.setText(ui.id)
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

            with open(self.show_file_dialog(self.OPENED_LESSON_PATH), "wb") as f:
                pickle.dump([title, file_assignments], f, -1)

            open(self.OPENED_LESSON_PATH, 'a').write(f'\n{lesson_id}')

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
    def add_lesson_list(ui):
        cursor = ui.connection.cursor()
        cursor.execute(f'SELECT LessonId FROM lesson_in_room WHERE RoomId = {ui.id}')
        lesson_ids = [row[0] for row in cursor]
        for lesson_id in lesson_ids:
            cursor.execute(f'SELECT Name FROM lesson WHERE LessonId = {lesson_id}')
            lesson_name = [row[0] for row in cursor][0]
            ui.lesson_list.addItem(f'ID: {lesson_id}, Tên: {lesson_name}')

    @staticmethod
    def add_student_list(ui):
        cursor = ui.connection.cursor()
        cursor.execute(f'SELECT Username, ShowName FROM user WHERE RoomId = {ui.id} AND Type = 0')
        students = [row for row in cursor]
        for student in students:
            username, name = student
            ui.student_list.addItem(f'Tên người dùng: {username}, Tên: {name}')

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
    window = RoomWindow('16', 1, None, connection)
    window.show()
    sys.exit(app.exec_())
