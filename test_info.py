import os
import pickle

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QMessageBox
from info_frame import Frame_Info

from models.assignment import Test
from path import OPENED_TEST_DATA
from test_frame import Frame_Test

TEST_PATH = "./UI_Files/Test_Info.ui"


class TestWindow(QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self, index):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(TEST_PATH, self)
        self.index = index
        self.init_UI()
        UIFunction(self)

    def init_UI(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()
        self.title_bar.mouseMoveEvent = self.moveWindow
        self.Test_btn.setStyleSheet(
            """QPushButton {
                background-color: rgba(255, 255, 255,50);
                border-radius: 10px;
                color: black;
            }"""
        )

    def moveWindow(self, event):
        if UIFunction.GLOBAL_STATE == True:
            UIFunction.maximize_restore(ui=self)
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class UIFunction(TestWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
    GLOBAL_STATE = True
    path = None
    Format = [True, False]

    def __init__(self, ui):
        self.connect(ui)

    def connect(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.reopen_edit(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        self.put_frame_in_list(ui, 0)
        self.put_frame_in_list(ui, 1)
        ui.stacked_widget.setCurrentIndex(0)
        self.check_test(ui, OPENED_TEST_DATA)
        ui.Test_btn.clicked.connect(lambda: self.changed(ui, 0))
        ui.Info_btn.clicked.connect(lambda: self.changed(ui, 1))
        ui.add_test.clicked.connect(lambda: self.add_frame(ui=ui))
        ui.add_info.clicked.connect(lambda: self.add_frame(ui=ui))

    def check_test(self, ui, filename):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
                if data[0] != 0:
                    for i in data[0]:
                        self.add_frame(ui, i)

    def changed(self, ui, k):
        if k == 0:
            ui.stacked_widget.setCurrentIndex(0)
            ui.Test_btn.setStyleSheet(
                """QPushButton {
                    background-color: rgba(255, 255, 255,50);
                    border-radius: 10px;
                    color: black;
                }"""
            )
            ui.Info_btn.setStyleSheet(
                """QPushButton {
                    background-color: rgb(255, 255, 255);
                    border-radius: 10px;
                    color: black;
                }"""
            )
        else:
            ui.stacked_widget.setCurrentIndex(1)
            ui.Info_btn.setStyleSheet(
                """QPushButton {
                    background-color: rgba(255, 255, 255,50);
                    border-radius: 10px;
                    color: black;
                }"""
            )

            ui.Test_btn.setStyleSheet(
                """QPushButton {
                    background-color: rgb(255, 255, 255);
                    border-radius: 10px;
                    color: black;
                }"""
            )

    def put_frame_in_list(self, ui, num):
        if num:
            current_layout = ui.test.layout()
            if not current_layout:
                current_layout = QVBoxLayout()
                current_layout.setContentsMargins(9, 9, 9, 9)
                ui.test.setLayout(current_layout)
            for i in reversed(range(current_layout.count())):
                current_layout.itemAt(i).widget().setParent(None)

            ui.scroll_test.verticalScrollBar().setValue(1)
        else:
            current_layout = ui.info.layout()
            if not current_layout:
                current_layout = QVBoxLayout()
                current_layout.setContentsMargins(9, 9, 9, 9)
                ui.info.setLayout(current_layout)
            for i in reversed(range(current_layout.count())):
                current_layout.itemAt(i).widget().setParent(None)

            ui.scroll_info.verticalScrollBar().setValue(1)

    def add_frame(self, ui, test=[]):
        if ui.stacked_widget.currentIndex() == 0:
            ui.frame = Frame_Test(ui_main=ui, test=test)
            ui.test.layout().addWidget(ui.frame)
        else:
            ui.frame = Frame_Info(ui)
            ui.info.layout().addWidget(ui.frame)

    def saveTest(self, ui, filename):
        tests = ui.test.children()
        tests.pop(0)
        results = []
        for test in tests:
            inputs, outputs = test.input.children(), test.output.children()
            inputs.pop(0)
            outputs.pop(0)
            results.append(Test([i.text() for i in inputs], [i.text() for i in outputs]))
        with open(filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
        with open(filename, "wb") as f:
            data[ui.index] = results 
            pickle.dump(data, f, -1)    

    def reopen_edit(self, ui):
        self.saveTest(ui, OPENED_TEST_DATA)
        ui.switch_window.emit()
        ui.close()

    def maximize_restore(self, ui):
        status = self.GLOBAL_STATE
        if status == False:
            ui.showMaximized()

            self.GLOBAL_STATE = True
            ui.centralwidget.setStyleSheet(
                """background-color: rgb(74, 74, 74);
                    border-radius: 0px;"""
            )
            ui.btn_maximize.setToolTip("khôi phục")
        else:
            self.GLOBAL_STATE = False
            ui.showNormal()
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.centralwidget.setStyleSheet(
                """background-color: rgb(74, 74, 74);
    border-radius: 20px;"""
            )
            ui.btn_maximize.setToolTip("Phóng to")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
