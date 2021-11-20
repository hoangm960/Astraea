import subprocess
import time

import pyautogui as auto
from PyQt5.QtWidgets import QApplication


def screen_resolution():
    app = QApplication([])
    screen_resolution = app.desktop().availableGeometry()
    return screen_resolution.width(), screen_resolution.height()

def find_ide():
    import pygetwindow as gw

    subprocess.Popen(["thonny"])
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
    
def install_ide():
    p = subprocess.run("pip install thonny")
    if p.returncode == 0:
        subprocess.Popen(["thonny"])
        time.sleep(3)
        try:
            auto.click('utils/click.png')
        except:
            pass
        

SCREEN_WIDTH, SCREEN_HEIGHT = screen_resolution()
