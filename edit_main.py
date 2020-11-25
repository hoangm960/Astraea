import os
from pathlib import Path
import pickle
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsDropShadowEffect,
    QLayout,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)
from PyQt5 import uic
from UI_Files import Resources
from win32api import GetSystemMetrics
import main_ui
from encryption import *

EDIT_FORM_PATH = "UI_Files/edit_form.ui"
EDIT_FRAME_PATH = "UI_Files/edit_frame.ui"
OPENED_LESSON_PATH = "data/Users/opened_assignment.oa"
# KEY_PATH


class Assignment:
    def __init__(self, name, ex_file, input_file, ans_file, tests, vars, details):
        self.name = name
        self.ex_file = ex_file
        self.input_file = input_file
        self.ans_file = ans_file
        self.tests = tests
        self.vars = vars
        self.details = details


class EditWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi(EDIT_FORM_PATH, self)
        self.setGeometry(
            round((GetSystemMetrics(0) - self.width()) / 2),
            round((GetSystemMetrics(1) - self.height()) / 2),
            self.width(),
            self.height(),
        )

        def moveWindow(event):
            if UIFunctions.returnStatus() == True:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(EditWindow):
    GLOBAL_STATE = False
    ASSIGNMENTS = []
    deleted = False

    @classmethod
    def uiDefinitions(cls, ui):
        # Delete title bar
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Make drop shadow
        ui.shadow = QGraphicsDropShadowEffect(ui)
        ui.shadow.setBlurRadius(20)
        ui.shadow.setXOffset(0)
        ui.shadow.setYOffset(0)
        ui.shadow.setColor(QColor(0, 0, 0, 100))
        ui.bg_frame.setGraphicsEffect(ui.shadow)

        # Button function
        ui.btn_maximize.clicked.connect(lambda: cls.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: cls.reopen_main(ui))
        ui.confirm_btn.clicked.connect(
            lambda: cls.load_assignments(ui, open(OPENED_LESSON_PATH).read().rstrip())
        )

        # Window size grip
        ui.sizegrip = QSizeGrip(ui.frame_grip)
        ui.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(90, 90, 90)}"
        )
        ui.sizegrip.setToolTip("Resize Window")

        # Change scene
        ui.confirm_button.clicked.connect(lambda: cls.go_to_second(ui))
        ui.return_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(0))
        ui.add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(2))
        ui.return_add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))
        ui.confirm_add_btn.clicked.connect(
            lambda: cls.add_frame(ui, int(ui.num_entry_3.text()))
        )
        ui.confirm_add_btn.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))
        ui.stacked_widget.setCurrentIndex(0)
        ui.Hours_entry.setDisabled(True)
        ui.Minutes_entry.setDisabled(True)
        ui.checkBox.clicked.connect(lambda: ui.Hours_entry.setValue(0))
        ui.checkBox.clicked.connect(lambda: ui.Minutes_entry.setValue(0))
        with open(OPENED_LESSON_PATH) as f:
            cls.check_empty(ui, f.read().rstrip())

    @classmethod
    def check_empty(cls, ui, filename):
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                ui.stacked_widget.setCurrentIndex(1)
                with open(filename, "rb") as f:
                    unpickler = pickle.Unpickler(f)
                    data = unpickler.load()
                    title = data[0]
                    assignments = data[1]
                    cls.put_frame_in_list(ui, len(assignments))
                    cls.setup_frame(ui, title, assignments)

    @classmethod
    def go_to_second(cls, ui):
        cls.change_lesson_title(ui, ui.name_entry.text())
        cls.put_frame_in_list(ui, ui.num_entry.value())
        ui.stacked_widget.setCurrentIndex(1)

    @classmethod
    def returnStatus(cls):
        return cls.GLOBAL_STATE

    @classmethod
    def maximize_restore(cls, ui):
        status = cls.GLOBAL_STATE

        if status == False:
            ui.showMaximized()

            cls.GLOBAL_STATE = True

            ui.bg_layout.setContentsMargins(0, 0, 0, 0)
            ui.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30);
                border-radius: 0px;
                color: rgb(255, 255, 255);"""
            )
            ui.btn_maximize.setToolTip("Restore")
        else:
            cls.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.bg_layout.setContentsMargins(10, 10, 10, 10)
            ui.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30);
                border-radius: 10px;
                color: rgb(255, 255, 255);"""
            )
            ui.btn_maximize.setToolTip("Maximize")

    class EditFrame(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(EDIT_FRAME_PATH, self)

            self.test_file_btn.clicked.connect(
                lambda: self.show_file_dialog(self.test_file_entry)
            )
            self.input_file_btn.clicked.connect(
                lambda: self.show_file_dialog(self.input_file_entry)
            )
            self.ans_file_btn.clicked.connect(
                lambda: self.show_file_dialog(self.ans_file_entry)
            )

        def show_file_dialog(self, entry):
            HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            file_name = QFileDialog.getOpenFileName(self, "Open file", HOME_PATH)

            if file_name[0]:
                entry.setText(file_name[0])

    @classmethod
    def change_lesson_title(cls, ui, title):
        ui.lesson_title.setText(title if title else "Bài học không tên")

    @classmethod
    def setup_frame(cls, ui, title, assignments):
        children = ui.content_widget.children()
        i = 1
        cls.change_lesson_title(ui, title)
        for assignment in assignments:
            children[i].title_entry.setText(assignment.name)
            children[i].test_file_entry.setText(assignment.ex_file)
            children[i].input_file_entry.setText(assignment.input_file)
            children[i].ans_file_entry.setText(assignment.ans_file)
            children[i].test_num_entry.setValue(assignment.tests)
            children[i].test_var_entry.setValue(assignment.vars)
            children[i].details_entry.setText(assignment.details)
            i += 1

    @classmethod
    def put_frame_in_list(cls, ui, num):
        current_layout = ui.content_widget.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.content_widget.setLayout(current_layout)
        for i in reversed(range(current_layout.count())):
            current_layout.itemAt(i).widget().setParent(None)

        ui.scrollArea.verticalScrollBar().setValue(1)

        cls.add_frame(ui, num)

    @classmethod
    def add_frame(cls, ui, num):
        for _ in range(num):
            ui.frame = cls.EditFrame()
            ui.frame.close_btn.clicked.connect(lambda: cls.close_frame(ui, ui.frame))
            ui.content_widget.layout().addWidget(ui.frame)

    @classmethod
    def close_frame(cls, ui, frame):
        children = ui.content_widget.children()
        del children[0]
        pos = len(children) - children.index(frame) - 1
        cls.warn_close_frame(ui, children[pos])
        if cls.deleted == True:
            children[pos].setParent(None)
            ui.scrollArea.verticalScrollBar().setValue(1)

    @classmethod
    def warn_close_frame(cls, ui, frame):
        msg = QMessageBox(ui)
        msg.setWindowTitle("Xóa bài tập")
        msg.setText(f"'{frame.title_entry.text()}' sẽ được xóa")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(cls.popup_button)
        msg.exec_()

    @classmethod
    def popup_button(cls, i):
        cls.deleted = False if i.text().lower() == "cancel" else True

    @classmethod
    def load_assignments(cls, ui, filename):
        children = ui.content_widget.children()
        del children[0]
        assignments = []
        for i in range(ui.content_widget.layout().count()):
            if not children[i].title_entry.text() in [
                assignment.name for assignment in assignments
            ]:
                assignments.append(
                    Assignment(
                        children[i].title_entry.text(),
                        children[i].test_file_entry.text(),
                        children[i].input_file_entry.text(),
                        children[i].ans_file_entry.text(),
                        children[i].test_num_entry.value(),
                        children[i].test_var_entry.value(),
                        children[i].details_entry.toPlainText(),
                    )
                )

        with open(filename, "wb") as f:
            pickle.dump([ui.lesson_title.text(), assignments], f, -1)

        cls.reopen_main(ui)

    @classmethod
    def reopen_main(cls, ui):
        main_ui.main("teacher")
        ui.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditWindow()
    window.show()
    sys.exit(app.exec_())
