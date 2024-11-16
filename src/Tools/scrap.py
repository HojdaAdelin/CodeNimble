import requests

def get_latest_version_from_github(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    
    try:
        response = requests.get(url, timeout=5)  # Timeout pentru a evita blocarea
        response.raise_for_status()  # Ridică o excepție pentru coduri de eroare HTTP

        # Extragem versiunea cea mai recentă
        latest_version = response.json().get("tag_name", "Unknown version")
        return latest_version
    
    except requests.ConnectionError:
        return "No internet connection"
    except requests.Timeout:
        return "Request timed out"
    except requests.RequestException as e:
        # Orice altă eroare
        return f"Error: {e}"
