import os
import pickle

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

from info_frame import Frame_Info
from models.assignment import Info, Test
from path import OPENED_INFO_DATA, OPENED_TEST_DATA
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
        self.Test_btn.setStyleSheet(
            """QPushButton {
                background-color: rgba(255, 255, 255,50);
                border-radius: 10px;
                color: black;
            }"""
        )

class UIFunction(TestWindow):
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"
    path = None
    Format = [True, False]

    def __init__(self, ui):
        self.connect(ui)

    def connect(self, ui):
        ui.btn_quit.clicked.connect(lambda: self.reopen_edit(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        self.put_frame_in_list(ui, 0)
        self.put_frame_in_list(ui, 1)
        self.check_file(ui, OPENED_TEST_DATA, 0)
        self.check_file(ui, OPENED_INFO_DATA, 1)
        ui.stacked_widget.setCurrentIndex(0)
        ui.Test_btn.clicked.connect(lambda: self.changed(ui, 0))
        ui.Info_btn.clicked.connect(lambda: self.changed(ui, 1))
        ui.add_test.clicked.connect(lambda: self.add_frame(ui=ui))
        ui.add_info.clicked.connect(lambda: self.add_frame(ui=ui))

    def check_file(self, ui, filename, mode):
        ui.stacked_widget.setCurrentIndex(mode)
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load()
                for i in data[ui.index]:
                    if i:
                        self.add_frame(ui, i if mode == 0 else [], i if mode == 1 else [])

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

    def add_frame(self, ui, test=[], info=[]):
        if ui.stacked_widget.currentIndex() == 0:
            ui.frame = Frame_Test(ui_main=ui, test=test)
            ui.test.layout().addWidget(ui.frame)
        else:
            ui.frame = Frame_Info(ui_main=ui, info=info)
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
        self._saveData(ui, filename, results)    

    def saveInfo(self, ui, filename):
        infos = ui.info.children()
        infos.pop(0)
        results = []
        for info in infos:
            keyword, msg, min_num = info.keyword.text(), info.message.text(), info.count.value()
            results.append(Info(keyword, msg, min_num))
        self._saveData(ui, filename, results)    

    def _saveData(self, ui, filename, results):
        data = []
        if os.path.getsize(filename) > 0:
            with open(filename, 'rb') as f:
                unpickler = pickle.Unpickler(f)
                data = unpickler.load() 

        d = ui.index + 1 - len(data)
        if d > 0:
            data.extend([0 for _ in range(d)])

        with open(filename, 'wb') as f:
            data[ui.index] = results
            pickle.dump(data, f, -1)    

    def reopen_edit(self, ui):
        self.saveTest(ui, OPENED_TEST_DATA)
        self.saveInfo(ui, OPENED_INFO_DATA)
        ui.switch_window.emit()
        ui.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
