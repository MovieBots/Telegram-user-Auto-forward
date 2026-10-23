import json
import os
from pathlib import Path

CONFIG_PATH = Path(os.getenv("CONFIG_PATH", "config.json"))

def load_config():
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return {
                "sources": list(data.get("sources", [])),
                "destination": data.get("destination", ""),
            }
        except Exception:
            pass
    return {
        "sources": [x.strip() for x in os.getenv("SOURCE_CHANNELS", "").split(",") if x.strip()],
        "destination": os.getenv("DESTINATION_CHANNEL", "").strip(),
    }

def save_config(config):
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
