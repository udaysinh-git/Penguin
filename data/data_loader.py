import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "bot_data.json"

def _load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_logs_channel_id():
    data = _load_data()
    return data.get("logs_channel_id")

def set_logs_channel_id(channel_id):
    data = _load_data()
    data["logs_channel_id"] = channel_id
    _save_data(data)
