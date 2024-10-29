import json
import requests
import shutil
import zipfile
import os

def main():
    url = "https://api.github.com/repos/HojdaAdelin/CodeNimble/releases/latest"

    try:
        response = requests.get(url)
        data = response.json()

        assets = data.get("assets", [])
        download_url = None
        for asset in assets:
            if asset.get("name") == "CodeNimble-build.zip":
                download_url = asset.get("browser_download_url")
                break

        if not download_url:
            print("Update package not found.")
            return

        print("Downloading update...")
        zip_path = "update.zip"
        with requests.get(download_url, stream=True) as r:
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        extract_path = "update_temp"
        os.makedirs(extract_path, exist_ok=True)

        print("Extracting update...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        print("Applying update...")
        for item in os.listdir(extract_path):
            source = os.path.join(extract_path, item)
            destination = os.path.join(".", item)

            try:
                if os.path.isdir(source):
                    if os.path.exists(destination):
                        # Copiază fiecare fișier în parte pentru a suprascrie doar fișierele individuale
                        for root, _, files in os.walk(source):
                            dest_dir = os.path.join(destination, os.path.relpath(root, source))
                            os.makedirs(dest_dir, exist_ok=True)
                            for file in files:
                                shutil.copy2(os.path.join(root, file), dest_dir)
                    else:
                        shutil.copytree(source, destination)  # Copiază dacă nu există
                else:
                    shutil.copy2(source, destination)  # Suprascrie fișierul existent
                print(f"Successfully updated: {item}")
            except Exception as e:
                print(f"Failed to update {item}: {e}")

        os.remove(zip_path)
        shutil.rmtree(extract_path)
        print("Update completed successfully! Please restart the application.")

    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    main()
