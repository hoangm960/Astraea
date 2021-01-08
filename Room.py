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
    def __init__(self, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: ui.close())
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.showMaximized()
        ui.ID_Room.setText(ui.id)
        self.add_lesson_list(ui)
        self.add_student_list(ui)

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
