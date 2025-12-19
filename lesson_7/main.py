import time
from pathlib import Path

def func(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            print(line, end="")

if __name__ == "__main__":
    log_path = Path(__file__).with_name("app.log")
    func(str(log_path))
