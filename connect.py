from encryption import decrypt, encrypt
import sys

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow


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
    KEY_PATH = "data/encryption/users.key"
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"

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
            ui.room_btn.hide()
        else:
            ui.room_btn.clicked.connect(lambda: self.create_room(ui))
        ui.Go_Room.clicked.connect(lambda: self.Go_Room(ui))
        ui.Quit.clicked.connect(lambda: self.Quit(ui))
            

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
            ui.id_entry.hide()
            self.check_room(ui)
        timer.singleShot(2000, lambda: complete())  

    def enter_room(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        username = open(self.USER_PATH).readline().rstrip()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)
        room_id = ui.id_entry.text()
        if room_id:
            cursor = ui.connection.cursor()
            cursor.execute(f'SELECT RoomId FROM room WHERE RoomId = {room_id} AND Status = 1')
            if [row for row in cursor]:
                open(self.OPENED_ROOM_PATH, 'w').write(room_id)
                cursor.execute(f"UPDATE user SET RoomId = {room_id} WHERE Username = '{username}'")
                ui.frame.close()
                ui.frame_2.close()
                ui.label_2.show()
                ui.id_entry.close()
                ui.label_2.setText('Đã vào được phòng\nid: {}'.format(room_id))
                ui.timer = QtCore.QTimer()
                ui.timer.singleShot(1000, lambda: self.close_pg(ui))
            ui.connection.commit()


    def Go_Room(self, ui):
        import Room
        room_id = open(self.OPENED_ROOM_PATH).read().rstrip()
        if room_id:
            window = Room.RoomWindow(ui.role, ui.pg, ui.connection)
            window.show()
            ui.close()

    def check_room(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        username = open(self.USER_PATH).readline().rstrip()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)
        cursor = ui.connection.cursor()
        cursor.execute(f"SELECT RoomId FROM user WHERE Username = '{username}'")
        room_ids = [row for row in cursor]
        if room_ids:
            for room_id in room_ids:
                open(self.OPENED_ROOM_PATH, 'w').write(str(room_id[0]))

        room_id = open(self.OPENED_ROOM_PATH).read().rstrip()
        if room_id:
            ui.label.setText(f'ID Phòng: {room_id}')

            ui.room_btn.hide()
            ui.In_btn.hide()
            ui.id_entry.hide()
        else:
            ui.Quit.hide()
            ui.Go_Room.hide()

    def Quit(self, ui):
        decrypt(self.USER_PATH_ENCRYPTED, self.USER_PATH, self.KEY_PATH)
        username = open(self.USER_PATH).readline().rstrip()
        encrypt(self.USER_PATH, self.USER_PATH_ENCRYPTED, self.KEY_PATH)

        open(self.OPENED_ROOM_PATH, 'w').close()
        cursor = ui.connection.cursor()
        cursor.execute(f"UPDATE user SET RoomId = NULL WHERE Username = '{username}'")
        ui.connection.commit()
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
