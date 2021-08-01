import subprocess
import time
from random import randrange

import mysql.connector
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow
import pyautogui as auto

import Main
from encryption import *


class LoadingScreen(QMainWindow):
    counter = 0
    switch_window = QtCore.pyqtSignal(object)

    def __init__(self, version):
        self.version = version

        QMainWindow.__init__(self)
        uic.loadUi("./UI_files/Loading_Screen.ui", self)
        self.move(
            round((Main.SCREEN_WIDTH - self.width()) / 2),
            round((Main.SCREEN_HEIGHT - self.height()) / 2),
        )
        UIFunction(self, version)


class UIFunction(LoadingScreen):
    pg = None

    def __init__(self, ui, version):
        self.update_version(ui, str(version))

        ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui.frame.hide()
        ui.Out.clicked.connect(lambda: ui.close())
        ui.pushButton.clicked.connect(lambda: self.tryAgain(ui, version))
        ui.timer = QtCore.QTimer()
        ui.timer.timeout.connect(lambda: self.progress(ui))
        ui.timer.start(20)
        ui.show()

    @staticmethod
    def update_version(ui, version):
        ui.version.setText(
            f'<html><head/><body><p align="right"><span style=" font-size:14pt; color:#ffffff;">v{version}</span></p></body></html>'
        )

    def delay(self, point, wait):
        if self.counter == point:
            time.sleep(wait)

    def tryAgain(self, ui, version):
        ui.close()
        window = LoadingScreen(version)
        window.show()

    def install_ide(self):
        subprocess.call("pip3 install thonny")
        subprocess.Popen(["thonny"], shell=True)
        pg = self.find_ide()
        pg.activate()
        auto.press("enter")
        pg.close()

    def find_ide(self):
        import pygetwindow as gw

        subprocess.Popen(["thonny"], shell=True)
        time.sleep(2)
        ide_title = ""
        while not ide_title:
            titles = gw.getAllTitles()
            for title in titles:
                if "thonny" in title.lower():
                    ide_title = title
                    break
        if gw.getWindowsWithTitle(ide_title):
            return gw.getWindowsWithTitle(ide_title)[0]

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
                self.install_ide()
                
        if self.counter == 14:
            ui.timer.singleShot(2905, lambda: ui.Loading_label.setText("khởi động ..."))
            self.pg = self.find_ide()
            self.pg.minimize()

        if self.counter == 50:
            ui.Loading_label.setText("đang kết nối...")
        if self.counter == 73:
            time.sleep(3)
            try:
                mysql.connector.connect(
                    host="remotemysql.com",
                    user="53K73q3Z6I",
                    password="DpXgsUvOuu",
                    database="53K73q3Z6I",
                )
            except:
                ui.Loading_label.setText(
                    "kết nối thất bại. Đường truyền không ổn định."
                )
                ui.frame.show()
                ui.timer.stop()
                ui.progressBar.hide()
                self.pg.close()

        self.delay(randrange(5, 10), 0.1)
        self.delay(randrange(20, 30), 0.23)
        self.delay(randrange(40, 50), 0.43)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(60, 70), 0.93)
        self.delay(randrange(80, 90), 0.17)
        self.delay(randrange(90, 99), 0.6)
        self.delay(99, 1)
        self.counter += 1
        