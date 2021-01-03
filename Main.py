import os
import subprocess
from pathlib import Path
from time import sleep

import pygetwindow as gw

VERSION = "2.6"
PG = None

def create_file():
    USER_PATH = "./data/Users/"
    ENCRYPTION_PATH = "./data/encryption/"
    OPENED_RESULT_PATH = "./data/results/"
    OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"
    OPENED_DOC = "./data/Users/opened_doc.od"


    Path(USER_PATH).mkdir(parents=True, exist_ok=True)
    Path(ENCRYPTION_PATH).mkdir(parents=True, exist_ok=True)
    Path(OPENED_RESULT_PATH).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(OPENED_DOC):
        open(OPENED_DOC, "w").close()
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


if __name__ == "__main__":
    check_ide()
    create_file()
    open_ide()
    
    import login_main
    login_main.main(PG, VERSION)
