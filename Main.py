import os
from pathlib import Path


VERSION = "2.6.2"


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


if __name__ == "__main__":

    create_file()

    import login_main
    login_main.main(VERSION)
