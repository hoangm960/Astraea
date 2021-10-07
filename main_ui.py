import os
import pickle

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from Main import screen_resolution
from UI_Files import Resources

UI_MAIN_PATH = "./UI_Files/ui_main.ui"
OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
SCREEN_WIDTH, SCREEN_HEIGHT = screen_resolution()

class MainWindow(QMainWindow):
    switch_window_edit = QtCore.pyqtSignal()
    switch_window_doc = QtCore.pyqtSignal()
    switch_window_connect = QtCore.pyqtSignal()
    switch_window_profile = QtCore.pyqtSignal()
    switch_window_result = QtCore.pyqtSignal()
    switch_window_quit = QtCore.pyqtSignal()

    def __init__(self, role, pg):
        self.role = role
        self.pg = pg

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        self.init_UI()
        self.define_role()

    def init_UI(self):
        self.setGeometry(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.width(),
            SCREEN_HEIGHT,
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.profile_btn.setDisabled(False)
        if self.pg:
            self._init_pg()


    def define_role(self):
        if self.role == 1:
            TeacherUIFunctions(self)
        if self.role == 0:
            StudentUIFunctions(self)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                try:
                    self.pg.minimize()
                except:
                    pass
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                try:
                    self._init_pg()
                except:
                    pass
        QMainWindow.changeEvent(self, event)

    def _init_pg(self):
        self.pg.restore()
        self.pg.moveTo(-8, 0)
        self.pg.resizeTo(SCREEN_WIDTH - self.width() + 16, self.height() + 8)


class UIFunctions(MainWindow):
    assignments = {}

    def __init__(self, ui):
        self.check_opened_lesson(ui, OPENED_LESSON_PATH)
        self.connect_btn(ui)

    def connect_btn(self, ui):
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: self.quit(ui))
        ui.load_btn.clicked.connect(
            lambda: self.show_file_dialog(ui, OPENED_LESSON_PATH)
        )
        ui.profile_btn.clicked.connect(lambda: self.open_profile(ui))

        if (
            os.path.getsize(OPENED_LESSON_PATH) > 0
            and open(OPENED_LESSON_PATH, encoding="utf8").readlines()[1] != "0"
        ):
            ui.LessonButton.clicked.connect(lambda: self.open_doc(ui))
        else:
            ui.LessonButton.hide()

        ui.list_assignments.itemPressed.connect(lambda: self.load_details(ui))
        ui.Server_btn.clicked.connect(lambda: self.open_connect(ui))

    def quit(self, ui):
        ui.switch_window_quit.emit()

    def open_profile(self, ui):
        ui.switch_window_profile.emit()

    def open_connect(self, ui):
        ui.switch_window_connect.emit()

    def check_opened_lesson(self, ui, filename):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, encoding="utf8") as f:
                file_path = f.readline().rstrip("\n")
                if os.path.exists(file_path):
                    self.load_assignments(ui, file_path)
                else:
                    open(filename, "w", encoding="utf8").write("\n0")

    def show_file_dialog(self, ui, filename):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, "*.list")[0]
        if file_path:
            self.load_assignments(ui, file_path)
            with open(filename, "w", encoding="utf8") as f:
                f.writelines([f"{file_path}\n", "0"])

    @staticmethod
    def get_assignments(filename):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
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
        ui.lesson_title.setText(title) if title else ui.lesson_title.setParent(None)

    def open_doc(self, ui):
        ui.switch_window_doc.emit()


class TeacherUIFunctions(UIFunctions):
    def __init__(self, ui):
        super().__init__(ui)
        ui.main_btn.setText("Sửa đổi")
        ui.main_btn.setStyleSheet(
            """QPushButton {background-color: rgb(156, 220, 254); border-radius: 5px;}
        QPushButton:hover {background-color: rgba(156, 220, 254, 150);}"""
        )
        ui.main_btn.clicked.connect(lambda: self.open_edit(ui))

    def open_edit(self, ui):
        ui.switch_window_edit.emit()


class StudentUIFunctions(UIFunctions):
    def __init__(self, ui):
        super().__init__(ui)
        ui.main_btn.setText("Kiểm tra")
        ui.main_btn.setStyleSheet(
            """QPushButton {background-color: rgb(156, 220, 254); border-radius: 5px;}
        QPushButton:hover {background-color: rgba(156, 220, 254, 150);}"""
        )
        ui.main_btn.clicked.connect(lambda: self.open_result_form(ui))

    def open_result_form(self, ui):
        ui.switch_window_result.emit()
