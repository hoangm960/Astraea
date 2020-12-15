import argparse
import os
import subprocess
import sys
from pathlib import Path
from time import sleep
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QLineEdit,
                             QListWidgetItem, QMainWindow, QMessageBox)
import pygetwindow as gw
from PyQt5 import QtCore

VERSION = 2.5

parser = argparse.ArgumentParser(
    description="Astraea - Công cụ hỗ trợ dạy học"
)
parser.add_argument(
    "--file", type=str, help="Mở ứng dụng với file cho trước."
)
args = parser.parse_args()


def create_file():
    USER_PATH = "./data/Users/"
    ENCRYPTION_PATH = "./data/encryption/"
    OPENED_RESULT_PATH = "./data/results/"

    Path(USER_PATH).mkdir(parents=True, exist_ok=True)
    Path(ENCRYPTION_PATH).mkdir(parents=True, exist_ok=True)
    Path(OPENED_RESULT_PATH).mkdir(parents=True, exist_ok=True)


# def find_idle():
#     class Error(Exception):
#         pass

#     def _find(pathname, matchFunc=os.path.isfile):
#         for dirname in sys.path:
#             candidate = os.path.join(dirname, pathname)
#             if matchFunc(candidate):
#                 return candidate
#         raise Error("Can't find file %s" % pathname)

#     return _find("Lib\site-packages\pythonwin\Pythonwin.ex")


pg = None
def open_idle():
    global pg
    os.system("start pythonwin")
    sleep(1)
    if gw.getWindowsWithTitle("PythonWin"):
        pg = gw.getWindowsWithTitle("PythonWin")[0]
    pg.minimize()


open_idle()

if __name__ == "__main__":
    import login_main
    login_main.main(pg, VERSION)
    # login_main.main(args.file)
