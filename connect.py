from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from encryption import decrypt, encrypt
from path import (KEY_PATH, OPENED_ASSIGNMENT_PATH, OPENED_ROOM_PATH,
                  USER_PATH, USER_PATH_ENCRYPTED)
from utils.connect_db import get_connection

CONNECT_UI = "./UI_Files/connect.ui"


class ConnectWindow(QMainWindow):
    switch_window_main = QtCore.pyqtSignal()
    switch_window_room = QtCore.pyqtSignal(int)

    def __init__(self, role):
        self.role = role
        QMainWindow.__init__(self)
        uic.loadUi(CONNECT_UI, self)
        self.initUI()
        UIFunctions(self)

    def initUI(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(
            round((QApplication.primaryScreen().size().width() - self.width()) / 2),
            round((QApplication.primaryScreen().size().height() - self.height()) / 2),
        )
        self.label_2.hide()


class UIFunctions(ConnectWindow):
    def __init__(self, ui):
        self.connect_btn(ui)
        self.check_room(ui)

    def connect_btn(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.return_main(ui))
        ui.In_btn.clicked.connect(lambda: self.enter_room(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        if ui.role == 0:
            ui.room_btn.close()
        else:
            ui.room_btn.clicked.connect(lambda: self.create_room(ui))
        ui.Go_Room.clicked.connect(lambda: self.open_room(ui))
        ui.Quit.clicked.connect(lambda: self.Quit(ui))
        ui.Quit.clicked.connect(
            lambda: open(
                OPENED_ASSIGNMENT_PATH, "w", encoding="utf8"
            ).close()
        )

    def create_room(self, ui):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO room(Status) VALUES(1)")
        lesson_id = cursor.lastrowid
        connection.commit()
        connection.close()

        open(OPENED_ROOM_PATH, "w", encoding="utf8").write(str(lesson_id))
        ui.label_2.show()
        ui.frame_2.hide()
        ui.id_entry.hide()
        ui.label_2.setText("Hoàn tất tạo phòng\nid: {}".format(lesson_id))
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
        username = self._get_user("utf8")
        room_id = ui.id_entry.text()
        connection = get_connection()
        if room_id:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT RoomId FROM room WHERE RoomId = %s AND Status = %s",
                (room_id, 1),
            )
            if [row for row in cursor]:
                open(OPENED_ROOM_PATH, "w", encoding="utf8").write(room_id)
                cursor.execute(
                    "UPDATE user SET RoomId = %s WHERE Username = %s",
                    (room_id, username),
                )
                ui.frame_2.close()
                ui.label_2.show()
                ui.id_entry.close()
                ui.label_2.setText("Đã vào được phòng\nid: {}".format(room_id))
                ui.timer = QtCore.QTimer()
                ui.timer.singleShot(1000, lambda: self.return_main(ui))
            connection.commit()
            connection.close()

    def open_room(self, ui):
        room_id = open(OPENED_ROOM_PATH, encoding="utf8").read().rstrip()
        if room_id:
            ui.switch_window_room.emit(int(room_id))

    def check_room(self, ui):
        username = self._get_user("utf8")
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT RoomId FROM user WHERE Username = %s", (username,))
        room_ids = [row for row in cursor]
        connection.close()
        if room_ids:
            for room_id in room_ids:
                open(OPENED_ROOM_PATH, "w", encoding="utf8").write(
                    str(room_id[0]) if room_id[0] else ""
                )

        room_id = open(OPENED_ROOM_PATH, encoding="utf8").read().rstrip()
        if room_id:
            ui.label.setText(f"ID Phòng: {room_id}")
            ui.room_btn.hide()
            ui.In_btn.hide()
            ui.id_entry.hide()
            open(OPENED_ASSIGNMENT_PATH, "w", encoding="utf8").close()
        else:
            ui.Quit.hide()
            ui.Go_Room.hide()

    def Quit(self, ui):
        username = self._get_user("utf-8")
        connection = get_connection()
        open(OPENED_ROOM_PATH, "w", encoding="utf8").close()
        cursor = connection.cursor()
        cursor.execute("UPDATE user SET RoomId = NULL WHERE Username = %s", (username,))
        connection.commit()
        connection.close()

        ui.label.setText("Nhập ID Phòng")
        if ui.role == 1:
            ui.room_btn.show()
        ui.Go_Room.hide()
        ui.Quit.hide()

    def _get_user(self, encoding):
        decrypt(USER_PATH_ENCRYPTED, USER_PATH, KEY_PATH)
        result = open(USER_PATH, encoding=encoding).readline().rstrip()
        encrypt(USER_PATH, USER_PATH_ENCRYPTED, KEY_PATH)
        return result

    def return_main(self, ui):
        ui.switch_window_main.emit()
