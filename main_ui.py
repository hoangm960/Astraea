import os
import pickle
import sys
from PyQt5.QtGui import QIcon

import mysql.connector
import pygetwindow
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

import Main
from UI_Files import Resources

UI_MAIN_PATH = "./UI_Files/ui_main.ui"
OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
QuitFile = "./UI_Files/QuitFrame.ui"


class MainWindow(QMainWindow):
    def __init__(self, role, pg):
        self.role = role
        self.pg = pg

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        try:
            self.pg.restore()
            self.pg.moveTo(-8, 0)
            self.pg.resizeTo(
                Main.SCREEN_WIDTH - self.width() + 16, self.height() + 8)
        except (pygetwindow.PyGetWindowException, AttributeError):
            pass
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
                        Main.SCREEN_WIDTH - self.width() + 16, self.height() + 8)
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
                Main.SCREEN_WIDTH - ui.width() + 16, ui.height() + 8)
        ui.setGeometry(int(Main.SCREEN_WIDTH), int(Main.SCREEN_HEIGHT), ui.width(), int(Main.SCREEN_HEIGHT))
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize_idle(ui, ui.pg)
        ui.profile_btn.setDisabled(False)
        def open_profile(ui):
            import profile
            ui.mainWin = profile.ProfileWindow(ui, ui.pg)
            ui.mainWin.show()
        ui.profile_btn.clicked.connect(lambda: open_profile(ui))

        self.define_role(ui)
        self.connect_btn(ui)
        self.check_opened_lesson(ui, OPENED_LESSON_PATH)

    def connect_btn(self, ui):
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        def check():
            ui_main = QuitFrame(ui)
            ui_main.show()
        ui.btn_quit.clicked.connect(lambda: check())

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
        window = connect.DownloadWindow(ui.pg, ui.role)
        window.show()

    @staticmethod
    def resize_idle(ui, pg):
        if pg:
            pg.restore()
            pg.moveTo(-8, 0)
            pg.resizeTo(Main.SCREEN_WIDTH - ui.width() + 16, ui.height() + 8)

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
                    if os.path.exists(file_path):
                        self.load_assignments(ui, file_path)
                    else:
                        open(filename, 'w').write('')

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
        window = doc.DocWindow(ui.role, ui.pg)
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
            window = edit_main.EditWindow(ui.pg)
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
            window = result_main.ResultWindow(ui.pg)
            window.show()

    def define_role(self, ui):
        if ui.role == 1:
            self.TeacherUiFunctions(self, ui)
        if ui.role == 0:
            self.StudentUiFunctions(ui)


def main(role, pg):
    window = MainWindow(role, pg)
    window.move(Main.SCREEN_WIDTH - window.width(), 0)
    window.show()
class QuitFrame(QMainWindow):
    def __init__(self, ui):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(QuitFile, self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        def AcceptQuit():
            if ui.pg:
                ui.pg.close()
            ui.close()
            self.close()
        self.Accept.clicked.connect(lambda: AcceptQuit())
        self.Deny.clicked.connect(lambda: self.close())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main(1, None)
    # main(0, None, connection)
    sys.exit(app.exec_())
