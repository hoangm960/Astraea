import os
import pickle
import subprocess
import sys

import win32con
import win32gui
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizeGrip,
    QWidget,
)
from win32api import GetSystemMetrics
import result_main
import edit_main
import result_main
from UI_Files import Resources

UI_MAIN_PATH = "UI_Files/ui_main.ui"
ASSIGNMENTS_PATH = "data/Lesson/assignments.list"


class MainWindow(QMainWindow):
    def __init__(self, role):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        self.role = role
        UIFunctions.uiDefinitions(self)


class UIFunctions(MainWindow):
    assignments = {}

    @classmethod
    def uiDefinitions(cls, ui):
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ui.shadow = QGraphicsDropShadowEffect(ui)
        ui.shadow.setBlurRadius(50)
        ui.shadow.setXOffset(0)
        ui.shadow.setYOffset(0)
        ui.shadow.setColor(QColor(0, 0, 0, 200))
        ui.bg_frame.setGraphicsEffect(ui.shadow)

        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: cls.close_pg(ui))

        # cls.open_vscode()

        cls.load_assignments(ui, ASSIGNMENTS_PATH)
        ui.list_assignments.itemPressed.connect(lambda: cls.load_details(ui))

        cls.define_role(ui)

    @classmethod
    def open_vscode(cls):
        file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
        subprocess.call(file)
        cls.pg = win32gui.FindWindow(None, "Visual Studio Code")
        x0, y0, x1, y1 = win32gui.GetWindowRect(cls.pg)
        w = x1 - x0
        h = y1 - y0
        win32gui.MoveWindow(cls.pg, 0, 0, w + 45, h, True)

    @classmethod
    def close_pg(cls, ui):
        try:
            win32gui.PostMessage(cls.pg, win32con.WM_CLOSE, 0, 0)
        except:
            pass

        ui.close()

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
            [detail for detail in cls.assignments.values()][
                ui.list_assignments.currentRow()
            ]
        )

    @classmethod
    def change_assignment_title(cls, ui, title):
        ui.assignment_title.setText(title) if title else ui.assignment_title.setParent(None)

    class TeacherUiFunctions:
        parent = None
        changed = True

        @classmethod
        def __init__(cls, parent, ui):
            cls.parent = parent

            ui.main_btn.setText("Sửa đổi")
            ui.main_btn.setStyleSheet(
                """QPushButton {background-color: rgb(59, 143, 14);}
            QPushButton:hover {background-color: rgba(59, 143, 14, 150);}"""
            )
            ui.main_btn.clicked.connect(lambda: cls.open_edit_form(ui))

            ui.assignment_details.setReadOnly(False)
            ui.confirmButton = QDialogButtonBox(ui.frame_content_hint)
            ui.confirmButton.setStandardButtons(QDialogButtonBox.Ok)
            ui.confirmButton.setObjectName("confirmButton")
            ui.verticalLayout_4.addWidget(ui.confirmButton)
            ui.confirmButton.accepted.connect(
                lambda: cls.save_text(ui, ASSIGNMENTS_PATH)
            )

        @classmethod
        def save_text(cls, ui, filename):
            if os.path.exists(filename):
                if os.path.getsize(filename) > 0:
                    if (
                        list(cls.parent.assignments.values())[ui.list_assignments.currentRow()]
                        != ui.assignment_details.toPlainText()
                    ):
                        cls.show_confirm_mess(ui)

                    if cls.changed:
                        with open(filename, "rb") as f:
                            unpickler = pickle.Unpickler(f)
                            assignments = unpickler.load()[1]
                        assignments[
                            ui.list_assignments.currentRow()
                        ].details = ui.assignment_details.toPlainText()

                        with open(filename, "wb") as f:
                            pickle.dump(assignments, f)

                    cls.parent.load_details(ui)

        @classmethod
        def show_confirm_mess(cls, ui):
            msg = QMessageBox(ui)
            msg.setWindowTitle("Thành công sửa đổi bài tập")
            msg.setText("Chi tiết câu đã được chỉnh sửa")
            msg.setDetailedText(
                f"Chi tiết gốc:\n{list(cls.parent.assignments.values())[ui.list_assignments.currentRow()]}\n\nChi tiết sau khi sửa đổi:\n{ui.assignment_details.toPlainText()}"
            )
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(cls.popup_button)
            msg.exec_()

        @classmethod
        def popup_button(cls, i):
            cls.changed = False if i.text().lower() == "cancel" else True

        @classmethod
        def open_edit_form(cls, ui):
            window = edit_main.EditWindow()
            window.show()
            ui.close()

    class StudentUiFunctions:
        @classmethod
        def __init__(cls, parent, ui):
            cls.parent = parent

            ui.main_btn.setText("kiểm tra")
            ui.main_btn.setStyleSheet(
                """QPushButton {background-color: rgb(59, 143, 14);}
            QPushButton:hover {background-color: rgba(59, 143, 14, 150);}"""
            )
            ui.main_btn.clicked.connect(lambda: cls.open_result_form(ui))
        @classmethod
        def open_result_form(cls, ui):
            window = result_main.ResultWindow()
            window.show()
            ui.close()
    @classmethod
    def define_role(cls, ui):
        if ui.role.lower() == "teacher":
            cls.TeacherUiFunctions(cls, ui)
        if ui.role.lower() == "student":
            cls.StudentUiFunctions(cls, ui)


def main(role):
    window = MainWindow(role)
    window.move(GetSystemMetrics(0) - window.width(), 0)
    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main("teacher")
    sys.exit(app.exec_())
