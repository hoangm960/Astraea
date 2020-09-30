import errno
import os
import platform
import subprocess
from pywinauto import application
import pygetwindow as gw



def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == errno.ENOENT:
            return False
    return True


def find_prog(prog):
    if is_tool(prog):
        cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.call([cmd, prog])


file = os.path.expandvars("%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe")
subprocess.call(file)
vs_window = gw.getWindowsWithTitle("Visual Studio Code")[0]
vs_window.moveTo(0, 0)