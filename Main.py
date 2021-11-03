import os
import sys
from pathlib import Path


from UI_Files import Resources
from path import *

VERSION = "3.2.2"

def init():
    os.chdir(os.path.dirname(sys.argv[0]))
    def create_file(file):
        if not os.path.exists(file):
            open(file, "w", encoding='utf8').close()
    def create_dir(dir):
        Path(dir).mkdir(parents=True, exist_ok=True)


    paths = [USER_DIR_PATH, ENCRYPTION_DIR_PATH, RESULT_DIR_PATH]
    files = [OPENED_DOC_CONTENT, OPENED_ROOM_PATH, OPENED_DOC, OPENED_ASSIGNMENT_PATH]

    for dir in paths:
        create_dir(dir)
    for file in files:
        create_file(file)

    associate_file()

def associate_file():  # sourcery skip: move-assign
    OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"
    file = sys.argv[1] if len(sys.argv) >= 2 else None
    if file:
        with open(OPENED_ASSIGNMENT_PATH, "w", encoding="utf8") as f:
            f.writelines([f"{file}\n", "0"])

if __name__ == "__main__":

    init()

    import ui_controller
    ui_controller.main(VERSION)
