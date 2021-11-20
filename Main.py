import os
import sys
from pathlib import Path


from UI_Files import Resources
from path import *

VERSION = "3.3.2"


def init():
    os.chdir(os.path.dirname(sys.argv[0]))

    def create_file(file):
        if not os.path.exists(file):
            open(file, "w", encoding="utf8").close()

    def create_dir(dir):
        Path(dir).mkdir(parents=True, exist_ok=True)

    paths = [USER_DIR_PATH, ENCRYPTION_DIR_PATH, RESULT_DIR_PATH]
    files = [
        OPENED_DOC_CONTENT,
        OPENED_ROOM_PATH,
        OPENED_DOC,
        OPENED_ASSIGNMENT_PATH,
        OPENED_TEST_DATA,
        OPENED_INFO_DATA,
        COMMENT_PATH,
    ]

    for dir in paths:
        create_dir(dir)
    for file in files:
        create_file(file)

    for filename in [
        OPENED_TEST_DATA,
        OPENED_INFO_DATA,
        OPENED_DOC_CONTENT,
        COMMENT_PATH,
    ]:
        init_data(filename)
    associate_file()


def init_data(filename):
    if os.path.getsize(filename) > 0:
        with open(filename, "w") as f:
            f.write("")


def associate_file():
    file = sys.argv[1] if len(sys.argv) >= 2 else None
    if file:
        with open(OPENED_ASSIGNMENT_PATH, "w", encoding="utf8") as f:
            f.writelines([f"{file}\n", "0"])


if __name__ == "__main__":

    init()

    import ui_controller

    ui_controller.main(VERSION)
