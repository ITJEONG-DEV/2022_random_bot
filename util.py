import datetime
import json

log_path = "log/log.txt"


def parse_json(url):
    with open(url, "r", encoding="UTF-8") as json_text:
        json_contents = json.load(json_text)

        return json_contents


def set_log_path(path=""):
    if path == "":
        path = f"log/log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    global log_path
    log_path = path


def add_log(msg, label="log", saved=True, printed=True):
    log = f"[{label}] {msg} ({datetime.datetime.now().strftime('%H:%M:%S')})"

    if printed:
        print(log)

    if saved:
        with open(log_path, "a", encoding="UTF-8") as f:
            f.write(log + "\n")
