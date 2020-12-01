import argparse

from pathlib import Path

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

import login_main
login_main.main()