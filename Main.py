import login_main
import argparse
from pathlib import Path

USER_PATH = "data/Users/"
ENCRYPTION_PATH = "data/encryption/"
OPENED_RESULT_PATH = "./data/results/"

Path(USER_PATH).mkdir(parents=True, exist_ok=True)
Path(ENCRYPTION_PATH).mkdir(parents=True, exist_ok=True)
Path(OPENED_RESULT_PATH).mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(
    description="Astraea - Công cụ hỗ trợ dạy học"
)
parser.add_argument(
    "--file", type=str, help="Mở ứng dụng với file cho trước."
)
args = parser.parse_args()
# login_main.main(args.file)

login_main.main()
