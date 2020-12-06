import login_main
import argparse
from win32api import GetMonitorInfo, MonitorFromPoint
from pathlib import Path

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
SCREEN_WIDTH, SCREEN_HEIGHT = work_area[2], work_area[3]

USER_PATH = "data/Users/"
ENCRYPTION_PATH = "data/encryption/"

parser = argparse.ArgumentParser(
    description="Automate data processing and check data."
)
parser.add_argument(
    "--file", type=str, help="Mở ứng dụng với file cho trước."
)
args = parser.parse_args()
Path(USER_PATH).mkdir(parents=True, exist_ok=True)
Path(ENCRYPTION_PATH).mkdir(parents=True, exist_ok=True)
# login_main.main(args.file)

if __name__ == "__main__":
    login_main.main()
