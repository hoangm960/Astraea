import argparse
import os
from pathlib import Path
from time import sleep
import pygetwindow as gw

VERSION = 2.6
PG = None

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
    OPENED_LESSON_PATH = "./data/Users/opened_assignment.oa"

    Path(USER_PATH).mkdir(parents=True, exist_ok=True)
    Path(ENCRYPTION_PATH).mkdir(parents=True, exist_ok=True)
    Path(OPENED_RESULT_PATH).mkdir(parents=True, exist_ok=True)
    open(OPENED_LESSON_PATH, 'w').close()



def open_idle():
    global PG
    os.system("start pythonwin")
    sleep(1)
    if gw.getWindowsWithTitle("PythonWin"):
        PG = gw.getWindowsWithTitle("PythonWin")[0]
    PG.minimize()


create_file()
open_idle()

if __name__ == "__main__":
    import login_main
    login_main.main(PG, VERSION)
    # login_main.main(args.file)
