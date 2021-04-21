import os
import pickle
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QSizeGrip, QVBoxLayout, QWidget)

KEY_PATH = "./data/Lesson/assignments.key"
TEST_FORM_PATH = "./UI_Files/edit_test_form.ui"
TEST_FRAME_PATH = "./UI_Files/edit_test_frame.ui"
INFO_FRAME_PATH = "./UI_Files/edit_info_frame.ui"
OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"
HTML_CONVERT_PATH = "./data/html_convert"

from UI_Files import Resources


class Test:
    def __init__(self, input, output):
        self.input = input
        self.output = output


class EditTestWindow(QMainWindow):
    def __init__(self, pg, mode):
        self.pg = pg
        self.mode = mode
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(TEST_FORM_PATH, self)
        self.setGeometry(
            round((QApplication.primaryScreen().size().width() - self.width()) / 2),
            round((QApplication.primaryScreen().size().height() - self.height()) / 2),
            self.width(),
            self.height(),
        )

        def moveWindow(event):
            if UIFunctions.GLOBAL_STATE == True:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow

        UIFunctions(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunctions(EditTestWindow):
    GLOBAL_STATE = False
    ASSIGNMENTS = []
    doc_files = []

    def __init__(self, ui):
        # Delete title bar
        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Button function
        self.connect_btn(ui)

        # Window size grip
        ui.sizegrip = QSizeGrip(ui.frame_grip)
        ui.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px; margin: 5px; border-radius: 10px; } QSizeGrip:hover { background-color: rgb(90, 90, 90)}"
        )
        ui.sizegrip.setToolTip("Resize Window")

    def connect_btn(self, ui):
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: self.reopen_main(ui))

        ui.add_btn.clicked.connect(lambda: self.put_frame_in_list(ui))

    @classmethod
    def returnStatus(self):
        return self.GLOBAL_STATE

    def maximize_restore(self, ui):
        status = self.GLOBAL_STATE

        if status == False:
            ui.showMaximized()

            self.GLOBAL_STATE = True

            ui.bg_layout.setContentsMargins(0, 0, 0, 0)
            ui.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30);
                border-radius: 0px;
                color: rgb(255, 255, 255);"""
            )
            ui.btn_maximize.setToolTip("khôi phục")
        else:
            self.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.bg_layout.setContentsMargins(0, 0, 0, 0)
            ui.bg_frame.setStyleSheet(
                """background-color: rgb(30, 30, 30);
                border-radius: 10px;
                color: rgb(255, 255, 255);"""
            )
            ui.btn_maximize.setToolTip("Phóng to")

    @staticmethod
    def reopen_main(ui):
        import main_ui
        main_ui.main(1, ui.pg)
        ui.close()

    class EditTestFrame(QWidget):

        def __init__(self, ui, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(TEST_FRAME_PATH, self)
            self.close_btn.clicked.connect(lambda: self.closeFrame(ui))

        def add_frame(self):
            self.add_frame_btn.clicked.connect(self.put_frame_in_list)

        def put_frame_in_list(self):
            current_layout = self.scrollAreaWidgetContents.layout()
            if not current_layout:
                current_layout = QVBoxLayout()
                current_layout.setContentsMargins(9, 9, 9, 9)
                self.scrollAreaWidgetContents.setLayout(current_layout)

            self.scrollArea.verticalScrollBar().setValue(1)

            self.add_frame()

        def add_frame(self):
            self.wid = QPushButton
            self.scrollAreaWidgetContents.layout().addWidget(self.wid)
            print(self.scrollAreaWidgetContents.layout().children())

        def closeFrame(self, ui):
            self.setParent(None)
            ui.scrollArea.verticalScrollBar().setValue(1)

    class EditInfoFrame(QWidget):

        def __init__(self, ui, *args, **kwargs):
            super().__init__(*args, **kwargs)
            uic.loadUi(INFO_FRAME_PATH, self)
            self.close_btn.clicked.connect(lambda: self.closeFrame(ui))

        def closeFrame(self, ui):
            self.setParent(None)
            ui.scrollArea.verticalScrollBar().setValue(1)

    def put_frame_in_list(self, ui):
        current_layout = ui.content_widget.layout()
        if not current_layout:
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(9, 9, 9, 9)
            ui.content_widget.setLayout(current_layout)

        ui.scrollArea.verticalScrollBar().setValue(1)

        self.add_frame(ui)

    def add_frame(self, ui):
        ui.frame = self.EditTestFrame(ui) if ui.mode == 0 else self.EditInfoFrame(ui)

        ui.content_widget.layout().addWidget(ui.frame)

    @staticmethod
    def load_io(test_file):
        with open(test_file, encoding = 'utf-8') as f:
            lines = f.readlines()
            if lines:
                sep = lines[0].rstrip()
                del lines[0]
                tests = []
                for line in lines:
                    inputs, outputs = line.strip("\n\r").split(sep)
                    inputs, outputs = inputs.split('&'), outputs.split('&')
                    tests.append([inputs, outputs])
                return tests

    @staticmethod
    def load_info(info_file):
        with open(info_file, encoding = 'utf-8') as f:
            lines = f.readlines()
            if lines:
                sep = lines[0].rstrip()
                del lines[0]
                infos = []
                for line in lines:
                    key, message, nums = line.strip("\n\r").split(sep)
                    infos.append([key, message, nums])
                return infos

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditTestWindow(None, 0)
    window.show()
    sys.exit(app.exec_())
