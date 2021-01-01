import argparse
import os
import subprocess
from pathlib import Path
from time import sleep

import pygetwindow as gw

VERSION = "2.9"
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
    OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"

    Path(USER_PATH).mkdir(parents=True, exist_ok=True)
    Path(ENCRYPTION_PATH).mkdir(parents=True, exist_ok=True)
    Path(OPENED_RESULT_PATH).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(OPENED_ASSIGNMENT_PATH):
        open(OPENED_ASSIGNMENT_PATH, "w").close()


def check_ide():
    try:
        import thonny
    except ImportError:
        subprocess.call('pip3 install thonny')
        sleep(2)


def open_ide():
    global PG
    subprocess.Popen(['thonny'], shell=True)
    sleep(2)
    ide_title = ''
    while not ide_title:
        titles = gw.getAllTitles()
        for title in titles:
            if "thonny" in title.lower():
                ide_title = title
                break
    if gw.getWindowsWithTitle(ide_title):
        PG = gw.getWindowsWithTitle(ide_title)[0]
        PG.minimize()

check_ide()
create_file()
open_ide()

if __name__ == "__main__":
    import login_main
    login_main.main(PG, VERSION)
    # login_main.main(args.file)
