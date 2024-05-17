import requests

CURRENT_VERSION = "1.3"

def get_latest_version_from_github(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        latest_version = response.json()["tag_name"]
        return latest_version
    else:
        return "Failed to get current version"