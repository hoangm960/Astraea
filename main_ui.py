import os
import pickle
import subprocess
import sys
from time import sleep, time
from PyQt5 import QtGui
import win32con
import win32gui
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QFileDialog,
                             QGraphicsDropShadowEffect, QMainWindow)


from UI_Files import Resources
from win32api import GetMonitorInfo, MonitorFromPoint
import pygetwindow as gw


UI_MAIN_PATH = "./UI_Files/ui_main.ui"
OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
SCREEN_WIDTH, SCREEN_HEIGHT = work_area[2], work_area[3]


class MainWindow(QMainWindow):
    def __init__(self, role, pg=None):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        self.role = role
        self.pg = pg
        UIFunctions.uiDefinitions(self)

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
                    self.pg.resizeTo(SCREEN_WIDTH - self.width() + 16, self.height() + 8)
                except:
                    pass
        QMainWindow.changeEvent(self, event)
    

class UIFunctions(MainWindow):
    assignments = {}
    @classmethod
    def uiDefinitions(cls, ui):
        ui.setGeometry(SCREEN_WIDTH, SCREEN_HEIGHT, ui.width(), SCREEN_HEIGHT)
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        cls.resize_idle(ui, ui.pg)
        ui.shadow = QGraphicsDropShadowEffect(ui)
        ui.shadow.setBlurRadius(50)
        ui.shadow.setXOffset(0)
        ui.shadow.setYOffset(0)
        ui.shadow.setColor(QColor(0, 0, 0, 200))
        ui.bg_frame.setGraphicsEffect(ui.shadow)
        def open_profile():
            import profile
            ui.mainWin = profile.ProfileWindow()
            ui.mainWin.show()
        ui.profile_btn.clicked.connect(lambda: open_profile())
        
        
        cls.define_role(ui)
        cls.connect_btn(ui)
        cls.check_opened_lesson(ui, OPENED_LESSON_PATH)
        
    @classmethod
    def connect_btn(cls, ui):
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        if ui.pg:
            ui.btn_quit.clicked.connect(lambda: ui.pg.close())
        ui.btn_quit.clicked.connect(lambda: cls.close_pg(ui, ui.pg))

        ui.load_btn.clicked.connect(
            lambda: cls.show_file_dialog(ui, OPENED_LESSON_PATH)
        )
        ui.main_btn.clicked.connect(lambda: cls.close_pg(ui, ui.pg))
        ui.LessonButton.clicked.connect(lambda: cls.close_pg(ui, ui.pg))
        ui.LessonButton.clicked.connect(lambda: cls.open_doc(ui, ui.pg))

        ui.list_assignments.itemPressed.connect(lambda: cls.load_details(ui))

    @staticmethod
    def resize_idle(ui, pg):
        if pg:
            pg.restore()
            pg.moveTo(-8, 0)
            pg.resizeTo(SCREEN_WIDTH - ui.width() + 16, ui.height() + 8)

    @staticmethod
    def close_pg(ui, pg):
        if pg:
            pg.maximize()
        ui.close()

    @classmethod
    def check_opened_lesson(cls, ui, filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename) as f:
                    file_path = f.read().rstrip("\n")
                    cls.load_assignments(ui, file_path)

    @classmethod
    def show_file_dialog(cls, ui, filename):
        HOME_PATH = os.path.join(os.path.join(
            os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(
            ui, "Open file", HOME_PATH, "*.list")[0]
        if file_path:
            with open(filename, "w", encoding='utf8') as f:
                f.write(file_path)
            cls.load_assignments(ui, file_path)

    @classmethod
    def load_assignments(cls, ui, filename):
        ui.list_assignments.clear()
        cls.assignments.clear()
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    title = data[0]
                    assignments = data[1]
                    for assignment in assignments:
                        cls.assignments[assignment.name] = assignment.details
                        ui.list_assignments.addItem(assignment.name)
                    cls.change_assignment_title(ui, title)

    @classmethod
    def load_details(cls, ui):
        ui.assignment_details.setText(
            cls.assignments[ui.list_assignments.currentItem().text()]
        )

    @staticmethod
    def change_assignment_title(ui, title):
        ui.lesson_title.setText(
            title) if title else ui.lesson_title.setParent(None)

    @staticmethod
    def open_doc(ui, pg):
        import doc
        ui.main = doc.DocWindow(ui.role, pg)
        ui.main.show()

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
            window = edit_main.EditWindow(ui.pg)
            window.show()

    class StudentUiFunctions:
        def __init__(self, parent, ui):
            self.parent = parent
            ui.main_btn.setText("Kiểm tra")
            ui.main_btn.setStyleSheet(
                """QPushButton {background-color: rgb(156, 220, 254); border-radius: 5px;}
            QPushButton:hover {background-color: rgba(156, 220, 254, 150);}"""
            )
            ui.main_btn.clicked.connect(lambda: self.open_result_form(ui))

        @staticmethod
        def open_result_form(ui):
            import result_main
            window = result_main.ResultWindow(ui.pg)
            window.show()

    @classmethod
    def define_role(cls, ui):
        if ui.role.lower() == "teacher":
            cls.TeacherUiFunctions(cls, ui)
        if ui.role.lower() == "student":
            cls.StudentUiFunctions(cls, ui)


def main(role, pg):
    window = MainWindow(role, pg)
    window.move(SCREEN_WIDTH - window.width(), 0)
    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main("teacher", None)
    # main("student")
    sys.exit(app.exec_())
