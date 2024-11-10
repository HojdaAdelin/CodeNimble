import json
import os
import subprocess
import sys
import requests

def get_current_version():
    if os.path.exists("app_data_/version.json"):
        try:
            with open("app_data_/version.json", "r") as f:
                config_data = json.load(f)
            
            version = config_data.get("version")
            if version:  
                return version
        except (json.JSONDecodeError, KeyError):
            pass
    return "2.0"


def check_for_updates(status_bar):
    current_version = get_current_version()
    print(f"Current version: {current_version}")

    try:
        url = "https://api.github.com/repos/HojdaAdelin/CodeNimble/releases/latest"

        response = requests.get(url)
        data = response.json()

        latest_version = data.get("tag_name")

        if latest_version and latest_version > current_version:
            print(f"New version available: {latest_version}")
            update() 
        else:
            status_bar.toggle_inbox_icon(f"Current version: {current_version}\nYou already have the latest version.")
            print("You already have the latest version.")

    except Exception as e:
        print(f"Failed to check for updates: {e}")

def update():
    print("Closing application to apply update...")
    subprocess.Popen([sys.executable, 'update.py'])
    sys.exit()