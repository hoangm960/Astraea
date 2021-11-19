import time

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow

from utils.config import SCREEN_HEIGHT, SCREEN_WIDTH, find_ide, install_ide
from utils.connect_db import get_connection
from utils.encryption import *

UI_PATH = "./UI_files/Loading_Screen.ui"


class LoadingScreen(QMainWindow):
    counter = 0
    switch_window = QtCore.pyqtSignal(object)

    def __init__(self, version):
        self.version = version

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_PATH, self)
        self.initUI()
        UIFunction(self)

    def initUI(self):
        self.move(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.frame.hide()


class UIFunction(LoadingScreen):
    pg = None

    def __init__(self, ui):
        self.update_version(ui, )
        self.connect_btn(ui)
        ui.timer = QtCore.QTimer()
        ui.timer.timeout.connect(lambda: self.progress(ui))
        ui.timer.start(20)

    def connect_btn(self, ui):
        ui.Out.clicked.connect(lambda: ui.close())
        ui.pushButton.clicked.connect(lambda: self.tryAgain(ui, ui.version))
        

    def update_version(self, ui):
        ui.versionLabel.setText(
            f'<html><head/><body><p align="right"><span style=" font-size:14pt; color:#ffffff;">v{ui.version}</span></p></body></html>'
        )

    def delay(self, point, wait):
        if self.counter == point:
            time.sleep(wait)

    def tryAgain(self, ui, version):
        ui.close()
        window = LoadingScreen(version)
        window.show()

    def progress(self, ui):
        ui.progressBar.setValue(self.counter)
        if self.counter >= 100:
            ui.timer.stop()
            ui.switch_window.emit(self.pg)

        if self.counter == 6:
            ui.timer.singleShot(
                1500, lambda: ui.Loading_label.setText("kiểm tra cài đặt ...")
            )
            try:
                import thonny
            except ImportError:
                ui.timer.singleShot(
                    500, lambda: ui.Loading_label.setText("đang tải Thonny...")
                )
                install_ide()
                
        if self.counter == 14:
            ui.timer.singleShot(2905, lambda: ui.Loading_label.setText("khởi động ..."))
            self.pg = find_ide()
            self.pg.minimize()

        if self.counter == 50:
            ui.Loading_label.setText("đang kết nối...")
        if self.counter == 73:
            time.sleep(3)
            try:
                get_connection()
            except:
                ui.Loading_label.setText(
                    "kết nối thất bại. Đường truyền không ổn định."
                )
                ui.frame.show()
                ui.timer.stop()
                ui.progressBar.hide()
                self.pg.close()

        # self.delay(randrange(5, 10), 0.1)
        # self.delay(randrange(20, 30), 0.23)
        # self.delay(randrange(40, 50), 0.43)
        # self.delay(randrange(60, 70), 0.93)
        # self.delay(randrange(60, 70), 0.93)
        # self.delay(randrange(60, 70), 0.93)
        # self.delay(randrange(60, 70), 0.93)
        # self.delay(randrange(60, 70), 0.93)
        # self.delay(randrange(60, 70), 0.93)
        # self.delay(randrange(80, 90), 0.17)
        # self.delay(randrange(90, 99), 0.6)
        self.delay(99, 1)
        self.counter += 1
        