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
        ui.label_2.hide()
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.move(
            round((QApplication.primaryScreen().size().width() - ui.width()) / 2),
            round((QApplication.primaryScreen().size().height() - ui.height()) / 2),
        )

        self.check_room(ui)
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))
        ui.download_btn.clicked.connect(
            lambda: self.download(ui, ui.id_entry.text()))
        ui.upload_btn.clicked.connect(
            lambda: self.upload(ui, open(self.OPENED_LESSON_PATH).readline()))
        if ui.role == 'student':
            ui.upload_btn.close()
        ui.room_btn.clicked.connect(lambda: self.create_room(ui))
        ui.Go_Room.clicked.connect(lambda: self.Go_Room(ui))
        ui.Quit.clicked.connect(lambda: self.Quit(ui))
        if open(self.OPENED_ROOM_PATH, 'r').read():
            ui.room_btn.hide()
            ui.In_btn.hide()
        else:
            ui.Quit.hide()
            ui.Go_Room.hide()

    def download(self, ui, lesson_id):
        from edit_main import Assignment
        try:
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

                ui.frame.close()
                ui.frame_2.close()
                ui.label_2.show()
                id = ui.id_entry.text()
                ui.id_entry.close()
                ui.label_2.setText('Tải xuống đã hoàn tất\nid: {}'.format(id))
                ui.timer = QtCore.QTimer()
                ui.timer.singleShot(1000, lambda: self.close_pg(ui))

            open(self.OPENED_LESSON_PATH, 'a').write(f'\n{lesson_id}')
        except:
            ui.id_entry.clear()
            ui.id_entry.setText('ID không chính xác')
            ui.id_entry.setStyleSheet(
                """background-color: rgb(255, 255, 255); color: rgb(255,0,0);""")

            def set_default():
                ui.id_entry.clear()
                ui.id_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255);""")
            timer = QtCore.QTimer()
            timer.singleShot(1000, lambda: set_default())

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
        room_id = open(self.OPENED_ROOM_PATH).read().rstrip()
        lesson_id = int()
        if room_id:
            try:
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
                ui.connection.commit()
                ui.label_2.show()
                ui.frame_2.close()
                ui.id_entry.close()
            except:
                ui.id_entry.clear()
                ui.id_entry.setText('Không thể đăng bài.')
                ui.id_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255); color: rgb(255,0,0);""")
                def set_default():
                    ui.id_entry.clear()
                    ui.id_entry.setStyleSheet(
                        """background-color: rgb(255, 255, 255);""")
                timer = QtCore.QTimer()
                timer.singleShot(1000, lambda: set_default())    

            if lesson_id:
                cursor = ui.connection.cursor()
                cursor.execute(f"INSERT INTO lesson_in_room(RoomId, LessonId) VALUES({room_id}, {lesson_id})")
                ui.label_2.setText(f'Hoàn tất đăng bài\nid_room: {room_id}\nid_lesson: {lesson_id}')
                ui.connection.commit()

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

    def Go_Room(self, ui):
        import Room
        room_id = open(self.OPENED_ROOM_PATH).read().rstrip()
        if room_id:
            window = Room.RoomWindow(room_id, ui.role, ui.pg, ui.connection)
            window.show()
            ui.close()
        else:
            ui.id_entry.clear()
            ui.id_entry.setText('ID không chính xác')
            ui.id_entry.setStyleSheet(
                """background-color: rgb(255, 255, 255); color: rgb(255,0,0);""")

            def set_default():
                ui.id_entry.clear()
                ui.id_entry.setStyleSheet(
                    """background-color: rgb(255, 255, 255);""")
            timer = QtCore.QTimer()
            timer.singleShot(1000, lambda: set_default())

    def check_room(self, ui):
        room_id = open(self.OPENED_ROOM_PATH).read().rstrip()
        if room_id:
            ui.label.setText(f'ID Phòng: {room_id}')

    def Quit(self, ui):
        open(self.OPENED_ROOM_PATH,'w').close()
        ui.label.setText('Nhập ID bài học')
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
    window = DownloadWindow(None, 1, connection)
    window.show()
    sys.exit(app.exec_())
