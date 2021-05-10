import sys

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from encryption import decrypt, encrypt


class DownloadWindow(QMainWindow):
    CONNECT_UI = "./UI_Files/connect.ui"

    def __init__(self, pg, role, *args, **kwargs):
        self.pg = pg
        self.role = role
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(self.CONNECT_UI, self)
        UIFunctions(self)


class UIFunctions(DownloadWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
    OPENED_ROOM_PATH = "./data/Users/opened_room.or"
    KEY_PATH = "data/encryption/users.key"
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"

    def __init__(self, ui):
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
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        if ui.role == 0:
            ui.room_btn.close()
        else:
            ui.room_btn.clicked.connect(lambda: self.create_room(ui))
        ui.Go_Room.clicked.connect(lambda: self.Go_Room(ui))
        ui.Quit.clicked.connect(lambda: self.Quit(ui))
        ui.Quit.clicked.connect(lambda: open('./data/Users/opened_assignment.oa', 'w', encoding='utf8').close())

    @staticmethod
    def get_connection():
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="K63yMSwITl",
            password="zRtA9VtyHq",
            database="K63yMSwITl"
        )

        return connection

    def create_room(self, ui):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO room(Status) VALUES(1)")
        lesson_id = cursor.lastrowid
        connection.commit()
        connection.close()

        open(self.OPENED_ROOM_PATH, 'w', encoding='utf8').write(str(lesson_id))
        ui.label_2.show()
        ui.frame_2.hide()
        ui.id_entry.hide()
        ui.label_2.setText('Hoàn tất tạo phòng\nid: {}'.format(lesson_id))
        ui.room_btn.hide()
        timer = QtCore.QTimer()
        def complete():
            ui.label_2.hide()
            ui.frame_2.show()
            ui.id_entry.hide()
            ui.In_btn.hide()
            # self.check_room(ui)
        timer.singleShot(2000, lambda: complete())  

    def enter_room(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        username = open(self.USER_PATH, encoding="utf8").readline().rstrip()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)
        room_id = ui.id_entry.text()
        connection = self.get_connection()
        if room_id:
            cursor = connection.cursor()
            cursor.execute('SELECT RoomId FROM room WHERE RoomId = %s AND Status = %s', (room_id, 1))
            if [row for row in cursor]:
                open(self.OPENED_ROOM_PATH, 'w', encoding='utf8').write(room_id)
                cursor.execute("UPDATE user SET RoomId = %s WHERE Username = %s", (room_id, username))
                ui.frame_2.close()
                ui.label_2.show()
                ui.id_entry.close()
                ui.label_2.setText('Đã vào được phòng\nid: {}'.format(room_id))
                ui.timer = QtCore.QTimer()
                ui.timer.singleShot(1000, lambda: self.close_pg(ui))
            connection.commit()
            connection.close()


    def Go_Room(self, ui):
        import Room
        room_id = open(self.OPENED_ROOM_PATH, encoding='utf8').read().rstrip()
        if room_id:
            window = Room.RoomWindow(ui.role, ui.pg, room_id)
            window.show()
            ui.close()

    def check_room(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        username = open(self.USER_PATH, encoding="utf8").readline().rstrip()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT RoomId FROM user WHERE Username = %s", (username, ))
        room_ids = [row for row in cursor]
        connection.close()
        if room_ids:
            for room_id in room_ids:
                open(self.OPENED_ROOM_PATH, 'w', encoding='utf8').write(str(room_id[0]) if room_id[0] else '')

        room_id = open(self.OPENED_ROOM_PATH, encoding='utf8').read().rstrip()
        if room_id:
            ui.label.setText(f'ID Phòng: {room_id}')
            ui.room_btn.hide()
            ui.In_btn.hide()
            ui.id_entry.hide()
            open('./data/Users/opened_assignment.oa', 'w', encoding='utf8').close()
        else:
            ui.Quit.hide()
            ui.Go_Room.hide()

    def Quit(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        username = open(self.USER_PATH, encoding = 'utf-8').readline().rstrip()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)

        connection = self.get_connection()
        open(self.OPENED_ROOM_PATH, 'w', encoding='utf8').close()
        cursor = connection.cursor()
        cursor.execute("UPDATE user SET RoomId = NULL WHERE Username = %s", (username, ))
        connection.commit()
        connection.close()
        
        ui.label.setText('Nhập ID Phòng')
        if ui.role == 1:
            ui.room_btn.show()
        ui.Go_Room.hide()
        ui.Quit.hide()

    @staticmethod
    def close_pg(ui):
        import main_ui
        main_ui.main(ui.role, ui.pg)
        ui.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = DownloadWindow(None, 1)
    window = DownloadWindow(None, 0)
    window.show()
    sys.exit(app.exec_())
