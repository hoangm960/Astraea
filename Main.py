import argparse
import os
import subprocess
import sys
from pathlib import Path

import pygetwindow as gw
from win32api import GetMonitorInfo, MonitorFromPoint


USER_PATH = "./data/Users/"
ENCRYPTION_PATH = "./data/encryption/"
OPENED_RESULT_PATH = "./data/results/"
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
SCREEN_WIDTH, SCREEN_HEIGHT = work_area[2], work_area[3]

Path(USER_PATH).mkdir(parents=True, exist_ok=True)
Path(ENCRYPTION_PATH).mkdir(parents=True, exist_ok=True)
Path(OPENED_RESULT_PATH).mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(
    description="Astraea - Công cụ hỗ trợ dạy học"
)
parser.add_argument(
    "--file", type=str, help="Mở ứng dụng với file cho trước."
)
args = parser.parse_args()

def find_idle():
    class Error(Exception): pass

    def _find(pathname, matchFunc=os.path.isfile):
        for dirname in sys.path:
            candidate = os.path.join(dirname, pathname)
            if matchFunc(candidate):
                return candidate
        raise Error("Can't find file %s" % pathname)

    return _find("Lib\site-packages\pythonwin\Pythonwin.exe")

pg = None
def open_idle():
    global pg
    subprocess.Popen([find_idle()])

    while True:
        if gw.getWindowsWithTitle("PythonWin"):
            pg = gw.getWindowsWithTitle("PythonWin")[0]
            break
    pg.minimize()

open_idle()

import login_main
# login_main.main(args.file)
login_main.main()
