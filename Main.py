import os
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from UI_Files import Resources

VERSION = "3.2"

def init():
    def create_file(file):
        if not os.path.exists(file):
            open(file, "w", encoding='utf8').close()
    def create_dir(dir):
        Path(dir).mkdir(parents=True, exist_ok=True)

    USER_PATH = "./data/Users/"
    ENCRYPTION_PATH = "./data/encryption/"
    OPENED_RESULT_PATH = "./data/results/"
    OPENED_ASSIGNMENT_PATH = "./data/Users/opened_assignment.oa"
    OPENED_DOC = "./data/Users/opened_doc.od"
    OPENED_ROOM_PATH = "./data/Users/opened_room.or"
    OPENED_DOC_CONTENT = "./data/Users/opened_doc_content.html"


    paths = [USER_PATH, ENCRYPTION_PATH, OPENED_RESULT_PATH]
    files = [OPENED_DOC_CONTENT, OPENED_ROOM_PATH, OPENED_DOC, OPENED_ASSIGNMENT_PATH]

    for dir in paths:
        create_dir(dir)
    for file in files:
        create_file(file)

def screen_resolution():
    app = QApplication([])
    screen_resolution = app.desktop().availableGeometry()
    return screen_resolution.width(), screen_resolution.height()


if __name__ == "__main__":

    init()

    import ui_controller
    ui_controller.main(VERSION)
