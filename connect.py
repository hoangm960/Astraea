import os
import pickle
import sys
from datetime import datetime

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
    OPENED_ROOM_PATH = "./data/Users/opened_room.or"

    def __init__(self, ui):
        ui.connection = ui.connection
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
            round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
            round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )
        ui.label_2.hide()
        self.connect_btn(ui)
        self.check_room(ui)

    def connect_btn(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.In_btn.clicked.connect(lambda: self.enter_room(ui))
        if ui.role == 0:
            ui.room_btn.close()
        ui.room_btn.clicked.connect(lambda: self.create_room(ui))
        ui.Go_Room.clicked.connect(lambda: self.Go_Room(ui))
        ui.Quit.clicked.connect(lambda: self.Quit(ui))
        if open(self.OPENED_ROOM_PATH).readline().rstrip():
            ui.room_btn.hide()
            ui.In_btn.hide()
            ui.id_entry.hide()
        else:
            ui.Quit.hide()
            ui.Go_Room.hide()

    def create_room(self, ui):
        cursor = ui.connection.cursor()
        cursor.execute(f"INSERT INTO room(Status) VALUES(1)")
        lesson_id = cursor.lastrowid
        open(self.OPENED_ROOM_PATH, 'w').write(str(lesson_id))
        ui.connection.commit()
        ui.label_2.show()
        ui.frame_2.hide()
        ui.id_entry.hide()
        ui.label_2.setText('Hoàn tất tạo phòng\nid: {}'.format(lesson_id))
        ui.room_btn.hide()
        timer = QtCore.QTimer()
        def complete():
            ui.label_2.hide()
            ui.frame_2.show()
            ui.id_entry.show()
        timer.singleShot(2000, lambda: complete())  

    def enter_room(self, ui):
        id = ui.id_entry.text()
        if id:
            cursor = ui.connection.cursor()
            cursor.execute(f'SELECT RoomId FROM room WHERE RoomId = {id} AND Status = 1')
            if [row for row in cursor]:
                open(self.OPENED_ROOM_PATH, 'w').write(id)
                ui.frame.close()
                ui.frame_2.close()
                ui.label_2.show()
                ui.id_entry.close()
                ui.label_2.setText('Đã vào được phòng\nid: {}'.format(id))
                ui.timer = QtCore.QTimer()
                ui.timer.singleShot(1000, lambda: self.close_pg(ui))


    def Go_Room(self, ui):
        import Room
        room_id = open(self.OPENED_ROOM_PATH).read().rstrip()
        if room_id:
            window = Room.RoomWindow(ui.role, ui.pg, ui.connection)
            window.show()
            ui.close()

    def check_room(self, ui):
        room_id = open(self.OPENED_ROOM_PATH).read().rstrip()
        if room_id:
            ui.label.setText(f'ID Phòng: {room_id}')

    def Quit(self, ui):
        open(self.OPENED_ROOM_PATH, 'w').close()
        ui.label.setText('Nhập ID Phòng')
        ui.room_btn.show()
        ui.Go_Room.hide()
        ui.Quit.hide()

    @staticmethod
    def close_pg(ui):
        import main_ui
        main_ui.main(ui.role, ui.pg, ui.connection)
        ui.close()


if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="remotemysql.com",
        user="K63yMSwITl",
        password="zRtA9VtyHq",
        database="K63yMSwITl"
    )
    app = QApplication(sys.argv)
    # window = DownloadWindow(None, 1, connection)
    window = DownloadWindow(None, 0, connection)
    window.show()
    sys.exit(app.exec_())
