import json
import os

SETTINGS_FILE = "settings.json"


def load_settings():
    """加载设置文件"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"birthdate": "1988-07-19", "lifespan_years": 75}


def save_settings(settings):
    """保存设置文件"""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
