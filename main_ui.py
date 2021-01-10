import os
import pickle
import sys

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from win32api import GetMonitorInfo, MonitorFromPoint

from UI_Files import Resources

UI_MAIN_PATH = "./UI_Files/ui_main.ui"
OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
SCREEN_WIDTH, SCREEN_HEIGHT = work_area[2], work_area[3]


class MainWindow(QMainWindow):
    def __init__(self, role, pg, connection):
        self.role = role
        self.pg = pg
        self.connection = connection

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        if self.pg:
            self.pg.restore()
            self.pg.moveTo(-8, 0)
            self.pg.resizeTo(
                SCREEN_WIDTH - self.width() + 16, self.height() + 8)
        UIFunctions(self)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                try:
                    self.pg.minimize()
                except:
                    pass
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                try:
                    self.pg.restore()
                    self.pg.moveTo(-8, 0)
                    self.pg.resizeTo(
                        SCREEN_WIDTH - self.width() + 16, self.height() + 8)
                except:
                    pass
        QMainWindow.changeEvent(self, event)


class UIFunctions(MainWindow):
    assignments = {}

    def __init__(self, ui):
        if ui.pg:
            ui.pg.restore()
            ui.pg.moveTo(-8, 0)
            ui.pg.resizeTo(
                SCREEN_WIDTH - ui.width() + 16, ui.height() + 8)
        ui.setGeometry(SCREEN_WIDTH, SCREEN_HEIGHT, ui.width(), SCREEN_HEIGHT)
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize_idle(ui, ui.pg)

        def open_profile(ui):
            import profile
            ui.mainWin = profile.ProfileWindow(ui, ui.pg, ui.connection)
            ui.mainWin.show()
        ui.profile_btn.clicked.connect(lambda: open_profile(ui))

        self.define_role(ui)
        self.connect_btn(ui)
        self.check_opened_lesson(ui, OPENED_LESSON_PATH)

    def connect_btn(self, ui):
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        if ui.pg:
            ui.btn_quit.clicked.connect(lambda: ui.pg.close())
        ui.btn_quit.clicked.connect(lambda: self.close_pg(ui))

        ui.load_btn.clicked.connect(
            lambda: self.show_file_dialog(ui, OPENED_LESSON_PATH)
        )
        ui.main_btn.clicked.connect(lambda: self.close_pg(ui))
        if os.path.getsize(OPENED_LESSON_PATH) > 0:
            if open(OPENED_LESSON_PATH).readlines()[1] != '0':
                ui.LessonButton.clicked.connect(lambda: self.open_doc(ui))
            else:
                ui.LessonButton.hide()
        else:
            ui.LessonButton.hide()

        ui.list_assignments.itemPressed.connect(lambda: self.load_details(ui))
        ui.Server_btn.clicked.connect(lambda: self.open_connect(ui))

    def open_connect(self, ui):
        self.close_pg(ui)
        import connect
        window = connect.DownloadWindow(ui.pg, ui.role, ui.connection)
        window.show()

    @staticmethod
    def resize_idle(ui, pg):
        if pg:
            pg.restore()
            pg.moveTo(-8, 0)
            pg.resizeTo(SCREEN_WIDTH - ui.width() + 16, ui.height() + 8)

    @staticmethod
    def close_pg(ui):
        if ui.pg:
            ui.pg.maximize()
        ui.close()

    def check_opened_lesson(self, ui, filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, encoding='utf8') as f:
                    file_path = f.readline().rstrip("\n")
                    self.load_assignments(ui, file_path)

    def show_file_dialog(self, ui, filename):
        HOME_PATH = os.path.join(os.path.join(
            os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(
            ui, "Open file", HOME_PATH, "*.list")[0]
        if file_path:
            self.load_assignments(ui, file_path)
            with open(filename, "w", encoding='utf8') as f:
                f.writelines([f'{file_path}\n', '0'])

    @staticmethod
    def get_assignments(filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    return data[0], data[1]

    def load_assignments(self, ui, filename):
        ui.list_assignments.clear()
        self.assignments.clear()
        lesson = self.get_assignments(filename)
        if lesson:
            title, assignments = lesson
            for assignment in assignments:
                self.assignments[assignment.name] = assignment.details
                ui.list_assignments.addItem(assignment.name)
            self.change_assignment_title(ui, title)

    def load_details(self, ui):
        ui.assignment_details.setText(
            self.assignments[ui.list_assignments.currentItem().text()]
        )

    @staticmethod
    def change_assignment_title(ui, title):
        ui.lesson_title.setText(
            title) if title else ui.lesson_title.setParent(None)

    def open_doc(self, ui):
        self.close_pg(ui)
        import doc
        window = doc.DocWindow(ui.role, ui.pg, ui.connection)
        window.show()

    class TeacherUiFunctions:

        def __init__(self, parent, ui):
            self.parent = parent
            ui.main_btn.setText("Sửa đổi")
            ui.main_btn.setStyleSheet(
                """QPushButton {background-color: rgb(156, 220, 254); border-radius: 5px;}
            QPushButton:hover {background-color: rgba(156, 220, 254, 150);}"""
            )
            ui.main_btn.clicked.connect(lambda: self.open_edit_form(ui))

        @staticmethod
        def open_edit_form(ui):
            import edit_main
            window = edit_main.EditWindow(ui.pg, ui.connection)
            window.show()

    class StudentUiFunctions:
        def __init__(self, ui):
            ui.main_btn.setText("Kiểm tra")
            ui.main_btn.setStyleSheet(
                """QPushButton {background-color: rgb(156, 220, 254); border-radius: 5px;}
            QPushButton:hover {background-color: rgba(156, 220, 254, 150);}"""
            )
            ui.main_btn.clicked.connect(lambda: self.open_result_form(ui))

        @staticmethod
        def open_result_form(ui):
            import result_main
            window = result_main.ResultWindow(ui.pg, ui.connection)
            window.show()

    def define_role(self, ui):
        if ui.role == 1:
            self.TeacherUiFunctions(self, ui)
        if ui.role == 0:
            self.StudentUiFunctions(ui)


def main(role, pg, connection):
    window = MainWindow(role, pg, connection)
    window.move(SCREEN_WIDTH - window.width(), 0)
    window.show()


if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="remotemysql.com",
        user="K63yMSwITl",
        password="zRtA9VtyHq",
        database="K63yMSwITl"
    )
    app = QApplication(sys.argv)
    main(1, None, connection)
    # main(0, None, connection)
    sys.exit(app.exec_())
